# Fashion IG Analysis

Scraped Instagram post data (metadata only — captions, engagement stats, hashtags, mentions, post URLs) for **9 actively-scraped fashion-focused accounts**.

**Original 5 (global, last 30 days as of Aug 24, 2026):**
- [@dietsabya](https://www.instagram.com/dietsabya)
- [@diet_prada](https://www.instagram.com/diet_prada)
- [@stylenotcom](https://www.instagram.com/stylenotcom)
- [@thefashionobserve](https://www.instagram.com/thefashionobserve)
- [@databutmakeitfashion](https://www.instagram.com/databutmakeitfashion)

**Indian fashion scene — 4 actively scraped (added Aug 2026, verified genuinely active and fashion-specific):**
- [@thevofashion](https://www.instagram.com/thevofashion/) — The Voice of Fashion, a digital magazine tracking Indian fashion/design/culture
- [@sufimotiwala](https://www.instagram.com/sufimotiwala/) — originally identified via web research as a red-carpet-rating fashion critic, but **the actual scraped posts (Aug 2026) show his top content is personal-life posts tied to his run on the reality show "Lock Upp: Sach Ya Sazaa," not fashion commentary** (see `CONTENT_IDEAS.md` for detail). Kept in the dataset for now, but not a reliable fashion-critique reference until his content mix shifts back.
- [@fashioneditindia](https://www.instagram.com/fashioneditindia/) — tracking fashion, art & culture; global fashion, designers, people
- [@fashionrevolutionindia](https://www.instagram.com/fashionrevolutionindia/) — campaigning for a better fashion industry (0 posts in the current 30-day window — its last post fell just outside the cutoff; expected to populate on the next weekly run)
- [@mallikasinghania](https://www.instagram.com/mallikasinghania/) — fashion/beauty/lifestyle, showcasing home-grown Indian designer wear

**Found but NOT actively scraped:**
- [@elleindia](https://www.instagram.com/elleindia/) — Elle's official India edition. Verified real/active/fashion-specific, but has an unusually high posting volume (multiple times/day) that made a 30-day Instaloader backfill too slow to complete reliably. Excluded from the pipeline for now — not a quality issue, just a throughput one. Could be revisited with a shorter lookback window (e.g. 7 days instead of 30) if wanted.

**Not currently scrapable:** 11 additional legitimate Indian fashion accounts (Vogue India, FDCI, Lakme Fashion Week, WWD India, and others) are blocked by a current Instagram API bug — see [`UNSCRAPABLE_ACCOUNTS.md`](./UNSCRAPABLE_ACCOUNTS.md) for the full list and technical explanation.

## Contents

- `fashion_ig_scraped_data.csv` / `.xlsx` — combined dataset, one row per post, with a per-account sheet in the Excel version. Columns: `account`, `post_url`, `date_utc`, `format`, `likes`, `comments`, `video_views`, `driver_category`, `caption`, `hashtags`, `mentions`.
- `raw_jsonl/` — raw scraped output per account (one JSON object per post, including a `post_url` field) plus each account's profile metadata (followers, following, bio) at time of scrape.
- `LINKS.md` — every single scraped post's direct Instagram link, grouped by account, with date/likes/comments for quick reference.

## Method

Collected with [Instaloader](https://instaloader.github.io/) (public metadata only, no login) via a custom Python script bounding results to the last 30 days per account. `driver_category` is a keyword-based classification of each post's likely engagement driver (e.g. death/tragedy, scandal/controversy, runway recap, brand launch), applied after the fact for analysis purposes.

No media (images/video) is included in this repo — data only.
