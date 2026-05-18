import pandas as pd
from transformers import pipeline # type: ignore
import os
import matplotlib.pyplot as plt
import seaborn as sns

# ====================== CONFIG ======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'data', 'cleaned_reviews.csv')
output_dir = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'images'), exist_ok=True)

# Load data
df = pd.read_csv(file_path)
print("Original shape:", df.shape)

# Add review_id if not exists
if 'review_id' not in df.columns:
    df = df.reset_index().rename(columns={'index': 'review_id'})

# ====================== SENTIMENT ANALYSIS ======================
print("\nLoading DistilBERT model...")
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def get_sentiment(text):
    try:
        result = sentiment_pipeline(str(text)[:512])[0]
        label = result['label']
        score = result['score']
        if label == "NEGATIVE":
            return "Negative", round(-score, 4)
        else:
            return "Positive", round(score, 4)
    except:
        return "Neutral", 0.0

print("Performing Sentiment Analysis...")
df[['sentiment_label', 'sentiment_score']] = df['review'].apply(
    lambda x: pd.Series(get_sentiment(x))
)

# ====================== THEMATIC ANALYSIS ======================
def assign_theme(text):
    text = str(text).lower()
    if any(k in text for k in ['login', 'log in', 'otp', 'password', 'sign', 'account', 'verify']):
        return "Account Access Issues"
    elif any(k in text for k in ['slow', 'loading', 'crash', 'freeze', 'lag', 'speed', 'hang']):
        return "Performance Issues"
    elif any(k in text for k in ['transfer', 'send money', 'transaction', 'withdraw', 'deposit', 'payment']):
        return "Transaction Problems"
    elif any(k in text for k in ['ui', 'interface', 'design', 'button', 'screen', 'navigation']):
        return "UI/UX Experience"
    elif any(k in text for k in ['support', 'customer service', 'help', 'agent', 'chat']):
        return "Customer Support"
    elif any(k in text for k in ['good', 'excellent', 'great', 'love', 'best', 'fast', 'easy']):
        return "Positive Feedback"
    else:
        return "Other"

df['identified_theme'] = df['review'].apply(assign_theme)

# ====================== SAVE RESULTS ======================
final_columns = ['review_id', 'review', 'sentiment_label', 'sentiment_score', 'identified_theme']
df[final_columns].to_csv(os.path.join(output_dir, 'processed_reviews.csv'), index=False)

print("\n✅ Task 2 Completed!")
print(f"Total Reviews Processed: {len(df)}")
print("\nSentiment Distribution:\n", df['sentiment_label'].value_counts())
print("\nTheme Distribution:\n", df['identified_theme'].value_counts().head(7))

# ====================== VISUALIZATIONS ======================
# Sentiment Pie Chart
plt.figure(figsize=(8,6))
df['sentiment_label'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#4CAF50','#FF5252'])
plt.title('Sentiment Distribution')
plt.ylabel('')
plt.savefig(os.path.join(BASE_DIR, 'images', 'sentiment_distribution.png'), dpi=300, bbox_inches='tight')
plt.show()

# Top Themes
plt.figure(figsize=(10,6))
top_themes = df['identified_theme'].value_counts().head(8)
sns.barplot(x=top_themes.values, y=top_themes.index, palette='viridis')
plt.title('Top Themes in Customer Reviews')
plt.xlabel('Number of Reviews')
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'images', 'top_themes.png'), dpi=300, bbox_inches='tight')
plt.show()