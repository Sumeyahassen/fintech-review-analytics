import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
df = pd.read_csv('data/processed_reviews.csv')   # Use the one with sentiment if you have it
# If you don't have processed_reviews.csv yet, use cleaned_reviews.csv for now

print("Generating visualizations...")

# Set style
sns.set_style("whitegrid")

# 1. Rating Distribution by Bank
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='bank', y='rating')
plt.title('Rating Distribution by Bank')
plt.ylabel('Rating (1-5)')
plt.savefig('images/rating_distribution.png')
plt.show()

# 2. Average Rating by Bank
plt.figure(figsize=(8, 5))
avg_rating = df.groupby('bank')['rating'].mean().sort_values(ascending=False)
sns.barplot(x=avg_rating.index, y=avg_rating.values)
plt.title('Average Rating by Bank')
plt.ylabel('Average Rating')
plt.savefig('images/avg_rating.png')
plt.show()

# 3. Review Count by Bank
plt.figure(figsize=(8, 5))
counts = df['bank'].value_counts()
sns.barplot(x=counts.index, y=counts.values)
plt.title('Number of Reviews per Bank')
plt.ylabel('Number of Reviews')
plt.savefig('images/review_count.png')
plt.show()

print("✅ Visualizations saved in 'images/' folder!")