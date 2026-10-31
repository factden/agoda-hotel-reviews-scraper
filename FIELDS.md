# Output fields

In **Reviews** mode the Agoda Hotel Reviews Scraper produces **two datasets**. The **Reviews** dataset (the default)
has one row per public guest review, with the hotel context merged onto each row. The **Hotels** dataset has one row
per hotel with the aggregate. Scores are on Agoda's native **0–10 scale**. Fields a given review doesn't provide are
`null` (or an empty array).

In **Prices** mode (`mode: "prices"`) the actor instead writes the **Offers** dataset: one row per hotel per
check-in date (see [Offers dataset](#offers-dataset-prices-mode) below).

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

## Offers dataset (Prices mode)

In Prices mode (`mode: "prices"`) the actor writes one row per **hotel × check-in date** to the `offers` dataset.
A sold-out date is kept as a row with `available: false` - a checked date with no inventory is a real result,
delivered (and billed) just like an available date.

| Field | Type | Description |
|---|---|---|
| `hotelId` | integer | Agoda hotel id. |
| `hotelName` / `hotelUrl` | string \| null | Hotel name / the URL that produced this row. |
| `cityId` | integer \| null | Agoda city id for the property. |
| `currency` | string \| null | ISO currency of the prices in this row (set by the `currency` input). |
| `market` | string \| null | Content locale the prices were read with. |
| `checkInDate` / `checkOutDate` | string | Stay dates (`YYYY-MM-DD`). |
| `nights` / `rooms` / `adults` / `children` | integer | The booking party. |
| `available` | boolean | True if ≥1 room was bookable; false = sold out / no inventory (data flag only - every returned hotel-date is billed). |
| `soldOut` | boolean | True when the date is sold out / has no inventory. |
| `leadPerNight` / `leadTotal` | number \| null | Lowest per-night / total price across rooms (quick-scan lead price). |
| `roomCount` | integer | Number of bookable room entries returned (length of `offers`). |
| `offers` | array \| null | One entry per bookable room type, each with its own rate plans. See [Offer item](#offers-item-one-room-type) below. |
| `scrapedAt` | string | When the row was scraped (UTC ISO 8601). |
| `markdownContent` | string \| null | LLM-ready summary of this hotel-date's prices. |

### `offers[]` item (one room type)

Note: Agoda's per-room data is an `offers[]` array (one entry per room type), not a `rooms[]` array.

| Field | Type | Description |
|---|---|---|
| `typeId` | string \| null | Agoda room-type id. |
| `roomName` | string \| null | Room-type name (e.g. "Double Room", "Twin Room"). |
| `roomSize` | string \| null | Room size as shown by Agoda (e.g. "18 m²"), when available. |
| `bedType` | string \| null | Bed configuration (e.g. "1 double bed"). |
| `maxOccupancy` | string \| null | Max guests the room sleeps, as shown by Agoda. |
| `perNight` | number \| null | Lead per-night price for this room type (total / nights). |
| `total` | number \| null | Lead total stay price for this room type. |
| `strikethrough` | number \| null | Was-price (crossed-out original) when higher than `total`. |
| `currency` | string \| null | ISO currency of this room's prices (matches the row `currency`). |
| `tax` | number \| null | Reserved. The room grid does not itemize tax, so this is currently `null`. |
| `fees` | number \| null | Reserved. Not itemized by the room grid; currently `null`. |
| `totalInclusive` | number \| null | Reserved (tax/fee-inclusive total); currently `null`. |
| `breakfastIncluded` | boolean \| null | True when the lead rate for this room includes breakfast. |
| `inventorySource` | string \| null | Supplier/inventory source for the room (e.g. "Agoda"), when identifiable. |
| `roomsLeft` | integer \| null | Scarcity: rooms left at this price, when Agoda surfaces it. |
| `ratePlans` | array \| null | The bookable rate plans for this room type. See [Rate plan](#offersrateplans-item-one-rate-plan) below. |

### `offers[].ratePlans[]` item (one rate plan)

| Field | Type | Description |
|---|---|---|
| `ratePlanId` | string \| null | Agoda rate-plan id. |
| `ratePlanName` | string \| null | Rate-plan label (e.g. "Breakfast included"), when named. |
| `perNight` | number \| null | Per-night price for this rate plan (total / nights). |
| `total` | number \| null | Total stay price for this rate plan. |
| `strikethrough` | number \| null | Was-price for this rate plan, when higher than `total`. |
| `refundable` | boolean \| null | True if the rate plan is refundable / has free cancellation. |
| `freeCancellationUntil` | string \| null | Free-cancellation deadline, when the plan is refundable. |
| `paymentModel` | string \| null | `pay-now` vs `pay-later` (pay at hotel), when identifiable. |
| `breakfastIncluded` | boolean \| null | True when this rate plan includes breakfast. |
| `supplier` | string \| null | Inventory supplier for this rate plan, when identifiable. |

## Dataset views

The Reviews dataset ships two pre-built views you can switch between in the Console or request via the API:

- **Overview** — the columns most users want first (hotel, reviewer, score, review text, owner response, stay).
- **AI ingest (LLM-ready)** — `markdownContent` plus score, hotel and source — optimized for vector-DB / RAG loading.

The Offers dataset (Prices mode) ships two views:

- **Overview** - one row per hotel per check-in date with the lead price, room count and availability.
- **Prices (per room)** - each room type unwound into its own flat row (room, per-night, total, breakfast, bed,
  max guests, inventory source, rooms-left).
