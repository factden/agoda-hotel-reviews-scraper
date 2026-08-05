# How to scrape Agoda hotel reviews (the easy way)

Scraping Agoda directly is painful: anti-bot defenses, session handling, rotating proxies, and reviews spread
across 33 languages and multiple booking sources. This guide skips all of that by using the
[Agoda Hotel Reviews Scraper](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden) actor on Apify —
no login, no proxy setup, no anti-bot tuning.

## 1. Get an Apify token

Create a free [Apify](https://console.apify.com/sign-up?fpr=factden) account and copy your API token from
**Settings → Integrations**. New accounts include free credit.

## 2. Run it from the Console (no code)

1. Open the [actor page](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden) and click **Try for free**.
2. The input is pre-filled with example hotels. Leave them or replace them with your own.
3. Click **Start**. A small run finishes in well under a minute.
4. Download results from the **Output** tab as JSON, CSV, or Excel.

## 3. Find a hotel URL

Open a hotel's page on Agoda and copy the URL, e.g.
`https://www.agoda.com/bayswater-inn-hotel/hotel/london-gb.html`. Any regional Agoda domain and a locale prefix
(e.g. `/en-gb/`) are fine. You can paste the full URL, or just the **bare numeric hotel ID** (`11019`).

## 4. Run it from code

### Python

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("factden/agoda-hotel-reviews-scraper").call(run_input={
    "hotelUrls": ["https://www.agoda.com/bayswater-inn-hotel/hotel/london-gb.html"],
    "maxReviews": 200,
})
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Got {len(items)} reviews")
```

See [`snippets/`](./snippets) for Node and curl versions.

## 5. Useful input options

| Option | What it does |
|---|---|
| `maxReviews` | Cap reviews per hotel (controls cost). |
| `sortBy` | `newest`, `oldest`, `highestRating`, `lowestRating`. |
| `fromDate` / `toDate` | Only reviews in a `YYYY-MM-DD` window. |
| `minRating` / `maxRating` | Filter by score (Agoda uses a **0–10** scale). |
| `reviewSources` | Which booking sources to return. Defaults to Agoda; clear it for every source. |
| `languages` | Return only selected languages; empty = all languages in one stream. |

Full field reference: [`FIELDS.md`](./FIELDS.md). Full input format: [`examples/input.json`](./examples/input.json).

## 6. Feed it to an LLM

Each review includes a ready-to-use `markdownContent` field — no formatting needed:

```python
docs = [row["markdownContent"] for row in items]
# embed `docs` into your vector DB / RAG pipeline
```

---

**▶ [Run the Agoda Hotel Reviews Scraper on Apify →](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden)**
