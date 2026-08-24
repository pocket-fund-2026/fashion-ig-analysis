"""
Weekly incremental Instagram scrape.

Reads scripts/state.json for the last-seen post timestamp per account, pulls
only posts newer than that via Instaloader (public metadata + no login),
appends new records to raw_jsonl/<account>.jsonl (de-duplicated by shortcode),
and updates state.json with the newest timestamp seen this run.

Run from the repo root: python3 scripts/scrape_accounts.py
"""
import instaloader
import datetime
import json
import os
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(REPO_ROOT, "scripts", "state.json")
RAW_DIR = os.path.join(REPO_ROOT, "raw_jsonl")
ACCOUNTS = [
    "dietsabya", "diet_prada", "stylenotcom", "thefashionobserve", "databutmakeitfashion",
    "thevofashion", "bollywood_fashionpolice", "sufimotiwala", "indiarunwayweek", "theindiastylefashionweek",
]

os.makedirs(RAW_DIR, exist_ok=True)


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def load_existing_shortcodes(path):
    seen = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                try:
                    seen.add(json.loads(line)["shortcode"])
                except Exception:
                    pass
    return seen


def main():
    state = load_state()
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        quiet=True,
    )

    for username in ACCOUNTS:
        print(f"=== {username} ===", flush=True)
        acct_state = state.get(username, {})
        # default lookback: 8 days if we've never scraped this account before
        last_scraped_iso = acct_state.get("last_post_seen_at")
        if last_scraped_iso:
            cutoff = datetime.datetime.fromisoformat(last_scraped_iso).replace(tzinfo=None)
        else:
            cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=8)

        raw_path = os.path.join(RAW_DIR, f"{username}.jsonl")
        seen_shortcodes = load_existing_shortcodes(raw_path)

        try:
            profile = instaloader.Profile.from_username(L.context, username)
        except Exception as e:
            print(f"FAILED to load profile {username}: {e}", flush=True)
            continue

        new_records = []
        newest_seen = cutoff
        consecutive_old = 0
        try:
            for post in profile.get_posts():
                if post.date_utc <= cutoff:
                    consecutive_old += 1
                    if consecutive_old >= 6:
                        break
                    continue
                consecutive_old = 0
                if post.date_utc > newest_seen:
                    newest_seen = post.date_utc
                if post.shortcode in seen_shortcodes:
                    continue
                rec = {
                    "shortcode": post.shortcode,
                    "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "date_utc": post.date_utc.isoformat(),
                    "likes": post.likes,
                    "comments": post.comments,
                    "video_view_count": post.video_view_count if post.is_video else None,
                    "is_video": post.is_video,
                    "typename": post.typename,
                    "caption": post.caption or "",
                    "hashtags": post.caption_hashtags,
                    "mentions": post.caption_mentions,
                    "tagged_users": list(post.tagged_users) if post.tagged_users else [],
                    "accessibility_caption": post.accessibility_caption,
                }
                new_records.append(rec)
                time.sleep(0.5)
        except Exception as e:
            print(f"ERROR during iteration for {username}: {e}", flush=True)

        if new_records:
            with open(raw_path, "a") as f:
                for r in new_records:
                    f.write(json.dumps(r) + "\n")
        print(f"{username}: {len(new_records)} new posts since {cutoff.isoformat()}", flush=True)

        state[username] = {
            "last_run_at": datetime.datetime.utcnow().isoformat(),
            "last_post_seen_at": newest_seen.isoformat(),
            "new_posts_last_run": len(new_records),
        }
        save_state(state)
        time.sleep(2)

    print("SCRAPE_DONE")


if __name__ == "__main__":
    main()
