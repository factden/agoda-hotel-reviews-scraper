# Output fields

The Agoda Hotel Reviews Scraper produces **two datasets**. The **Reviews** dataset (the default) has one row per
public guest review, with the hotel context merged onto each row. The **Hotels** dataset has one row per hotel with
the aggregate. Scores are on Agoda's native **0–10 scale**. Fields a given review doesn't provide are `null` (or an
empty array).

## Reviews dataset

Each row starts with the hotel context, then the review fields.

| Field | Type | Description |
|---|---|---|
| `hotelId` | integer | Agoda hotel id. |
| `hotelName` | string \| null | Hotel display name. |
| `hotelUrl` | string \| null | The hotel-page URL that produced this row (`null` for a bare-ID input). |
| `reviewId` | string | Unique review identifier. |
| `source` | string \| null | Booking site the review was posted on (`Agoda`, `Booking.com`, …). |
| `providerId` | integer \| null | Agoda's numeric provider id for the source (Agoda = 332). |
| `title` | string \| null | Review headline (original language, falling back to the displayed title). |
| `text` | string \| null | Full review body (positives, negatives and free-text comment combined). |
| `positives` | string \| null | What the guest liked. |
| `negatives` | string \| null | What the guest disliked. |
| `score` | number \| null | Overall review score on the **0–10** scale. |
| `ratingText` | string \| null | Agoda's word label for the score (Exceptional, Very good, Good, …). |
| `reviewDate` | string \| null | Day the review was submitted (`YYYY-MM-DD`). |
| `reviewerName` | string \| null | Reviewer display name. |
| `reviewerCountry` | string \| null | Reviewer's country. |
| `travelerType` | string \| null | Traveler type (Couple, Family with young children, Solo traveler, Business traveler, …). |
| `roomType` | string \| null | Room type the guest booked. |
| `checkInDate` | string \| null | Guest check-in date (`YYYY-MM-DD`). |
| `checkOutDate` | string \| null | Guest check-out date (`YYYY-MM-DD`). |
| `lengthOfStay` | integer \| null | Length of stay in nights. |
| `reviewPhotos` | array | Guest photos: `[{ url, caption, id }]`. |
| `ownerResponse` | object \| null | Hotel/manager reply `{ text, date }`, or `null` when the hotel has not replied. |
| `markdownContent` | string | **LLM-ready** self-contained markdown block for the review — drop straight into a RAG pipeline. |

## Hotels dataset

One row per hotel (the aggregate). Starts with the same hotel context (`hotelId`, `hotelName`, `hotelUrl`), then:

| Field | Type | Description |
|---|---|---|
| `propertyType` | string \| null | Property type (Hotel, Resort, Apartment, …). |
| `stars` | number \| null | Star rating. |
| `addressStreet` | string \| null | Street address. |
| `addressCity` | string \| null | City. |
| `addressRegion` | string \| null | Area / district. |
| `addressCountry` | string \| null | Country. |
| `addressZip` | string \| null | Postal code. |
| `latitude` / `longitude` | number \| null | Property coordinates. |
| `score` | number \| null | Agoda's aggregate score on the **0–10** scale. |
| `reviewsCount` | integer \| null | Total Agoda reviews the property reports. |
| `providerScores` | array \| null | Per-source `{ providerId, source, score, reviewCount, maxScore }`. |
| `reviewsExtracted` | integer | How many reviews this run actually delivered for the hotel. |
| `extractedAt` | string | When the hotel row was scraped (UTC ISO 8601). |

## Dataset views

The Reviews dataset ships two pre-built views you can switch between in the Console or request via the API:

- **Overview** — the columns most users want first (hotel, reviewer, score, review text, owner response, stay).
- **AI ingest (LLM-ready)** — `markdownContent` plus score, hotel and source — optimized for vector-DB / RAG loading.
