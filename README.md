# Fashion IG Analysis

Scraped Instagram post data (metadata only — captions, engagement stats, hashtags, mentions, post URLs) for 10 fashion-commentary accounts.

**Original 5 (global, last 30 days as of Aug 24, 2026):**
- [@dietsabya](https://www.instagram.com/dietsabya)
- [@diet_prada](https://www.instagram.com/diet_prada)
- [@stylenotcom](https://www.instagram.com/stylenotcom)
- [@thefashionobserve](https://www.instagram.com/thefashionobserve)
- [@databutmakeitfashion](https://www.instagram.com/databutmakeitfashion)

**Added Aug 2026 — Indian fashion scene:**
- [@thevofashion](https://www.instagram.com/thevofashion/) — The Voice of Fashion, a digital magazine tracking Indian fashion/design/culture
- [@bollywood_fashionpolice](https://www.instagram.com/bollywood_fashionpolice/) — tabloid-style commentary on Bollywood celebrity fashion
- [@sufimotiwala](https://www.instagram.com/sufimotiwala/) — personality-led red-carpet rating Reels, honest/humor-driven celebrity style reviews
- [@indiarunwayweek](https://www.instagram.com/indiarunwayweek/) — official India Runway Week account, runway/collection coverage
- [@theindiastylefashionweek](https://www.instagram.com/theindiastylefashionweek/) — official account for India's national-level (Delhi NCR) fashion week

## Contents

- `fashion_ig_scraped_data.csv` / `.xlsx` — combined dataset, one row per post, with a per-account sheet in the Excel version. Columns: `account`, `post_url`, `date_utc`, `format`, `likes`, `comments`, `video_views`, `driver_category`, `caption`, `hashtags`, `mentions`.
- `raw_jsonl/` — raw scraped output per account (one JSON object per post, including a `post_url` field) plus each account's profile metadata (followers, following, bio) at time of scrape.
- `LINKS.md` — every single scraped post's direct Instagram link, grouped by account, with date/likes/comments for quick reference.

## Method

Collected with [Instaloader](https://instaloader.github.io/) (public metadata only, no login) via a custom Python script bounding results to the last 30 days per account. `driver_category` is a keyword-based classification of each post's likely engagement driver (e.g. death/tragedy, scandal/controversy, runway recap, brand launch), applied after the fact for analysis purposes.

No media (images/video) is included in this repo — data only.
