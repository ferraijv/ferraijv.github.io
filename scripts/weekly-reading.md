# Weekly reading generator

Requires Python 3.9+ with the America/Los_Angeles timezone available. Uses only the
standard library; no additional packages or AI API key are needed.

## Credentials

The script reads `RAINDROP_TOKEN` and `RAINDROP_COLLECTION_ID` from its environment.
GitHub repository Secrets and Variables are available to an Actions workflow only
when explicitly passed to the script's environment. They do not appear in your
local terminal automatically. Do not commit the token.

For a local preview, enter the token without displaying it (zsh on macOS):

```zsh
read -rs 'RAINDROP_TOKEN?Raindrop token: '
export RAINDROP_TOKEN
read 'RAINDROP_COLLECTION_ID?Collection ID: '
export RAINDROP_COLLECTION_ID
python3 scripts/generate_weekly_reading.py --include-all --dry-run
unset RAINDROP_TOKEN
```

## Generate posts

Run from the repository root:

```sh
# Preview the previous Monday–Sunday without changing files.
python3 scripts/generate_weekly_reading.py --dry-run

# Write the previous week's post to docs/_posts/.
python3 scripts/generate_weekly_reading.py

# First-run preview: include all saved, unpublished links, including this week.
python3 scripts/generate_weekly_reading.py --include-all --dry-run

# Backfill or retry a specific completed week (date must be a Monday).
python3 scripts/generate_weekly_reading.py --week-start 2026-10-05
```

The default week is the previous completed calendar week in Pacific time,
including daylight saving changes. Selection uses the bookmark's `created` time
(when saved to Raindrop), not the article's publication date. Save links after
reading them. Moving an old bookmark into this collection does not reset its save
date. Empty weeks produce no file.

Posts contain linked titles and the user's Raindrop `note`. Automatically scraped
`excerpt` text is not included. Notes are rendered as plain text with whitespace
collapsed; HTML, Markdown, and Liquid syntax are displayed literally.

The filename uses the week's Sunday, while the Jekyll `date` records the actual
generation time. Each post stores `weekly_reading_ids` and `weekly_reading_urls`
as tracking fields in its front matter. Keep those fields when editing a post.
All generated posts in the output directory are scanned for duplicate IDs and
exact URLs. Tracking parameters are not removed; differently written URLs may
still refer to the same article.

An existing week's post is never overwritten or appended to. If you add another
link after that week was generated, edit the post yourself or deliberately remove
the generated post and regenerate that week. `--include-all` is an explicit
first-run/backlog option: it bypasses date filtering for nonfuture saves and uses
an introduction explaining the broader selection. Do not use it in the normal
weekly schedule. Missed weeks can be backfilled with `--week-start`.

## Offline test

`--input-json PATH` reads a Raindrop API response (`{"items": [...]}`) or a bookmark
array instead of calling the API. Entries need `_id`, `created`, `link`, and
optionally `title` and `note`.

```sh
python3 scripts/generate_weekly_reading.py --input-json /tmp/reading.json --include-all --dry-run
python3 -m unittest discover -s tests -p 'test_weekly_reading.py' -v
```

Exit code 0 means generated, previewed, or nothing to do. Invalid data and API
failures return 1. Markdown previews go to stdout; preview/skip diagnostics go to
stderr. The script never changes Raindrop bookmarks, commits files, or deploys
the site. Those are the next workflow step.

## Future GitHub Actions invocation

Pass your saved settings explicitly:

```yaml
- name: Generate weekly reading
  env:
    RAINDROP_TOKEN: ${{ secrets.RAINDROP_TOKEN }}
    RAINDROP_COLLECTION_ID: ${{ vars.RAINDROP_COLLECTION_ID }}
  run: python3 scripts/generate_weekly_reading.py
```

The workflow must commit generated posts so later runs retain duplicate tracking,
then explicitly build and deploy Pages. If deployment fails after committing,
retry deployment from that commit; the generator will skip the existing post.
