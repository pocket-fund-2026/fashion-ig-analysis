# SOUL.md — Why This Exists

## What this actually is

This repo is the research foundation for launching a new fashion-commentary Instagram account. It's not just "scraped data" — it's a working answer to the question *"what actually makes a fashion account succeed, and where is there room for a new one?"*, built from real evidence instead of guesswork.

## Why I'm doing this

Anyone can start a fashion Instagram account and post about runway shows and hope it works. That's not a strategy — it's a bet. Before spending time building a page, publishing content, and trying to grow an audience, it's worth actually knowing:

- What kind of fashion content already gets traction, and why
- Which accounts are already dominating which lanes, so effort isn't wasted competing head-on where five other accounts already win
- Where there's real, current, uncovered ground — so the new account has something to actually own from day one instead of blending in

This project answers all three by treating five established fashion accounts as a dataset instead of just scrolling them.

## What it's actually doing, mechanically

1. **Scraping** — pulling real post data (likes, comments, views, captions, hashtags, timestamps) from 5 fashion-commentary Instagram accounts (@dietsabya, @diet_prada, @stylenotcom, @thefashionobserve, @databutmakeitfashion) using Instaloader, no login required, public data only.
2. **Categorizing** — tagging every post with what likely drove its engagement (death/tragedy, scandal, creative director news, runway recap, brand launch, etc.) so patterns become visible instead of anecdotal.
3. **Measuring** — comparing average engagement across categories, formats (video vs. image), and accounts to find out what's actually true, not what's assumed to be true (e.g. the surprising finding that these accounts' branded "content pillars" often underperform compared to reactive breaking-news posts).
4. **Finding whitespace** — going beyond the 5 accounts to the live web to find real, current fashion stories none of them are covering, so a new account has an original angle instead of a copy of an existing one.
5. **Repeating weekly** — an automated pipeline re-scrapes, re-checks Google Trends, and regenerates fresh content ideas every week, so this stays a living research base instead of a one-time snapshot that goes stale.

## How this is meant to be used

- **Before posting anything**, check `WHITESPACE.md` and `CONTENT_IDEAS.md` for angles that are proven-to-work *and* currently uncovered — that's the highest-leverage starting point.
- **When deciding on voice/format**, read `README.md`'s account summaries — five very different working models (anonymous tabloid, first-person data-analyst, high-volume aggregator, etc.) already exist as reference points; pick traits deliberately instead of drifting into whichever voice feels natural.
- **When something in fashion news breaks**, check the driver-category data (`fashion_ig_scraped_data.csv`) to gut-check whether it's the kind of story that tends to perform (death/tragedy, scandal, creative-director shakeups) before deciding how much effort to put into covering it fast.
- **Every week**, the pipeline (`scripts/`) adds fresh data automatically — treat `CONTENT_IDEAS.md` as a living planning document, not a one-time deliverable, and revisit it each week before planning that week's posts.
- **When the new account starts posting its own content**, its own performance data can eventually be added back into this same structure — turning this from "research about other people's accounts" into "an ongoing feedback loop for my own."

## The honest caveat

This tells you what *worked for these five accounts, recently*. It doesn't guarantee anything transfers directly — audiences, algorithms, and news cycles shift. Treat this as a strong starting hypothesis to test quickly, not a formula to follow blindly. The fastest way to find out if any of this actually works is to post, watch what happens, and feed those results back in.
