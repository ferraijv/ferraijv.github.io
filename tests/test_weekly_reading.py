import contextlib
from datetime import datetime, timezone
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError


spec = importlib.util.spec_from_file_location(
    "weekly_reading", Path(__file__).resolve().parents[1] / "scripts/generate_weekly_reading.py"
)
reading = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reading)


def bookmark(identifier=1, created="2026-10-06T12:00:00Z", link="https://example.com/article", **fields):
    return dict(_id=identifier, created=created, link=link, title="An article", **fields)


class WeeklyReadingTests(unittest.TestCase):
    def setUp(self):
        self.start, self.end = reading.week_bounds("2026-10-05")
        self.now = datetime(2026, 10, 12, 16, tzinfo=timezone.utc)

    def select(self, items, ids=None, urls=None, include_all=False):
        return reading.select_bookmarks(items, self.start, self.end, ids or set(), urls or set(), include_all, self.now)

    def test_previous_week_and_dst_boundaries(self):
        start, end = reading.week_bounds(now=datetime(2026, 11, 2, 16, tzinfo=timezone.utc))
        self.assertEqual(start.date().isoformat(), "2026-10-26")
        self.assertEqual(end.date().isoformat(), "2026-11-02")
        self.assertEqual((end.astimezone(timezone.utc) - start.astimezone(timezone.utc)).total_seconds(), 169 * 3600)
        with self.assertRaisesRegex(ValueError, "Monday"):
            reading.week_bounds("2026-10-06")

    def test_pacific_window_not_utc_calendar(self):
        items = [
            bookmark(1, "2026-10-05T06:59:59Z"),
            bookmark(2, "2026-10-05T07:00:00Z", "https://example.com/start"),
            bookmark(3, "2026-10-12T06:59:59Z", "https://example.com/end"),
            bookmark(4, "2026-10-12T07:00:00Z", "https://example.com/next"),
        ]
        self.assertEqual([item["_id"] for item in self.select(items)], [2, 3])

    def test_duplicate_ids_and_urls_across_and_within_posts(self):
        items = [bookmark(1), bookmark(2), bookmark(3, link="https://example.com/other")]
        self.assertEqual([item["_id"] for item in self.select(items)], [1, 3])
        self.assertEqual(self.select(items, {"1", "3"}, {"https://example.com/article"}), [])

    def test_include_all_and_future_dates(self):
        items = [bookmark(1, "2025-01-01T00:00:00Z"), bookmark(2, "2027-01-01T00:00:00Z")]
        self.assertEqual(self.select(items), [])
        self.assertEqual([item["_id"] for item in self.select(items, include_all=True)], [1])

    def test_render_escapes_captured_content_and_only_uses_user_note(self):
        item = bookmark(note='<script>alert(1)</script> {{ site.title }} [extra](bad)', excerpt="SCRAPED EXCERPT")
        item["title"] = "A [title] {% include secrets %}"
        item["link"] = reading.bookmark_url("https://example.com/a(b)")
        post = reading.render_post([item], self.start, self.end, self.now)
        self.assertNotIn("<script>", post)
        self.assertNotIn("{{", post)
        self.assertNotIn("{%", post)
        self.assertNotIn("SCRAPED EXCERPT", post)
        self.assertIn("a%28b%29", post)
        self.assertIn('weekly_reading_ids: ["1"]', post)

    def test_rejects_bad_urls_and_naive_dates(self):
        for url in ("javascript:alert(1)", "https://example.com/\nfoo", "not-a-link"):
            with self.assertRaises(ValueError):
                self.select([bookmark(link=url)])
        with self.assertRaisesRegex(ValueError, "timezone"):
            self.select([bookmark(created="2026-10-06T12:00:00")])

    def test_api_pagination(self):
        pages = [dict(result=True, items=[bookmark(i) for i in range(50)]), dict(result=True, items=[bookmark(50)])]
        responses = [io.BytesIO(json.dumps(page).encode()) for page in pages]
        with patch.object(reading, "urlopen", side_effect=responses) as opened:
            items = reading.fetch_bookmarks("dummy-token", "123")
        self.assertEqual(len(items), 51)
        self.assertIn("page=1", opened.call_args.args[0].full_url)

    def test_api_retry_and_authentication_failure(self):
        error = HTTPError("https://api.raindrop.io", 429, "limited", {"Retry-After": "1"}, None)
        response = io.BytesIO(b'{"result":true,"items":[]}')
        with patch.object(reading, "urlopen", side_effect=[error, response]), patch.object(reading.time, "sleep") as sleep:
            self.assertEqual(reading.fetch_bookmarks("dummy-token", "123"), [])
            sleep.assert_called_once_with(1)
        error = HTTPError("https://api.raindrop.io", 401, "unauthorized", {}, None)
        with patch.object(reading, "urlopen", side_effect=error), self.assertRaisesRegex(ValueError, "HTTP 401"):
            reading.fetch_bookmarks("dummy-token", "123")

    def test_dry_run_creation_ledger_and_idempotency(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            fixture = folder / "input.json"
            fixture.write_text(json.dumps([bookmark(note="My take")]))
            posts = folder / "posts"
            arguments = ["--input-json", str(fixture), "--posts-dir", str(posts), "--week-start", "2026-10-05", "--include-all"]
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(reading.main(arguments + ["--dry-run"]), 0)
                self.assertFalse(posts.exists())
                self.assertEqual(reading.main(arguments), 0)
                path = posts / "2026-10-11-weekly-reading.md"
                original = path.read_bytes()
                self.assertEqual(reading.published_entries(posts), ({"1"}, {"https://example.com/article"}))
                self.assertEqual(reading.main(arguments), 0)
                self.assertEqual(path.read_bytes(), original)
                # The next week cannot publish the same saved link again.
                arguments[arguments.index("2026-10-05")] = "2026-10-12"
                self.assertEqual(reading.main(arguments), 0)
                self.assertEqual(len(list(posts.glob("*.md"))), 1)

    def test_empty_week_writes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            fixture = folder / "input.json"
            fixture.write_text("[]")
            with contextlib.redirect_stderr(io.StringIO()):
                reading.main(["--input-json", str(fixture), "--posts-dir", str(folder / "posts")])
            self.assertFalse((folder / "posts").exists())


if __name__ == "__main__":
    unittest.main()
