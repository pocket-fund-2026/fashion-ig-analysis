# Content Plan — What My Page Should Cover

A concrete plan synthesizing the driver-category evidence, the 10 reference accounts (5 global + 5 India-focused), and the whitespace research into an actual coverage strategy. This is a living plan — revisit and adjust it as `INSIGHTS.md` accumulates more weekly snapshots.

## 1. Positioning: pick a lane deliberately

Based on the 10 reference accounts, three viable positioning options exist. Pick one rather than blending:

| Positioning | Closest models | Tradeoff |
|---|---|---|
| **Fast-reaction news account** | @diet_prada, @stylenotcom | Highest per-post payoff, but requires being genuinely fast and monitoring constantly |
| **Personality-led video critic** | @sufimotiwala | Builds a loyal audience around a voice, not just content — but requires being comfortable on camera consistently |
| **Data/analysis creator with an owned audience** | @databutmakeitfashion | Slower IG growth, but builds a durable asset (newsletter/email list) instead of a platform-dependent following |

**Recommendation:** start as a fast-reaction account (lowest barrier to entry, matches the strongest proven driver — breaking news) while layering in one recurring personality-led or data-driven series per week to build a secondary identity beyond pure reactivity.

## 2. Core content pillars (by proven driver strength)

Ranked by the driver-category evidence in `INSIGHTS.md` / `fashion_ig_scraped_data.csv`:

1. **Breaking industry news** (death/tragedy, scandal/controversy, creative director moves) — the highest-performing category across every account studied. Cover this fast, always.
2. **Brand launch/drop coverage** — reliably above-baseline, plannable in advance since launch dates are usually known ahead of time.
3. **Whitespace stories** (see `WHITESPACE.md`) — original angles the 10 tracked accounts aren't covering: Rousteing/Rabanne follow-up, mass-market creative directors, Lagos Fashion Week/African fashion, resale economics, adaptive fashion, AI-campaign backlash.
4. **India-specific coverage gap**: none of the 5 original global accounts cover Indian fashion at all, and the 5 India-focused accounts skew toward Bollywood/celebrity styling or official fashion-week listings rather than data-driven analysis or accountability journalism — @dietsabya is the only Indian "watchdog" account and has no real analogue for data/trend-style coverage. **A data-driven or accountability-style account for Indian fashion specifically is closer to unclaimed territory than trying to out-compete the 5 established global accounts head-on.**
5. **Recurring low-cost formats** (from `CONTENT_IDEAS.md`): word/language-fatigue tracking, "real or repro" authenticity checks, then-vs-now heritage pairings, unsung-object spotlights — fill gaps between big news days without needing a news hook.

## 3. Weekly content cadence (starting template)

| Day | Content type | Source |
|---|---|---|
| Mon | Weekend recap / whatever broke over the weekend | Fast reaction, monitor over Sat–Sun |
| Tue | Recurring low-cost format (rotate: word autopsy / real-or-repro / heritage pairing) | `CONTENT_IDEAS.md` |
| Wed | Whitespace story (one of the 6 in `WHITESPACE.md`, or a fresh one found the same way) | `WHITESPACE.md` + live web research |
| Thu | Brand/launch coverage if anything's dropping this week | Monitor brand announcement calendars |
| Fri | Data/trend post (Google Trends check via `check_trends.py`) or a "this week in fashion" digest | `trends/` folder |
| As-it-happens | Any death/scandal/controversy — drop the schedule and post immediately | Fastest-reacting wins |

Adjust the specific days/formats as real posting data comes in — this is a starting hypothesis, not a fixed rule.

## 4. Sourcing checklist (per post)

Before posting, check:
- [ ] Is this the kind of story that historically performs? (Check `INSIGHTS.md`'s current driver-category rankings.)
- [ ] Has anyone in the 10 tracked accounts already covered this? (Check `fashion_ig_scraped_data.csv` — avoid being the 11th account posting the same thing unless adding a genuinely new angle.)
- [ ] Is there a properly licensed image available? (Official brand/press photos, Wikimedia Commons, Unsplash/Pexels — never repost the copyrighted campaign image itself, especially for AI-controversy or similar contested-content stories. See `WHITESPACE.md` for worked examples of safe vs. risky image sourcing.)
- [ ] Does the caption match a deliberately chosen voice, not a drifting mix of tones?

## 5. How this plan evolves

This isn't a one-time document. Each week:
1. `scripts/scrape_accounts.py` pulls fresh data from all 10 accounts.
2. `scripts/analyze_evolution.py` appends a new dated snapshot to `INSIGHTS.md`, showing what's rising/falling in each driver category and account, plus flags new candidate keywords for `categorize.py`.
3. Revisit this plan's cadence/pillars if `INSIGHTS.md` shows a sustained shift (e.g. a category consistently trending down, or a new one emerging) — the plan should track the evidence, not the other way around.
4. Re-run the whitespace research (live web search cross-checked against the growing dataset) periodically — gaps close over time as other accounts catch up, so new ones need to be found.
