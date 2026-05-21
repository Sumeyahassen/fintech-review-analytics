import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ====================== LOAD PROCESSED DATA ======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
processed_file = os.path.join(BASE_DIR, 'data', 'processed', 'processed_reviews.csv')

df = pd.read_csv(processed_file)
print("Loaded processed data:", df.shape)

# ====================== ADVANCED ANALYSIS ======================

# 1. Sentiment Score Statistics
print("\n" + "="*60)
print("SENTIMENT SCORE STATISTICS")
print("="*60)
print(df['sentiment_score'].describe())

# 2. Sentiment by Theme (Very Important)
theme_sentiment = df.groupby('identified_theme').agg(
    count=('review', 'size'),
    avg_sentiment=('sentiment_score', 'mean'),
    positive_ratio=('sentiment_label', lambda x: (x == 'Positive').mean() * 100)
).round(3)

print("\nSentiment by Theme:")
print(theme_sentiment.sort_values('avg_sentiment', ascending=False))

# 3. Save Summary
theme_sentiment.to_csv(os.path.join(BASE_DIR, 'data', 'processed', 'theme_summary.csv'))

# ====================== VISUALIZATIONS ======================

plt.figure(figsize=(12, 6))
sns.barplot(data=theme_sentiment.reset_index(), 
            x='avg_sentiment', y='identified_theme', palette='coolwarm')
plt.title('Average Sentiment Score by Theme')
plt.xlabel('Average Sentiment Score')
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'images', 'sentiment_by_theme.png'), dpi=300, bbox_inches='tight')
plt.show()

print("\n Task 3 Analysis Completed!")
print("Summary saved: data/processed/theme_summary.csv")