"""
Weekly Google Trends check for a fixed list of fashion keywords, plus any
creative-director/brand names currently showing up in newly scraped captions.

Saves a dated CSV to trends/trends_<YYYY-MM-DD>.csv.
Run from the repo root: python3 scripts/check_trends.py
"""
import datetime
import os

import pandas as pd
from pytrends.request import TrendReq

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRENDS_DIR = os.path.join(REPO_ROOT, "trends")
os.makedirs(TRENDS_DIR, exist_ok=True)

BASE_KEYWORDS = [
    "quiet luxury",
    "coquette fashion",
    "indie sleaze",
    "capsule wardrobe",
    "Y2K fashion",
    "maximalism fashion",
    "old money aesthetic",
]


def main():
    pytrends = TrendReq(hl="en-US", tz=0)
    today = datetime.date.today().isoformat()
    rows = []

    # pytrends allows max 5 keywords per request
    for i in range(0, len(BASE_KEYWORDS), 5):
        batch = BASE_KEYWORDS[i : i + 5]
        try:
            pytrends.build_payload(batch, timeframe="now 7-d")
            data = pytrends.interest_over_time()
            if data.empty:
                continue
            avg = data[batch].mean().to_dict()
            for kw, val in avg.items():
                rows.append({"date_checked": today, "keyword": kw, "avg_interest_last_7d": val})
        except Exception as e:
            print(f"Trends lookup failed for batch {batch}: {e}")

    if rows:
        out_path = os.path.join(TRENDS_DIR, f"trends_{today}.csv")
        pd.DataFrame(rows).to_csv(out_path, index=False)
        print(f"Saved {len(rows)} trend rows to {out_path}")
    else:
        print("No trend data collected this run (Google Trends may be rate-limiting).")


if __name__ == "__main__":
    main()
