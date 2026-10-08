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

## GitHub Actions setup

The workflow is `.github/workflows/weekly-reading.yml`, named **Weekly reading
and site publishing**. Merge it to `main`, then set **Settings → Pages → Build and
deployment → Source** to **GitHub Actions**. Do not add a second suggested Pages
workflow. A deployment triggered by the merge may fail until this setting is
changed; run the workflow again after configuring Pages.

It runs Mondays at 8:17 a.m. Pacific, selecting the previous Monday–Sunday. Site
changes pushed to `main` also build and deploy, without generating a roundup.
Pull requests run generator tests without accessing Raindrop or deploying.

Under **Settings → Secrets and variables → Actions**, confirm `RAINDROP_TOKEN`
is a repository Secret and `RAINDROP_COLLECTION_ID` is a repository Variable.
The workflow passes these settings to the generator explicitly:

Pass your saved settings explicitly:

```yaml
- name: Generate weekly reading
  env:
    RAINDROP_TOKEN: ${{ secrets.RAINDROP_TOKEN }}
    RAINDROP_COLLECTION_ID: ${{ vars.RAINDROP_COLLECTION_ID }}
  run: python3 scripts/generate_weekly_reading.py
```

### First run

1. Add at least one link to the configured Raindrop collection.
2. Open **Actions → Weekly reading and site publishing → Run workflow**.
3. Select branch `main`, leave **Preview only** checked, and check **Include all
   unpublished links**. Optionally enter this week's Monday as **week_start** to
   label the first roundup with the current week.
4. Open the run's **build → Generate reading post** logs to inspect the Markdown.
   Preview runs write no post, make no commit, and skip site building/deployment.
5. Run again with the same inputs, but uncheck **Preview only**, to publish.
6. Wait for **validate**, **build**, and **deploy** to pass, then visit `/blog/`.

For normal scheduled runs, no manual inputs are needed. For a missed week, run
manually with its Monday date, preview unchecked, and include-all unchecked.

The workflow builds before committing the post. It commits only `docs/_posts`,
then explicitly uploads and deploys the site. If deployment fails after the
commit succeeds, rerun the workflow; the existing post is preserved and rebuilt.
If another commit reaches `main` while the job is running, its push may be
rejected; rerun on the latest `main`. GitHub's default token does not trigger
another push workflow, so the automated commit does not cause a publishing loop.

Raindrop HTTP 401 errors usually indicate an invalid token. A protected branch
that blocks the bot's direct commits requires a PR-based publishing approach.
The workflow's commit job explicitly requests `contents: write`; no personal
GitHub access token is needed. Scheduled jobs can be delayed, and public-repo
schedules are disabled after 60 days of repository inactivity.
