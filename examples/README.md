# Examples

All real public review data collected with the actor (Park Avenue Bayswater Inn Hyde Park, London — hotel `11019`).

- **`input.json`** — a ready-to-run actor input (one Agoda hotel URL).
- **`reviews-output.sample.json`** — **3 real review rows** showing the full field shape: a top 10/10 stay, a
  mid-score stay with a guest photo, and a critical low-score stay, each with the LLM-ready `markdownContent` block.
- **`reviews-sample.csv`** — **real reviews**, browsable right in GitHub's table view. CSV-flattened:
  `reviewPhotos` joined into one cell, `ownerResponse` split into `ownerResponse_text` / `ownerResponse_date`, and
  `markdownContent` omitted for readability.

Scores are on Agoda's native **0–10 scale**.

Run the actor for any hotel: **https://apify.com/factden/agoda-hotel-reviews-scraper?fpr=factden**
