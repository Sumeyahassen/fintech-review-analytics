import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get database credentials
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT', '5432')

# Check if password is loaded
if not DB_PASSWORD:
    raise Exception("❌ Missing DB_PASSWORD. Check your .env file!")

print("✅ .env file loaded successfully!")
print(f"Connecting to database: {DB_NAME} as user {DB_USER}")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)
cur = conn.cursor()

print("✅ Connected to PostgreSQL successfully!")

# ========================= CREATE TABLES =========================
cur.execute("""
    DROP TABLE IF EXISTS reviews CASCADE;
    DROP TABLE IF EXISTS banks CASCADE;

    CREATE TABLE banks (
        bank_id SERIAL PRIMARY KEY,
        bank_name VARCHAR(100) UNIQUE NOT NULL,
        app_name VARCHAR(200)
    );

    CREATE TABLE reviews (
        review_id SERIAL PRIMARY KEY,
        bank_id INTEGER REFERENCES banks(bank_id),
        review_text TEXT,
        rating INTEGER,
        review_date DATE,
        sentiment_label VARCHAR(20),
        sentiment_score FLOAT,
        identified_theme VARCHAR(100),
        source VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

print("✅ Tables created successfully!")

# ========================= INSERT DATA =========================
df = pd.read_csv('data/cleaned_reviews.csv')

# Insert Banks first
banks = df['bank'].unique()
for bank in banks:
    cur.execute("""
        INSERT INTO banks (bank_name) 
        VALUES (%s) 
        ON CONFLICT (bank_name) DO NOTHING
    """, (bank,))

# Get bank_id mapping
cur.execute("SELECT bank_name, bank_id FROM banks")
bank_map = dict(cur.fetchall())

# Prepare data for reviews
data = []
for _, row in df.iterrows():
    data.append((
        bank_map[row['bank']],
        row['review'],
        int(row['rating']),
        row['date'],
        None,   # sentiment_label (you can add later)
        None,   # sentiment_score
        None,   # identified_theme
        row['source']
    ))

# Insert reviews in batch (fast)
execute_values(cur, """
    INSERT INTO reviews 
    (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme, source)
    VALUES %s
""", data)

conn.commit()
print(f"✅ Successfully inserted {len(data)} reviews into the database!")

# Show summary
cur.execute("SELECT b.bank_name, COUNT(*) FROM reviews r JOIN banks b ON r.bank_id = b.bank_id GROUP BY b.bank_name")
print("\nReviews per bank in database:")
for row in cur.fetchall():
    print(f"   {row[0]}: {row[1]} reviews")

cur.close()
conn.close()