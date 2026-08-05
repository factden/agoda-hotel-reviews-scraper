"""Run the Agoda Hotel Reviews Scraper on Apify and print the results.

Install:  pip install apify-client
Docs:     https://apify.com/factden/agoda-hotel-reviews-scraper
"""

from apify_client import ApifyClient

# Get your token from https://console.apify.com/settings/integrations
client = ApifyClient("<YOUR_APIFY_TOKEN>")

run_input = {
    "hotelUrls": [
        "https://www.agoda.com/bayswater-inn-hotel/hotel/london-gb.html",
    ],
    "maxReviews": 100,
    "sortBy": "newest",
}

# Start the actor and wait for it to finish
run = client.actor("factden/agoda-hotel-reviews-scraper").call(run_input=run_input)

# Iterate the resulting dataset (one row per review)
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"{row.get('score')}/10  {row.get('hotelName')}")
    if row.get("ownerResponse"):
        print("   ↳ hotel responded")
