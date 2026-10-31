# Examples

All real public review data collected with the actor (Park Avenue Bayswater Inn Hyde Park, London — hotel `11019`).

### Reviews mode (default)

- **`input.json`** — a ready-to-run actor input (one Agoda hotel URL).
- **`reviews-output.sample.json`** — **3 real review rows** showing the full field shape: a top 10/10 stay, a
  mid-score stay with a guest photo, and a critical low-score stay, each with the LLM-ready `markdownContent` block.
- **`reviews-sample.csv`** — **real reviews**, browsable right in GitHub's table view. CSV-flattened:
  `reviewPhotos` joined into one cell, `ownerResponse` split into `ownerResponse_text` / `ownerResponse_date`, and
  `markdownContent` omitted for readability.

### Prices mode (`mode: "prices"`)

- **`prices-input.json`** - a ready-to-run Prices-mode input: one Agoda hotel, a check-in date, 1 night, currency
  USD. Set a `priceWindowEnd` to price a whole date range for tracking.
- **`offers-output.sample.json`** - two `offers` rows for one hotel: an available check-in date (two room types,
  each with rate plans, breakfast, strikethrough and rooms-left) and a sold-out date (`available: false`).

Scores are on Agoda's native **0–10 scale**; prices are in the requested currency. See
[`../FIELDS.md`](../FIELDS.md) for every field.

Run the actor for any hotel: **https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden**
