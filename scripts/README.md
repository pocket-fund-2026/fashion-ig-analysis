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

`scripts/state.json` records, per account, the timestamp of the newest post seen so far. Each run of `scrape_accounts.py` only pulls posts newer than that, so re-running never re-downloads or duplicates existing posts (also de-duplicated by shortcode as a second safety net).

## Notes

- No login is used — only public post metadata is pulled (captions, likes, comments, hashtags, mentions, timestamps). No images/video are downloaded by this pipeline.
- `check_trends.py` uses the unofficial `pytrends` library against Google Trends. It can be rate-limited, especially from shared/cloud IPs — a failed run just skips that week's trend snapshot rather than failing the whole pipeline.
- `categorize.py` holds the shared keyword-based driver-category classifier used by both `build_outputs.py` and (optionally) manual content-idea generation.
