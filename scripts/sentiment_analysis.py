import pandas as pd
from transformers import pipeline # type: ignore
import nltk
from nltk.corpus import stopwords
import os

# Download NLTK data
nltk.download('stopwords', quiet=True)

# Load cleaned data
df = pd.read_csv('data/cleaned_reviews.csv')
print("Original shape:", df.shape)

# ========================= SENTIMENT ANALYSIS =========================
print("\nLoading sentiment model... (this may take a minute)")

# Using DistilBERT model (good and fast)
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def get_sentiment(text):
    try:
        result = sentiment_pipeline(text[:512])[0]  # type: ignore # limit text length
        label = result['label'] # type: ignore
        score = result['score'] # type: ignore
        if label == "NEGATIVE":
            return "Negative", round(-score, 4) # type: ignore
        else:
            return "Positive", round(score, 4) # type: ignore
    except:
        return "Neutral", 0.0

print("Analyzing sentiment...")
df[['sentiment_label', 'sentiment_score']] = df['review'].apply(
    lambda x: pd.Series(get_sentiment(str(x)))
)

# ========================= BASIC THEME KEYWORDS =========================
def assign_theme(text):
    text = str(text).lower()
    if any(word in text for word in ['login', 'log in', 'otp', 'password', 'sign']):
        return "Account Access Issues"
    elif any(word in text for word in ['slow', 'loading', 'crash', 'freeze', 'lag']):
        return "Performance Issues"
    elif any(word in text for word in ['transfer', 'send money', 'transaction']):
        return "Transaction Problems"
    elif any(word in text for word in ['ui', 'interface', 'design', 'look']):
        return "UI/UX Experience"
    elif any(word in text for word in ['good', 'excellent', 'love', 'great', 'fast']):
        return "Positive Feedback"
    else:
        return "Other"

df['identified_theme'] = df['review'].apply(assign_theme)

# ========================= SAVE RESULTS =========================
os.makedirs('data', exist_ok=True)
df.to_csv('data/processed_reviews.csv', index=False)

print("\n" + "="*60)
print("=>Task 2 Sentiment Analysis Completed!")
print("Shape:", df.shape)
print("\nSentiment Distribution:")
print(df['sentiment_label'].value_counts())
print("\nTheme Distribution:")
print(df['identified_theme'].value_counts())
print("\nFile saved: data/processed_reviews.csv")