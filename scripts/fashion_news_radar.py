#!/usr/bin/env python3
"""
Fashion News Radar — pulls current listings from a fixed set of fashion
news/blog sites via Jina Reader (public read-proxy, no login/cookies),
scores each story for India-relevance + recency, and outputs a ranked
markdown + JSON digest.

Usage:
    python3 fashion_news_radar.py [--days 7] [--top 10] [--out OUT_PREFIX]

Rerunnable on demand — no state, no auth. Each site has its own extraction
pattern because listing pages are structured differently; if a site's HTML
changes, only that site's regex needs updating (see SITES below).
"""
import argparse
import json
import re
import time
import urllib.request
from datetime import datetime, timedelta

JINA_PREFIX = "https://r.jina.ai/"

SITES = {
    "fibre2fashion": "https://www.fibre2fashion.com/news/fashion-news/india",
    "fashionherald": "https://fashionherald.in",
    "vogue_india": "https://www.vogue.in/fashion",
    "fashionnetwork_india": "https://in.fashionnetwork.com",
    "azafashions_blog": "https://www.azafashions.com/blog/",
}

INDIA_KEYWORDS = [
    "india", "indian", "mumbai", "delhi", "bengaluru", "bangalore", "kolkata",
    "chennai", "hyderabad", "bollywood", "sari", "saree", "lehenga", "kurta",
    "paithani", "kanjeevaram", "kanchipuram", "banarasi", "zardozi", "kantha",
    "chikankari", "bandhani", "ikat", "ajrakh", "desi", "sabyasachi",
    "manish malhotra", "abu jani", "sandeep khosla", "jj valaya", "fabindia",
    "myntra", "arvind fashions", "peter england", "shoppers stop", "raymond",
    "nyfw india", "durga puja", "navratri", "diwali", "ambani", "kapoor",
    "bhatt", "chopra", "wedding", "bridal",
]

MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"


def fetch(url: str) -> str:
    req = urllib.request.Request(JINA_PREFIX + url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def parse_date(date_str: str):
    date_str = date_str.strip()
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%d %B %Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def extract_fibre2fashion(text):
    pat = re.compile(
        r"\[([^\]]{15,150})\]\((https://www\.fibre2fashion\.com/news/[a-z-]+/[^)]+newsdetails\.htm)\)\s*\n+\s*"
        rf"(({MONTHS}) \d{{1,2}}, \d{{4}})"
    )
    out, seen = [], set()
    for title, url, date, _ in pat.findall(text):
        if url in seen:
            continue
        seen.add(url)
        out.append({"title": title, "url": url, "date": parse_date(date)})
    return out


def extract_fashionherald(text):
    # Links are nested: [![alt](img-url) Title Text](article-url)
    pat = re.compile(
        r"\[!\[[^\]]*\]\([^)]*\)\s*([^\[\]]{10,180})\]\((https://fashionherald\.in/(?!wp-content|category)[a-z0-9-]+/)\)"
    )
    out, seen = [], set()
    for title, url in pat.findall(text):
        if url in seen:
            continue
        seen.add(url)
        out.append({"title": title.strip(), "url": url, "date": None})  # listing only shows relative age
    return out


def extract_vogue(text):
    pat = re.compile(
        rf"(\d{{1,2}} (?:{MONTHS.replace('|', '|').replace('Jan', 'January').replace('Feb', 'February').replace('Mar', 'March').replace('Apr', 'April').replace('Jun', 'June').replace('Jul', 'July').replace('Aug', 'August').replace('Sep', 'September').replace('Oct', 'October').replace('Nov', 'November').replace('Dec', 'December')}) \d{{4}})"
        r"[\s\S]{0,400}?## \[([^\]]{10,150})\]\((https://www\.vogue\.in/content/[^)]+)\)"
    )
    out, seen = [], set()
    for date, title, url in pat.findall(text):
        if url in seen:
            continue
        seen.add(url)
        out.append({"title": title, "url": url, "date": parse_date(date)})
    return out


def extract_fashionnetwork(text):
    pat = re.compile(r"### \[([^\]]{10,180})\]\((https://in\.fashionnetwork\.com/news/[^)]+)\)")
    out, seen = [], set()
    for title, url in pat.findall(text):
        if url in seen:
            continue
        seen.add(url)
        out.append({"title": title, "url": url, "date": None})  # needs per-article fetch for date
    return out


def extract_aza(text):
    pat = re.compile(
        rf"(({MONTHS.replace('Jan','January').replace('Feb','February').replace('Mar','March').replace('Apr','April').replace('Jun','June').replace('Jul','July').replace('Aug','August').replace('Sep','September').replace('Oct','October').replace('Nov','November').replace('Dec','December')}) \d{{1,2}}, \d{{4}})"
        r"[\s\S]{0,300}?#### \[([^\]]{10,150})\]\((https://www\.azafashions\.com/blog/[a-z0-9-]+/)"
    )
    out, seen = [], set()
    for date, _, title, url in pat.findall(text):
        if url in seen:
            continue
        seen.add(url)
        out.append({"title": title, "url": url, "date": parse_date(date)})
    return out


EXTRACTORS = {
    "fibre2fashion": extract_fibre2fashion,
    "fashionherald": extract_fashionherald,
    "vogue_india": extract_vogue,
    "fashionnetwork_india": extract_fashionnetwork,
    "azafashions_blog": extract_aza,
}


def india_score(title: str) -> int:
    t = title.lower()
    return sum(1 for kw in INDIA_KEYWORDS if kw in t)


def run(days: int, top_n: int, out_prefix: str):
    cutoff = datetime.now() - timedelta(days=days)
    all_items = []

    for site, url in SITES.items():
        try:
            text = fetch(url)
        except Exception as e:
            print(f"[{site}] fetch failed: {e}")
            continue
        items = EXTRACTORS[site](text)
        for it in items:
            it["site"] = site
            it["india_score"] = india_score(it["title"])
            in_window = it["date"] is not None and it["date"] >= cutoff
            it["recent"] = in_window
        all_items.extend(items)
        print(f"[{site}] {len(items)} items extracted")
        time.sleep(0.3)

    # Rank: recent + india-relevant first, then india-relevant undated, then rest
    def sort_key(it):
        return (
            0 if it["recent"] else (1 if it["date"] is None else 2),
            -it["india_score"],
            -(it["date"].timestamp() if it["date"] else 0),
        )

    ranked = sorted(all_items, key=sort_key)
    top = ranked[:top_n]

    md = [f"# Fashion News Radar — India Focus\n",
          f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}. Window: last {days} days where a date was available; undated listing items ranked below dated recent ones.\n"]
    for i, it in enumerate(top, 1):
        date_str = it["date"].strftime("%Y-%m-%d") if it["date"] else "date unknown"
        tag = "RECENT" if it["recent"] else ("UNDATED" if it["date"] is None else "OLDER")
        md.append(f"{i}. **[{it['title']}]({it['url']})**  \n   _{it['site']} | {date_str} | india_score={it['india_score']} | {tag}_\n")

    with open(f"{out_prefix}.md", "w") as f:
        f.write("\n".join(md))

    with open(f"{out_prefix}.json", "w") as f:
        json.dump(
            [{**it, "date": it["date"].isoformat() if it["date"] else None} for it in ranked],
            f, indent=2,
        )

    print(f"\nWrote {out_prefix}.md and {out_prefix}.json — top {len(top)} of {len(all_items)} total items")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--out", type=str, default="news_radar")
    args = ap.parse_args()
    run(args.days, args.top, args.out)
