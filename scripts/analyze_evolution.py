"""
Turns the accumulated dataset into a running intelligence log instead of a static report.

Each run:
1. Computes current driver-category and per-account performance from ALL data in raw_jsonl/.
2. Compares against the last recorded snapshot (scripts/insights_history.json) to surface
   what changed since last time (rising/falling categories, new accounts, coverage gaps).
3. Extracts the most common meaningful words in this run's top-quartile posts (by likes) as
   a cheap signal for "language that's currently working."
4. Flags the most frequent words appearing in still-uncategorized captions, as candidate
   keywords to add to categorize.py's THEMES list next time it's edited.
5. Appends (never overwrites) a new dated section to INSIGHTS.md and records the new
   snapshot in insights_history.json, so the log actually accumulates understanding over time.

Run from the repo root: python3 scripts/analyze_evolution.py
"""
import collections
import datetime
import json
import os
import re
import sys

import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(REPO_ROOT, "raw_jsonl")
HISTORY_PATH = os.path.join(REPO_ROOT, "scripts", "insights_history.json")
INSIGHTS_PATH = os.path.join(REPO_ROOT, "INSIGHTS.md")
ACCOUNTS = [
    "dietsabya", "diet_prada", "stylenotcom", "thefashionobserve", "databutmakeitfashion",
    "thevofashion", "bollywood_fashionpolice", "sufimotiwala", "indiarunwayweek", "theindiastylefashionweek",
]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from categorize import categorize  # noqa: E402

STOPWORDS = set(
    "the a an and or but of to in on for with is are was were be been being this that "
    "it its as at by from up out so if then than not no yes just also very really "
    "u ur im its it's dont don't we our you your they their he she his her rn tho "
    "have has had do does did can could would should will".split()
)


def load_all_posts():
    posts = []
    for acc in ACCOUNTS:
        path = os.path.join(RAW_DIR, f"{acc}.jsonl")
        if not os.path.exists(path):
            continue
        for line in open(path):
            try:
                p = json.loads(line)
            except Exception:
                continue
            p["account"] = acc
            p["driver_category"] = categorize(p.get("caption", ""))
            posts.append(p)
    return posts


def top_words(captions, n=15):
    counter = collections.Counter()
    for c in captions:
        words = re.findall(r"[a-zA-Z']+", (c or "").lower())
        for w in words:
            if len(w) > 3 and w not in STOPWORDS:
                counter[w] += 1
    return counter.most_common(n)


def load_history():
    if os.path.exists(HISTORY_PATH):
        return json.load(open(HISTORY_PATH))
    return []


def save_history(history):
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def main():
    posts = load_all_posts()
    likeable = [p for p in posts if p.get("likes") is not None and p["likes"] >= 0]
    if not likeable:
        print("No data to analyze yet.")
        return

    overall_avg = sum(p["likes"] for p in likeable) / len(likeable)

    cat_stats = collections.defaultdict(list)
    for p in likeable:
        cat_stats[p["driver_category"]].append(p["likes"])
    cat_avgs = {c: sum(v) / len(v) for c, v in cat_stats.items()}

    acct_stats = collections.defaultdict(list)
    for p in likeable:
        acct_stats[p["account"]].append(p["likes"])
    acct_avgs = {a: sum(v) / len(v) for a, v in acct_stats.items()}

    uncategorized_pct = 100 * sum(1 for p in posts if p["driver_category"] == "Uncategorized/other") / len(posts)
    uncategorized_words = top_words(
        [p["caption"] for p in posts if p["driver_category"] == "Uncategorized/other"], n=15
    )

    sorted_likes = sorted(p["likes"] for p in likeable)
    q3_idx = int(len(sorted_likes) * 0.75)
    q3_threshold = sorted_likes[q3_idx] if sorted_likes else 0
    top_quartile_captions = [p["caption"] for p in likeable if p["likes"] >= q3_threshold]
    winning_words = top_words(top_quartile_captions, n=15)

    history = load_history()
    prev = history[-1] if history else None

    today = datetime.date.today().isoformat()
    lines = [f"\n## Snapshot: {today}\n"]
    lines.append(f"Total posts in dataset: **{len(posts)}** across {len(acct_avgs)} active accounts. "
                 f"Overall avg likes: **{overall_avg:,.0f}**. Uncategorized: **{uncategorized_pct:.1f}%**.\n")

    lines.append("### Driver category performance (all-time, this run)")
    for cat, avg in sorted(cat_avgs.items(), key=lambda x: -x[1]):
        n = len(cat_stats[cat])
        delta = ""
        if prev and cat in prev.get("cat_avgs", {}):
            prev_avg = prev["cat_avgs"][cat]
            pct = 100 * (avg - prev_avg) / prev_avg if prev_avg else 0
            arrow = "▲" if pct > 5 else ("▼" if pct < -5 else "→")
            delta = f" {arrow} {pct:+.0f}% vs last snapshot"
        elif prev:
            delta = " (new category since last snapshot)"
        lines.append(f"- **{cat}**: n={n}, avg likes={avg:,.0f}{delta}")

    lines.append("\n### Account performance (all-time, this run)")
    for acc, avg in sorted(acct_avgs.items(), key=lambda x: -x[1]):
        n = len(acct_stats[acc])
        delta = ""
        if prev and acc in prev.get("acct_avgs", {}):
            prev_avg = prev["acct_avgs"][acc]
            pct = 100 * (avg - prev_avg) / prev_avg if prev_avg else 0
            arrow = "▲" if pct > 5 else ("▼" if pct < -5 else "→")
            delta = f" {arrow} {pct:+.0f}% vs last snapshot"
        elif prev:
            delta = " (new account since last snapshot)"
        lines.append(f"- **@{acc}**: n={n}, avg likes={avg:,.0f}{delta}")

    lines.append("\n### Language currently working (top-quartile posts by likes)")
    lines.append(", ".join(f"{w} ({c})" for w, c in winning_words))

    if uncategorized_words:
        lines.append("\n### Candidate keywords to add to `categorize.py` (frequent in still-uncategorized posts)")
        lines.append(", ".join(f"{w} ({c})" for w, c in uncategorized_words))

    with open(INSIGHTS_PATH, "a") as f:
        f.write("\n".join(lines) + "\n")

    history.append({
        "date": today,
        "total_posts": len(posts),
        "overall_avg_likes": overall_avg,
        "uncategorized_pct": uncategorized_pct,
        "cat_avgs": cat_avgs,
        "acct_avgs": acct_avgs,
    })
    save_history(history)

    print(f"Appended snapshot for {today} to INSIGHTS.md ({len(posts)} total posts, "
          f"{uncategorized_pct:.1f}% uncategorized)")


if __name__ == "__main__":
    main()
