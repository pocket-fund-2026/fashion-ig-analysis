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
import random
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(REPO_ROOT, "scripts", "state.json")
RAW_DIR = os.path.join(REPO_ROOT, "raw_jsonl")
ACCOUNTS = [
    "dietsabya", "diet_prada", "stylenotcom", "thefashionobserve", "databutmakeitfashion",
    "thevofashion", "sufimotiwala", "fashioneditindia", "fashionrevolutionindia", "mallikasinghania",
    "brownfashiongal", "manifest.ind",
]

os.makedirs(RAW_DIR, exist_ok=True)


class GentleRateController(instaloader.RateController):
    """Adds a floor delay before every request so we stay well under
    Instagram's per-window thresholds instead of bursting until we hit a 429
    and relying on its backoff."""

    def query_waittime(self, query_type, current_time, untracked_queries=False):
        base = super().query_waittime(query_type, current_time, untracked_queries)
        return max(base, random.uniform(6, 10))


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
        rate_controller=lambda ctx: GentleRateController(ctx),
    )

    login_user = os.environ.get("IG_LOGIN_USER")
    if login_user:
        try:
            L.load_session_from_file(login_user)
            print(f"Loaded saved session for {login_user}", flush=True)
        except FileNotFoundError:
            print(
                f"No saved session for {login_user} — run "
                f"'.venv/bin/instaloader --login={login_user}' once first "
                f"to create one interactively.",
                flush=True,
            )
            return

    for username in ACCOUNTS:
        print(f"=== {username} ===", flush=True)
        acct_state = state.get(username, {})
        # default lookback: 8 days if we've never scraped this account before
        last_scraped_iso = acct_state.get("last_post_seen_at")
        if last_scraped_iso:
            cutoff = datetime.datetime.fromisoformat(last_scraped_iso).replace(tzinfo=None)
        else:
            # first-time backfill depth; override with e.g. BACKFILL_DAYS=30 for a deeper one-time pull
            backfill_days = int(os.environ.get("BACKFILL_DAYS", "8"))
            cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=backfill_days)

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
                time.sleep(random.uniform(1.5, 3.0))
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
        time.sleep(random.uniform(20, 35))

    print("SCRAPE_DONE")


if __name__ == "__main__":
    main()
