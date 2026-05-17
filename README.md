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