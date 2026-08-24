# Weekly Update Pipeline

Run in this order (from the repo root):

```bash
pip install -r scripts/requirements.txt
python3 scripts/scrape_accounts.py    # 1. incremental scrape, updates scripts/state.json
python3 scripts/check_trends.py       # 2. Google Trends snapshot -> trends/trends_<date>.csv
python3 scripts/build_outputs.py      # 3. rebuild CSV/Excel/LINKS.md from raw_jsonl/
```

Then review the newly scraped posts (the counts printed by `scrape_accounts.py`, or diff `raw_jsonl/*.jsonl`), refresh `CONTENT_IDEAS.md` with fresh suggestions drawn from that week's top posts, and commit everything:

```bash
git add -A
git commit -m "Weekly update: $(date -u +%Y-%m-%d)"
git push
```

## State tracking

`scripts/state.json` records, per account, the timestamp of the newest post seen so far. Each run of `scrape_accounts.py` only pulls posts newer than that, so re-running never re-downloads or duplicates existing posts (also de-duplicated by shortcode as a second safety net). New accounts added to `ACCOUNTS` with no existing state default to an 8-day lookback on their first run.

## Tracked accounts (10)

Original 5 (global): `dietsabya`, `diet_prada`, `stylenotcom`, `thefashionobserve`, `databutmakeitfashion`

Added Aug 2026 — Indian fashion scene: `thevofashion`, `bollywood_fashionpolice`, `sufimotiwala`, `indiarunwayweek`, `theindiastylefashionweek`

## Known issues

- **`theindiastylefashionweek`** currently fails to load with `400 Bad Request - "Asset asset://laser.provider/ig_business_category_subvertical has been deleted"` from Instagram's profile API — reproduced consistently across multiple runs (Aug 24, 2026), so likely an account-type/schema incompatibility with this Instaloader version rather than a transient error. Left in the `ACCOUNTS` list so it retries automatically if Instagram/Instaloader resolve it; check `scripts/state.json` (absence of an entry means it's never successfully scraped) before assuming it's working.
- **`bollywood_fashionpolice`** and **`indiarunwayweek`** returned 0 posts on their first (8-day lookback) run — either they simply haven't posted recently, or worth spot-checking manually if this persists for multiple weekly runs.

## Notes

- No login is used — only public post metadata is pulled (captions, likes, comments, hashtags, mentions, timestamps). No images/video are downloaded by this pipeline.
- `check_trends.py` uses the unofficial `pytrends` library against Google Trends. It can be rate-limited, especially from shared/cloud IPs — a failed run just skips that week's trend snapshot rather than failing the whole pipeline.
- `categorize.py` holds the shared keyword-based driver-category classifier used by both `build_outputs.py` and (optionally) manual content-idea generation.
