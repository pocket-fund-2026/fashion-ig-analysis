# Fashion IG Analysis

Scraped Instagram post data (metadata only — captions, engagement stats, hashtags, mentions, post URLs) for 11 fashion-focused accounts.

**Original 5 (global, last 30 days as of Aug 24, 2026):**
- [@dietsabya](https://www.instagram.com/dietsabya)
- [@diet_prada](https://www.instagram.com/diet_prada)
- [@stylenotcom](https://www.instagram.com/stylenotcom)
- [@thefashionobserve](https://www.instagram.com/thefashionobserve)
- [@databutmakeitfashion](https://www.instagram.com/databutmakeitfashion)

**Indian fashion scene (added Aug 2026, verified genuinely active and fashion-specific):**
- [@thevofashion](https://www.instagram.com/thevofashion/) — The Voice of Fashion, a digital magazine tracking Indian fashion/design/culture
- [@sufimotiwala](https://www.instagram.com/sufimotiwala/) — personality-led red-carpet rating Reels, honest/humor-driven celebrity style reviews
- [@elleindia](https://www.instagram.com/elleindia/) — Elle's official India edition
- [@fashioneditindia](https://www.instagram.com/fashioneditindia/) — tracking fashion, art & culture; global fashion, designers, people
- [@fashionrevolutionindia](https://www.instagram.com/fashionrevolutionindia/) — campaigning for a better fashion industry
- [@mallikasinghania](https://www.instagram.com/mallikasinghania/) — fashion/beauty/lifestyle, showcasing home-grown Indian designer wear

**Not currently scrapable:** 11 additional legitimate Indian fashion accounts (Vogue India, FDCI, Lakme Fashion Week, WWD India, and others) are blocked by a current Instagram API bug — see [`UNSCRAPABLE_ACCOUNTS.md`](./UNSCRAPABLE_ACCOUNTS.md) for the full list and technical explanation.

## Contents

- `fashion_ig_scraped_data.csv` / `.xlsx` — combined dataset, one row per post, with a per-account sheet in the Excel version. Columns: `account`, `post_url`, `date_utc`, `format`, `likes`, `comments`, `video_views`, `driver_category`, `caption`, `hashtags`, `mentions`.
- `raw_jsonl/` — raw scraped output per account (one JSON object per post, including a `post_url` field) plus each account's profile metadata (followers, following, bio) at time of scrape.
- `LINKS.md` — every single scraped post's direct Instagram link, grouped by account, with date/likes/comments for quick reference.

## Method

Collected with [Instaloader](https://instaloader.github.io/) (public metadata only, no login) via a custom Python script bounding results to the last 30 days per account. `driver_category` is a keyword-based classification of each post's likely engagement driver (e.g. death/tragedy, scandal/controversy, runway recap, brand launch), applied after the fact for analysis purposes.

No media (images/video) is included in this repo — data only.
