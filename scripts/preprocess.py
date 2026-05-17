import pandas as pd
import os

# Load the raw data
df = pd.read_csv('data/raw/raw_reviews.csv')

print("Original Data Shape:", df.shape)
print("\nReviews per bank:")
print(df['bank'].value_counts())

# ====================== PREPROCESSING ======================

# 1. Remove duplicate reviews
df = df.drop_duplicates(subset=['review', 'date', 'bank'])

# 2. Remove rows with missing review text or rating
df = df.dropna(subset=['review', 'rating'])

# 3. Convert rating to integer
df['rating'] = df['rating'].astype(int)

# 4. Ensure date format is correct
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

# Final columns
final_columns = ['review', 'rating', 'date', 'bank', 'source']
df = df[final_columns]

# ====================== SAVE ======================
os.makedirs('data', exist_ok=True)
df.to_csv('data/cleaned_reviews.csv', index=False)

print("\n" + "="*50)
print("✅ Preprocessing Completed!")
print("Cleaned Data Shape:", df.shape)
print("\nFinal Reviews per Bank:")
print(df['bank'].value_counts())
print(f"\nTotal Clean Reviews: {len(df)}")
print("Cleaned file saved as: data/cleaned_reviews.csv")