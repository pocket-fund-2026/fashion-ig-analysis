# Unscrapable Accounts — Known Instagram API Issue

These are real, legitimate fashion-industry Instagram accounts identified during research that currently **cannot be scraped** due to a technical issue on Instagram's side, not a quality or relevance problem with the accounts themselves.

## The technical issue, explained

Instaloader fetches basic profile data (followers, bio, post count) via Instagram's internal endpoint `https://www.instagram.com/api/v1/users/web_profile_info/`. For a specific class of accounts — verified "Business"/"Creator"-type profiles that have an internal sub-category tag set (e.g. a media company tagged "Magazine," a retailer tagged "Clothing Store") — this endpoint now returns:

```
400 Bad Request - "fail" status, message "Asset asset://laser.provider/ig_business_category_subvertical
has been deleted. You cannot use this schema"
```

In plain terms: Instagram appears to have deprecated or removed an internal field used to sub-categorize business accounts, but the code that builds the profile API response still tries to reference it for accounts that have that field set — instead of gracefully omitting it, the whole request fails with a hard error. This is a bug on Instagram's backend, not something wrong with Instaloader's request or these specific accounts. Confirmed reproducible across multiple retries; not a transient/rate-limit issue.

We're on the latest available Instaloader version (4.15.3, confirmed against both Homebrew and PyPI — no newer release exists as of Aug 24, 2026), so there's no update available yet that works around this.

## Affected accounts (13)

All verified as real, legitimate fashion-relevant Instagram accounts via web research — just currently inaccessible to this scraping pipeline:

| Account | Why it would have been valuable |
|---|---|
| [@vogueindia](https://www.instagram.com/vogueindia/) | Vogue's official India edition |
| [@missmalini](https://www.instagram.com/missmalini/) | Major Indian entertainment/fashion/lifestyle media outlet |
| [@wwdindia](https://www.instagram.com/wwdindia/) | WWD's India-focused trade coverage |
| [@thebridalbox](https://www.instagram.com/thebridalbox/) | Indian bridal fashion coverage |
| [@wedmegood](https://www.instagram.com/wedmegood/) | Large Indian wedding-fashion planning platform |
| [@fdciofficial](https://www.instagram.com/fdciofficial/) | Fashion Design Council of India — the official industry body |
| [@lakmefashionwk](https://www.instagram.com/lakmefashionwk/) | Lakme Fashion Week's official account |
| [@theindiastylefashionweek](https://www.instagram.com/theindiastylefashionweek/) | Official account for India's national-level (Delhi NCR) fashion week |
| [@indianfashionhubb](https://www.instagram.com/indianfashionhubb/) | Indian fashion/wedding style/celebrity glamour hub |
| [@indiannfashion](https://www.instagram.com/indiannfashion/) | "The Indian Fashion" official account |
| [@the.estd](https://www.instagram.com/the.estd/) | The Established — Indian fashion/culture digital publication |
| [@diet_paratha](https://www.instagram.com/diet_paratha/) | Fashion-commentary account (user-suggested) |
| [@currentmood.mag](https://www.instagram.com/currentmood.mag/) | Fashion/culture magazine account (user-suggested) |

## What to do about it

- **Periodically retry** these via `scripts/scrape_accounts.py` — if Instagram patches the bug or a new Instaloader release works around it, these should start working again with no code changes needed on our end (they're not hardcoded as excluded, just currently absent from the active `ACCOUNTS` list).
- **Don't read anything into their absence from the working dataset** — this is a tooling gap, not a signal that these accounts are inactive or low-quality. Several (Vogue India, FDCI, Lakme Fashion Week) are among the most authoritative sources in Indian fashion.
- If a manual data point from one of these is ever needed, it can be pulled by hand (viewing the account directly) rather than via the automated pipeline, until the underlying issue resolves.
