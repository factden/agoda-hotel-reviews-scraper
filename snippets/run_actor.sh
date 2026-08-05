#!/usr/bin/env bash
# Run the Agoda Hotel Reviews Scraper on Apify with curl, then fetch the dataset.
# Docs: https://apify.com/factden/agoda-hotel-reviews-scraper

TOKEN="<YOUR_APIFY_TOKEN>"   # https://console.apify.com/settings/integrations

# Run the actor synchronously and get dataset items back in one call
curl -s -X POST \
  "https://api.apify.com/v2/acts/factden~agoda-hotel-reviews-scraper/run-sync-get-dataset-items?token=${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "hotelUrls": [
      "https://www.agoda.com/bayswater-inn-hotel/hotel/london-gb.html"
    ],
    "maxReviews": 100,
    "sortBy": "newest"
  }'
