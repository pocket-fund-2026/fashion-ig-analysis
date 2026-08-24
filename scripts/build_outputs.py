"""
Rebuild the combined CSV/Excel dataset and LINKS.md from everything in raw_jsonl/.

Run from the repo root: python3 scripts/build_outputs.py
"""
import json
import os
import sys

import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(REPO_ROOT, "raw_jsonl")
ACCOUNTS = [
    "dietsabya", "diet_prada", "stylenotcom", "thefashionobserve", "databutmakeitfashion",
    "thevofashion", "sufimotiwala", "fashioneditindia", "fashionrevolutionindia", "mallikasinghania",
]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from categorize import categorize  # noqa: E402


def main():
    all_rows = []
    sheets = {}
    links_lines = ["# All Scraped Post Links\n", "Every post scraped in this dataset, grouped by account, newest first.\n"]

    for acc in ACCOUNTS:
        path = os.path.join(RAW_DIR, f"{acc}.jsonl")
        if not os.path.exists(path):
            continue
        posts = [json.loads(l) for l in open(path)]
        rows = []
        for p in posts:
            row = {
                "account": acc,
                "post_url": p.get("post_url") or f"https://www.instagram.com/p/{p['shortcode']}/",
                "date_utc": p["date_utc"][:19].replace("T", " "),
                "format": "Video" if p["is_video"] else "Image/Carousel",
                "likes": p["likes"] if p["likes"] is not None and p["likes"] >= 0 else None,
                "comments": p["comments"],
                "video_views": p.get("video_view_count"),
                "driver_category": categorize(p["caption"]),
                "caption": p["caption"],
                "hashtags": ", ".join(p["hashtags"]) if p["hashtags"] else "",
                "mentions": ", ".join(p["mentions"]) if p["mentions"] else "",
            }
            rows.append(row)
            all_rows.append(row)
        df = pd.DataFrame(rows).drop_duplicates(subset=["post_url"]).sort_values("date_utc", ascending=False)
        sheets[acc] = df

        links_lines.append(f"\n## @{acc} ({len(df)} posts)\n")
        for _, r in df.iterrows():
            likes = r["likes"] if pd.notna(r["likes"]) else "hidden"
            links_lines.append(f"- [{r['date_utc'][:10]}]({r['post_url']}) — {likes} likes, {r['comments']} comments")

    combined = pd.DataFrame(all_rows).drop_duplicates(subset=["post_url"]).sort_values(
        ["account", "date_utc"], ascending=[True, False]
    )

    csv_path = os.path.join(REPO_ROOT, "fashion_ig_scraped_data.csv")
    xlsx_path = os.path.join(REPO_ROOT, "fashion_ig_scraped_data.xlsx")
    links_path = os.path.join(REPO_ROOT, "LINKS.md")

    combined.to_csv(csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        combined.to_excel(writer, sheet_name="All_Accounts_Combined", index=False)
        for acc, df in sheets.items():
            df.to_excel(writer, sheet_name=acc[:31], index=False)
    with open(links_path, "w") as f:
        f.write("\n".join(links_lines) + "\n")

    print(f"Rebuilt outputs: {len(combined)} total posts across {len(sheets)} accounts")


if __name__ == "__main__":
    main()
