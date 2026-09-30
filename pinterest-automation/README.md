# Pinterest automation (bombay-bride.com)

Scrape bridal/couture imagery from brand sites, queue 2 pins/day, post via n8n.

- `scrapers/`      per-platform scrapers (`shopify.py` works for any Shopify brand)
- `sources/`       one JSON per brand: product title, page URL, image URLs, credit
- `images/`        downloaded lead images, one folder per brand (gitignored: third-party copyright)
- `queue/`         pin queue (title, description, board, link, source credit, status)
- `n8n-workflows/` exported n8n workflow JSON (Pinterest node: OfficialMoAdel/n8n-nodes-pinterest)
- `docs/`          notes, link/credit policy

Each pin credits the source brand. Nothing posts without approval.
