# Scrape Method — Captions + Image URLs

How `TOP_10_POSTS.md` was built: captions/engagement from the existing `raw_jsonl/` dataset, image URLs fetched live via Jina Reader. No Instagram login, cookies, or browser automation involved in the image step.

## Step 1: Pull existing scraped metadata

The `raw_jsonl/` data in this repo was already collected by `scripts/scrape_accounts.py` (Instaloader, public metadata only, no login). To reuse it:

```bash
curl -s -o <account>.jsonl \
  "https://raw.githubusercontent.com/pocket-fund-2026/fashion-ig-analysis/main/raw_jsonl/<account>.jsonl"
```

Each line is one post:
```json
{"shortcode": "...", "date_utc": "...", "likes": 0, "comments": 0, "caption": "...", "hashtags": [...], "mentions": [...], "post_url": "..."}
```

## Step 2: Select top N posts per account

```python
posts.sort(key=lambda p: p["date_utc"], reverse=True)
top10 = posts[:10]
```

## Step 3: Fetch image URLs via Jina Reader

For each post's `post_url`, hit Jina's public read-proxy (server-rendered, logged-out, no session needed):

```bash
curl -s "https://r.jina.ai/https://www.instagram.com/p/<shortcode>/"
```

The response is Markdown containing image tags:
```
![Image 2: Photo by ...](https://scontent-*.cdninstagram.com/...)
```

Extract the first non-profile-picture image:
```python
import re
img_re = re.compile(r'!\[Image \d+: ([^\]]*)\]\((https://[^)]+cdninstagram\.com[^)]+)\)')
for alt, url in img_re.findall(text):
    if "profile picture" in alt.lower():
        continue
    image_url = url
    break
```

Throttle with `time.sleep(0.3)` between requests to stay polite.

**Note:** these are Instagram's signed CDN URLs — they carry an expiry token (`oe=` param) and will eventually stop resolving. Treat them as a point-in-time snapshot, not permanent links. Re-run this step to refresh.

## Step 4: Assemble and commit

Merge caption/engagement + fetched image URL into one Markdown block per post, grouped by account. Push via the GitHub Contents API (works well for single-file updates without a local clone):

```bash
gh auth switch --hostname github.com --user pocket-fund-2026
gh api repos/pocket-fund-2026/fashion-ig-analysis/contents/<file>.md \
  -X PUT --input payload.json
# payload.json = {"message": "...", "content": "<base64>", "branch": "main", "sha": "<existing sha, if updating>"}
```

## What did NOT work (tried first)

| Method | Result |
|---|---|
| Browser `sessionid` cookie + `insta-fetcher` (Android API) | Blocked — served a "not logged in" page when run from a different machine/network than the original browser session |
| `opencli instagram user` / `opencli instagram profile` (Chrome-extension browser automation) | Blocked reproducibly across every account tried — "Navigation rejected" or an HTML error page instead of JSON |
| `opencli instagram search` | Worked fine, but only returns account search results, not post/profile data |

**Why Jina Reader worked when the others didn't:** it never touches Instagram's authenticated app API — it fetches the public page HTML the way a search-engine crawler would, so there's no session/cookie/bot-detection surface to get blocked on.
