#!/usr/bin/env python3
"""Turn a Raindrop collection into a Jekyll post (Python 3.9+, stdlib only)."""

import argparse
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from datetime import date, datetime, time as datetime_time, timedelta, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
PACIFIC = ZoneInfo("America/Los_Angeles")


def week_bounds(week_start=None, now=None):
    """Return Pacific midnights, Monday inclusive through next Monday exclusive."""
    now = now or datetime.now(PACIFIC)
    if week_start:
        start = date.fromisoformat(week_start)
        if start.weekday() != 0:
            raise ValueError("--week-start must be a Monday (YYYY-MM-DD).")
    else:
        today = now.astimezone(PACIFIC).date()
        start = today - timedelta(days=today.weekday() + 7)
    return (
        datetime.combine(start, datetime_time.min, PACIFIC),
        datetime.combine(start + timedelta(days=7), datetime_time.min, PACIFIC),
    )


def fetch_bookmarks(token, collection_id):
    """Read every API page; retry temporary failures without printing credentials."""
    if not token:
        raise ValueError("Set RAINDROP_TOKEN, or use --input-json for an offline test.")
    if not collection_id or not str(collection_id).isdigit() or int(collection_id) <= 0:
        raise ValueError("RAINDROP_COLLECTION_ID must be your collection's positive numeric ID.")
    bookmarks = []
    page = 0
    while True:
        query = urlencode({"page": page, "perpage": 50, "sort": "created"})
        request = Request(
            "https://api.raindrop.io/rest/v1/raindrops/{}?{}".format(collection_id, query),
            headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
        )
        for attempt in range(3):
            try:
                with urlopen(request, timeout=30) as response:
                    payload = json.load(response)
                break
            except HTTPError as error:
                if error.code in (429, 500, 502, 503, 504) and attempt < 2:
                    retry_after = error.headers.get("Retry-After", "")
                    delay = min(int(retry_after), 30) if retry_after.isdigit() else 2 ** (attempt + 1)
                    time.sleep(delay)
                    continue
                raise ValueError("Raindrop request failed (HTTP {}). Check the token and collection ID.".format(error.code)) from None
            except (URLError, TimeoutError):
                if attempt < 2:
                    time.sleep(2 ** (attempt + 1))
                    continue
                raise ValueError("Cannot reach Raindrop after three attempts. Try again later.") from None
        if not isinstance(payload, dict) or payload.get("result") is not True:
            raise ValueError("Raindrop returned an unsuccessful response.")
        items = payload.get("items")
        if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
            raise ValueError("Raindrop returned invalid bookmark data.")
        bookmarks.extend(items)
        if len(items) < 50:
            return bookmarks
        page += 1


def published_entries(posts_dir):
    """Read JSON-compatible YAML tracking fields from previously generated posts."""
    ids, urls = set(), set()
    for path in sorted(posts_dir.glob("*.md")) + sorted(posts_dir.glob("*.markdown")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        frontmatter = text.split("\n---", 1)[0]
        for field, target in (("weekly_reading_ids", ids), ("weekly_reading_urls", urls)):
            match = re.search(r"^" + field + r": (.+)$", frontmatter, re.MULTILINE)
            if match:
                values = json.loads(match.group(1))
                if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
                    raise ValueError("Invalid {} tracking field in {}.".format(field, path.name))
                target.update(values)
    return ids, urls


def bookmark_url(value):
    """Validate a web link and encode characters unsafe in a Markdown destination."""
    if not isinstance(value, str) or any(ord(c) < 32 for c in value):
        raise ValueError("A bookmark has an invalid URL.")
    value = value.strip()
    parts = urlsplit(value)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError("Bookmarks must have an http or https URL.")
    return quote(value, safe="/:?&=#%+@!$;,~-._")


def select_bookmarks(items, start, end, known_ids, known_urls, include_all=False, now=None):
    now = now or datetime.now(timezone.utc)
    selected = []
    seen_ids, seen_urls = set(known_ids), set(known_urls)
    dated = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("_id"), int):
            raise ValueError("Each bookmark must have a numeric _id.")
        created = datetime.fromisoformat(str(item.get("created", "")).replace("Z", "+00:00"))
        if created.tzinfo is None:
            raise ValueError("Bookmark creation dates must include a timezone.")
        dated.append((created, item))
    for created, item in sorted(dated, key=lambda pair: (pair[0], pair[1]["_id"])):
        if created > now or (not include_all and not start <= created < end):
            continue
        identifier = str(item["_id"])
        url = bookmark_url(item.get("link"))
        if identifier in seen_ids or url in seen_urls:
            continue
        selected.append(dict(item, link=url))
        seen_ids.add(identifier)
        seen_urls.add(url)
    return selected


def plain_text(value):
    """Render captured text literally, including HTML, Markdown and Liquid syntax."""
    text = " ".join(str(value or "").split())
    text = html.escape(text, quote=False).replace("{", "&#123;").replace("}", "&#125;")
    return re.sub(r"([\\`*_\[\]#!|])", r"\\\1", text)


def render_post(items, start, end, now=None, include_all=False):
    now = (now or datetime.now(PACIFIC)).astimezone(PACIFIC)
    start_date = start.date().isoformat()
    title = "Things I Read — Week of " + start_date
    intro = "Articles and interesting things I read from {} through {}.".format(
        start_date, (end.date() - timedelta(days=1)).isoformat()
    )
    if include_all:
        intro = "A roundup of links saved in my reading collection. This first roundup includes earlier saves too."
    lines = [
        "---", "layout: post", "title: " + json.dumps(title, ensure_ascii=False),
        "date: " + now.strftime("%Y-%m-%d %H:%M:%S %z"),
        'categories: ["weekly-reading"]',
        "excerpt: " + json.dumps(intro),
        "weekly_reading_week: " + json.dumps(start_date),
        "weekly_reading_ids: " + json.dumps([str(item["_id"]) for item in items]),
        "weekly_reading_urls: " + json.dumps([item["link"] for item in items]),
        "---", "", intro, "",
    ]
    for item in items:
        title = plain_text(item.get("title") or urlsplit(item["link"]).hostname)
        lines.extend(["### [{}](<{}>)".format(title, item["link"]), ""])
        # Raindrop's `note` is the user's writing; `excerpt` can be scraped text.
        if item.get("note"):
            lines.extend([plain_text(item["note"]), ""])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week-start", help="Monday YYYY-MM-DD; default: previous completed week")
    parser.add_argument("--include-all", action="store_true", help="Include all unpublished saves, regardless of week (first-run test)")
    parser.add_argument("--dry-run", action="store_true", help="Print Markdown without writing a post")
    parser.add_argument("--input-json", type=Path, help="Read a bookmark array or API response from a local file instead of Raindrop")
    parser.add_argument("--posts-dir", type=Path, default=ROOT / "docs" / "_posts")
    args = parser.parse_args(argv)
    start, end = week_bounds(args.week_start)
    # Sunday filenames are stable even if Monday's run is delayed or retried.
    path = args.posts_dir / ((end.date() - timedelta(days=1)).isoformat() + "-weekly-reading.md")
    if path.exists():
        print("Skipped: {} already exists; existing posts are never overwritten.".format(path), file=sys.stderr)
        return 0
    if args.input_json:
        payload = json.loads(args.input_json.read_text(encoding="utf-8"))
        items = payload.get("items") if isinstance(payload, dict) else payload
        if not isinstance(items, list):
            raise ValueError("--input-json must contain a bookmark array or an object with items.")
    else:
        items = fetch_bookmarks(os.environ.get("RAINDROP_TOKEN"), os.environ.get("RAINDROP_COLLECTION_ID"))
    known_ids, known_urls = published_entries(args.posts_dir)
    selected = select_bookmarks(items, start, end, known_ids, known_urls, args.include_all)
    if not selected:
        print("Skipped: no unpublished links for this selection.", file=sys.stderr)
        return 0
    content = render_post(selected, start, end, include_all=args.include_all)
    if args.dry_run:
        print(content)
        print("Preview: {} links; would write {}.".format(len(selected), path), file=sys.stderr)
    else:
        args.posts_dir.mkdir(parents=True, exist_ok=True)
        # Link a fully written temporary file into place, without overwriting.
        # A failed write cannot leave a partial post that looks already published.
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=args.posts_dir, delete=False) as output:
                temp_path = Path(output.name)
                output.write(content)
            os.link(temp_path, path)
        finally:
            if temp_path is not None:
                temp_path.unlink()
        print("Created {} with {} links.".format(path, len(selected)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as error:
        print("Error: {}".format(error), file=sys.stderr)
        sys.exit(1)
