# Agoda Hotel Reviews Scraper

> Scrape **Agoda hotel reviews** at scale — guest **scores** (/10), full **original + translated review text**, **liked/disliked** notes, **reviewer country**, **traveler type**, **stay dates**, **review photos**, and **hotel owner responses** — plus a per‑review **LLM‑ready markdown** block. Filter by **date, score, source, or any of Agoda's 33 review languages**. Runs on [Apify](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden).

> One actor, two jobs: **Reviews + Prices**. Switch to **Prices mode** for **live room rates, per‑room rate
> plans, and availability by date** in 24 currencies, with one billable row per hotel per check‑in date.

[![Run on Apify](https://img.shields.io/badge/Run%20on-Apify-00b04f?logo=apify&logoColor=white)](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

This repo is the **developer entry point** for the Agoda Hotel Reviews Scraper actor: the output shape, copy‑paste API snippets, a full [field dictionary](./FIELDS.md), and a short [how‑to](./HOWTO.md). The actor itself runs on Apify — no login, no Agoda API key, no proxy or anti‑bot setup required.

**▶ [Run it on Apify →](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden)**

**Watch the walkthrough:**

[![Agoda Hotel Reviews Scraper demo](https://img.youtube.com/vi/zSUbguMJiIg/maxresdefault.jpg)](https://www.youtube.com/watch?v=zSUbguMJiIg)

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

Or switch to **Prices mode** (`mode: "prices"`) to get **live room rates & availability by date** instead — one row per hotel per check-in date with room-wise rate plans, inventory supplier, breakfast/cancellation flags and scarcity, in 24 currencies. See [FIELDS.md](FIELDS.md#offers-dataset-prices-mode).

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

## Prices mode: room rates & availability by date

Set **Mode** to `prices` (`"mode": "prices"`) to pull **live room rates and availability** for the same hotels
instead of reviews. You get **one row per hotel per check-in date** in the `offers` dataset, with **one entry per
room type** (not a `rooms[]` array). Each room entry carries its **per-night and total price**, **strikethrough**
(was-price), **breakfast** flag, **bed type / max occupancy**, **inventory source**, **rooms-left** scarcity, and a
list of **rate plans** (pay-now vs pay-at-hotel, refundable vs non-refundable, free-cancellation deadline).

How to scrape Agoda prices:

1. Switch **Mode** to **Prices**.
2. Paste the same **Hotel URLs or IDs** (one per line).
3. Set the stay: **Check-in date**, **Nights**, and the booking party (**Rooms / Adults / Children ages**).
4. Pick a **Currency** (one of 24, USD default). The currency is set in the request, so the proxy country does not
   change it, and one run returns one currency.
5. (Optional) Set a **Price window end** plus a **Price window step** to price every check-in across a date range
   (one row per date) for rate and availability tracking. Step `1` is daily, `7` is weekly and cheaper.
6. Click **Start**, then export the `offers` dataset as **JSON, CSV, Excel, or HTML**, or pull it from the API.

A sold-out date is still returned as a row with `"available": false`. A checked date with no inventory is a real
result, delivered alongside the available dates. Ready-to-run input: [`examples/prices-input.json`](./examples/prices-input.json).
Sample output: [`examples/offers-output.sample.json`](./examples/offers-output.sample.json). Full field reference:
[FIELDS.md → Offers dataset](./FIELDS.md#offers-dataset-prices-mode).

```json
{
  "mode": "prices",
  "hotelUrls": ["https://www.agoda.com/bayswater-inn-hotel/hotel/london-gb.html"],
  "checkInDate": "2026-12-01",
  "nights": 1,
  "currency": "USD"
}
```

**Reviews mode is unchanged:** existing review runs and their inputs keep working exactly as before.

---

## Use cases

- **Reputation & sentiment analysis** — track scores and guest sentiment for your own or competitor hotels.
- **Competitor benchmarking** — review volume, scores, and per‑source ratings per property.
- **Market research** — break reviews down by traveler type, reviewer country, and language.
- **AI / RAG pipelines** — drop each review's `markdownContent` straight into a vector DB.
- **Rate & availability tracking** (Prices mode) - monitor room prices, rate plans and sold-out dates across a
  date window, in any of 24 currencies.

---

## How much does it cost?

Pay‑per‑event on Apify. Lower **Max reviews per hotel** (reviews) or use a wider **Price window step** (prices) to
cap cost. New Apify accounts get **free credit**.

- **Reviews mode:** a per‑review fee, charged only on reviews actually returned, plus a small **$0.005 run start
  fee** (effective November 14, 2026).
- **Prices mode:** a per‑priced‑hotel‑date fee (one hotel × check‑in date), around **$0.005** on the free tier and
  less on paid tiers. **Sold‑out dates are billed too**, because a checked, no‑inventory date is a real result.

See the [actor page](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden) for current, tier-by-tier
pricing.

---

## FAQ

**Does Agoda have a reviews API?** Not a public one for reading guest reviews — Agoda's partner/affiliate APIs cover rates and availability only. This actor returns the review data with no key and no partner account.

**Is scraping Agoda reviews legal?** The actor collects only **publicly available** review data. As with any scraping, review Agoda's Terms of Service and your local regulations (including GDPR), and use the data responsibly.

**Do I need an Agoda account or API key?** No. Everything runs inside the actor on Apify's infrastructure — no login, no key, no proxy setup.

**Can I get reviews in a specific language?** Yes — select one or more of Agoda's 33 review languages; the actor fetches a stream per language and merges + de‑duplicates them.

**Can I get room prices and availability, not just reviews?** Yes. Set **Mode** to **Prices** to get live room
rates, per‑room rate plans and availability by date (one row per hotel per check‑in date) in 24 currencies. See
[Prices mode](#prices-mode-room-rates--availability-by-date) above.

**A URL didn't resolve.** Agoda sometimes relists a hotel under a new URL. Open the hotel on agoda.com and paste its current URL, or use the numeric hotel ID.

**Found a bug or want a field added?** Open an issue here, or use the **Issues** tab on the [Apify actor page](https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden).

---

## Other scrapers by FactDen

- [Booking.com Scraper](https://apify.com/factden/booking-com-scraper?fpr=factden) - hotels, live prices, per-room rates, availability & occupancy, and guest reviews across a whole city or one hotel ([docs](https://github.com/factden/booking-com-scraper))
- [MCA India Company & Director Data Scraper](https://apify.com/factden/mca-company-director-scraper?fpr=factden) - India MCA company master + directors' personal email & phone
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
- [Fliggy Hotel Reviews Scraper](https://apify.com/factden/fliggy-hotel-reviews-scraper?fpr=factden) - Fliggy (飞猪) hotel reviews by city or URL, with per-dimension sub-ratings, sentiment tags & AI summaries ([docs](https://github.com/factden/fliggy-hotel-reviews-scraper))
- [Traveloka Hotel & Activity Reviews Scraper](https://apify.com/factden/traveloka-hotel-reviews-scraper?fpr=factden) - Traveloka hotel & Xperience activity reviews with 1-10 ratings, category sub-scores, owner replies & English translation ([docs](https://github.com/factden/traveloka-hotel-reviews-scraper))
- [All FactDen actors →](https://apify.com/factden?fpr=factden)

---

_The sample data in this repo is real public Agoda review data, collected with the actor and provided for documentation/evaluation. Run the actor on Apify to pull data for any hotel, at any scale._

_Found this useful? A star on this repo helps other people find it._
