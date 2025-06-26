from pymongo import MongoClient
import time

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["10M_db"]
collection = db["10M_data"]

# Drop previous data
collection.drop()

# Configuration
total_docs = 10_000_000
batch_size = 10_000  # Number of documents per batch
num_batches = total_docs // batch_size

# Sample data 
def generate_document(i):
    return {
        "user_id": i,
        "username": f"user_{i}",
        "email": f"user_{i}@example.com",
        "status": "active"
    }

# Insert loop
start_time = time.time()

for batch in range(num_batches):
    docs = [generate_document(i + batch * batch_size) for i in range(batch_size)]
    collection.insert_many(docs, ordered=False)  # use ordered=False for better performance

    if (batch + 1) % 10 == 0:
        elapsed = time.time() - start_time
        print(f"Inserted {(batch + 1) * batch_size} documents in {elapsed:.2f} seconds")

total_time = time.time() - start_time
print(f"\n Inserted {total_docs:,} documents in {total_time:.2f} seconds")
