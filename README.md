# Agoda Hotel Reviews Scraper

> Scrape **Agoda hotel reviews** at scale — guest **scores** (/10), full **original + translated review text**, **liked/disliked** notes, **reviewer country**, **traveler type**, **stay dates**, **review photos**, and **hotel owner responses** — plus a per‑review **LLM‑ready markdown** block. Filter by **date, score, source, or any of Agoda's 33 review languages**. Runs on [Apify](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden).

[![Run on Apify](https://img.shields.io/badge/Run%20on-Apify-00b04f?logo=apify&logoColor=white)](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

This repo is the **developer entry point** for the Agoda Hotel Reviews Scraper actor: the output shape, copy‑paste API snippets, a full [field dictionary](./FIELDS.md), and a short [how‑to](./HOWTO.md). The actor itself runs on Apify — no login, no Agoda API key, no proxy or anti‑bot setup required.

**▶ [Run it on Apify →](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden)**

<p align="center">
  <a href="https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden" rel="sponsored noopener">
    <img src="https://raw.githubusercontent.com/factden/apify-actor-assets/main/agoda-hotel-reviews-scraper/02-reviews-overview.png" alt="Agoda Hotel Reviews Scraper — one structured row per guest review" width="900">
  </a>
</p>

---

## What it extracts

Point it at any Agoda hotel URL (or a bare numeric hotel ID) and get two structured datasets:

- **Reviews** — one row per guest review: the overall **/10 score**, the word **rating label**, full **review text** (original + translated), separate **liked / disliked** notes, **reviewer country**, **traveler type**, **room type**, **stay dates**, **length of stay**, **review photos**, any **hotel owner response**, and an LLM‑ready `markdownContent` block.
- **Hotels** — one summary row per hotel: property type, star rating, full address, coordinates, the Agoda score, total review count, and **per‑source scores** (Agoda, Booking.com, …).

### Two things worth knowing

🗣️ **Reviews in any of Agoda's 33 languages** — leave it empty for one combined all‑languages stream, or select specific languages and the actor fetches a dedicated stream per language and **merges + de‑duplicates** them for you.

🤖 **LLM‑ready `markdownContent` per review** — a self‑contained markdown block, ready for direct vector‑DB / RAG ingestion with zero formatting work.

|  |  |
|---|---|
| ![Hotel aggregate — one row per hotel](https://raw.githubusercontent.com/factden/apify-actor-assets/main/agoda-hotel-reviews-scraper/04-hotel-overview.png) | ![LLM-ready markdown field](https://raw.githubusercontent.com/factden/apify-actor-assets/main/agoda-hotel-reviews-scraper/03-reviews-ai-ingest.png) |
| Hotel aggregate — score, address, per‑source counts | LLM‑ready `markdownContent` field |

---

## Quick start (API)

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("factden/agoda-hotel-reviews-scraper").call(run_input={
    "hotelUrls": ["https://www.agoda.com/bayswater-inn-hotel/hotel/london-gb.html", "11019"],
    "maxReviews": 100,
    "sortBy": "newest",
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(row["hotelName"], row["score"])
```

More: **[Python](./snippets/run_actor.py)** · **[Node](./snippets/run_actor.js)** · **[curl](./snippets/run_actor.sh)**

<p align="center">
  <img src="https://raw.githubusercontent.com/factden/apify-actor-assets/main/agoda-hotel-reviews-scraper/01-input-form.png" alt="Agoda Hotel Reviews Scraper input form on Apify Console — hotel URLs plus filters and limits" width="720">
</p>

---

## Output

Real sample output lives in **[`examples/`](./examples)**:

- [`examples/reviews-sample.csv`](./examples/reviews-sample.csv) — **real review rows** — browse it right in GitHub's table view
- [`examples/reviews-output.sample.json`](./examples/reviews-output.sample.json) — 3 review rows showing the full field shape (incl. `markdownContent`)
- [`examples/input.json`](./examples/input.json) — a ready‑to‑run input

Every field is documented in **[`FIELDS.md`](./FIELDS.md)**. Scores are on Agoda's native **0–10 scale**. From Apify you can download results as **JSON, CSV, Excel, or HTML**.

---

## Use cases

- **Reputation & sentiment analysis** — track scores and guest sentiment for your own or competitor hotels.
- **Competitor benchmarking** — review volume, scores, and per‑source ratings per property.
- **Market research** — break reviews down by traveler type, reviewer country, and language.
- **AI / RAG pipelines** — drop each review's `markdownContent` straight into a vector DB.

---

## How much does it cost?

Pay‑per‑event on Apify: a **per‑review fee with no per‑run start fee** — and **nothing** if a run returns zero reviews. Lower **Max reviews per hotel** to cap cost. New Apify accounts get **free credit**. See the [actor page](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden) for current pricing.

---

## FAQ

**Does Agoda have a reviews API?** Not a public one for reading guest reviews — Agoda's partner/affiliate APIs cover rates and availability only. This actor returns the review data with no key and no partner account.

**Is scraping Agoda reviews legal?** The actor collects only **publicly available** review data. As with any scraping, review Agoda's Terms of Service and your local regulations (including GDPR), and use the data responsibly.

**Do I need an Agoda account or API key?** No. Everything runs inside the actor on Apify's infrastructure — no login, no key, no proxy setup.

**Can I get reviews in a specific language?** Yes — select one or more of Agoda's 33 review languages; the actor fetches a stream per language and merges + de‑duplicates them.

**A URL didn't resolve.** Agoda sometimes relists a hotel under a new URL. Open the hotel on agoda.com and paste its current URL, or use the numeric hotel ID.

**Found a bug or want a field added?** Open an issue here, or use the **Issues** tab on the [Apify actor page](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden).

---

## Other scrapers by FactDen

- [Expedia Reviews Scraper](https://apify.com/factden/expedia-hotel-reviews-scraper?fpr=factden)
  ([docs](https://github.com/factden/expedia-hotel-reviews-scraper))
- [Hotels.com Reviews Scraper](https://apify.com/factden/hotels-com-reviews-scraper?fpr=factden)
  ([docs](https://github.com/factden/hotels-com-reviews-scraper))
- [Trip.com & Ctrip Reviews Scraper](https://apify.com/factden/ctrip-trip-reviews-scraper?fpr=factden)
  ([docs](https://github.com/factden/ctrip-trip-reviews-scraper))
- [Google Hotels Scraper](https://apify.com/factden/google-hotels-scraper?fpr=factden)
  ([docs](https://github.com/factden/google-hotels-scraper))
- [TripAdvisor Hotel Reviews API](https://apify.com/factden/tripadvisor-hotel-reviews-api?fpr=factden)
  ([docs](https://github.com/factden/tripadvisor-hotel-reviews-api))
- [MakeMyTrip & Goibibo Reviews Scraper](https://apify.com/factden/makemytrip-scraper?fpr=factden)
  ([docs](https://github.com/factden/makemytrip-scraper))
- [Airbnb Data Scraper](https://apify.com/factden/airbnb-data-scraper?fpr=factden)
  ([docs](https://github.com/factden/airbnb-data-scraper))
- [All FactDen actors →](https://apify.com/factden?fpr=factden)

---

_The sample data in this repo is real public Agoda review data, collected with the actor and provided for documentation/evaluation. Run the actor on Apify to pull data for any hotel, at any scale._

_Found this useful? A star on this repo helps other people find it._
