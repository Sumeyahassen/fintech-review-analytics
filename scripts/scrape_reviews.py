from google_play_scraper import reviews, Sort
import pandas as pd
from tqdm import tqdm
import time

# Correct App IDs for the three banks
apps = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

all_reviews = []

for bank_name, app_id in tqdm(apps.items(), desc="Scraping Banks"):
    print(f"\n🔄 Scraping {bank_name}...")
    
    # First batch
    result, continuation_token = reviews(
        app_id,
        lang='en',
        country='et',
        sort=Sort.NEWEST,
        count=200
    )
    
    for r in result:
        all_reviews.append({
            'review': r['content'],
            'rating': r['score'],
            'date': r['at'].strftime('%Y-%m-%d'),
            'bank': bank_name,
            'source': 'Google Play'
        })
    
    # Get more reviews using continuation token
    while continuation_token and len(all_reviews) < 1500:
        print(f"   Continuing {bank_name}... (Total: {len(all_reviews)})")
        result, continuation_token = reviews(
            app_id,
            continuation_token=continuation_token,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=200
        )
        for r in result:
            all_reviews.append({
                'review': r['content'],
                'rating': r['score'],
                'date': r['at'].strftime('%Y-%m-%d'),
                'bank': bank_name,
                'source': 'Google Play'
            })
        time.sleep(2)  # Avoid being blocked

# Convert to DataFrame and Save
df = pd.DataFrame(all_reviews)

# Create folder if not exists
import os
os.makedirs('data/raw', exist_ok=True)

df.to_csv('data/raw/raw_reviews.csv', index=False)

print("\n✅ Scraping Completed Successfully!")
print("="*50)
print(df['bank'].value_counts())
print(f"Total Reviews Collected: {len(df)}")