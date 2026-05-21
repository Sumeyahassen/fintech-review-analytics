# Fintech Review Analytics

Project for analyzing Google Play Store reviews for Ethiopian Banks (CBE, BOA, Dashen).

## Task 1: Data Collection & Preprocessing

### Methodology
- Used `google-play-scraper` library
- Language: English (`lang='en'`)
- Country: Ethiopia (`country='et'`)
- Sort: Newest
- Total Raw Reviews Collected: **3200**

### Final Cleaned Data
- Total Clean Reviews: **~3100+** (after removing duplicates & missing values)
- CBE: ~1500+
- BOA: ~580+
- Dashen: ~580+

### Files
- Raw data: `data/raw/raw_reviews.csv` (ignored by git)
- Cleaned data: `data/cleaned_reviews.csv` (ignored by git)

### How to Run
```bash
python scripts/scrape_reviews.py
python scripts/preprocess.py
## Task 2: Sentiment Analysis & Thematic Analysis

### Objective
To perform sentiment analysis on customer reviews and identify key business themes using Natural Language Processing (NLP).

### Methodology
- **Sentiment Model**: Used `distilbert-base-uncased-finetuned-sst-2-english` (DistilBERT Transformer model)
- **Theme Detection**: Implemented custom rule-based keyword mapping for business-relevant themes
- **Output Format**: Saved results with columns: `review_id`, `review`, `sentiment_label`, `sentiment_score`, `identified_theme`

### Results

- **Total Reviews Analyzed**: 2,736
- **Sentiment Distribution**:
  - Positive: **1,686** (61.6%)
  - Negative: **1,050** (38.4%)

- **Top Themes Identified**:
  - Positive Feedback: 945
  - Transaction Problems: 124
  - Account Access Issues: 117
  - Performance Issues: 90
  - UI/UX Experience: 43
  - Customer Support: 27

### Insights
- Majority of users have a **positive** experience with the fintech application.
- Main areas of concern are **Transaction Problems** and **Account Access Issues**.
- These findings can help the product team prioritize improvements.

### Visualizations
- Sentiment Distribution (Pie Chart)
- Top Themes Distribution (Bar Chart)

### Files & Deliverables
- **Script**: `scripts/sentiment_analysis.py`
- **Processed Data**: `data/processed/processed_reviews.csv`
- **Charts**: `images/sentiment_distribution.png`, `images/top_themes.png`

### Tool Selection Rationale
DistilBERT was selected over traditional tools (TextBlob/VADER) because it provides better context understanding and higher accuracy for customer feedback analysis.
## Task 3: Database Engineering

- Database: PostgreSQL (`bank_reviews`)
- Tables Created: `banks` and `reviews`
- Total Records Inserted: **2736 reviews**
- Used `psycopg2` + `SQLAlchemy` style batch insert
- Successfully linked reviews with their respective banks