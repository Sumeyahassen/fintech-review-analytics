from google_play_scraper import reviews, Sort
import pandas as pd
import time
import os

# Only BOA and Dashen
apps = {
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

all_new = []

for bank_name, app_id in apps.items():
    print(f"\n🔄 Scraping more for {bank_name}...")
    continuation_token = None
    count = 0
    
    while count < 600:   # Try to get up to 600
        result, continuation_token = reviews(
            app_id,
            continuation_token=continuation_token, # type: ignore
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=200
        )
        for r in result:
            all_new.append({
                'review': r['content'],
                'rating': r['score'],
                'date': r['at'].strftime('%Y-%m-%d'),
                'bank': bank_name,
                'source': 'Google Play'
            })
        count += len(result)
        print(f"  Got {len(result)} more → Total for {bank_name}: {count}")
        if not continuation_token:
            break
        time.sleep(2)

# Append to existing raw file
df_new = pd.DataFrame(all_new)
os.makedirs('data/raw', exist_ok=True)

if os.path.exists('data/raw/raw_reviews.csv'):
    df_old = pd.read_csv('data/raw/raw_reviews.csv')
    df_combined = pd.concat([df_old, df_new], ignore_index=True)
else:
    df_combined = df_new

df_combined.to_csv('data/raw/raw_reviews.csv', index=False)
print(f"\nAdded more reviews. New total: {len(df_combined)}")