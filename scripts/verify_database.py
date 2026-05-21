import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)
cur = conn.cursor()

print("📊 DATABASE VERIFICATION")
print("="*50)

# Total reviews
cur.execute("SELECT COUNT(*) FROM reviews")
print(f"Total Reviews: {cur.fetchone()[0]}") # type: ignore

# Reviews per bank
cur.execute("""
    SELECT b.bank_name, COUNT(*) as review_count, AVG(r.rating) as avg_rating
    FROM reviews r 
    JOIN banks b ON r.bank_id = b.bank_id 
    GROUP BY b.bank_name
""")
print("\nReviews per Bank:")
for row in cur.fetchall():
    print(f"   {row[0]:<10}: {row[1]} reviews | Avg Rating: {row[2]:.2f}")

cur.close()
conn.close()