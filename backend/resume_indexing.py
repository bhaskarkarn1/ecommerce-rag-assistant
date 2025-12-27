import os
import pandas as pd
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from sentence_transformers import SentenceTransformer

load_dotenv()

# Connect to Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("amazon-products")

# Load processed Amazon product data
df = pd.read_csv("data/processed_amazon_products.csv")

# Clean metadata (Pinecone cannot store NaN)
df["title"] = df["title"].fillna("")
df["description"] = df["description"].fillna("")
df["category"] = df["category"].fillna("")
df["asin"] = df["asin"].fillna("")

# Prepare text field (title + description)
df["text"] = df["title"].astype(str) + " " + df["description"].astype(str)

# === Check which ASINs exist in Pinecone using metadata filter ===
existing_ids = set()

print("Checking existing vectors in Pinecone...")

for asin in df["asin"].tolist():
    try:
        result = index.query(
            vector=[0] * 384,    # dummy vector (384 dimensions)
            top_k=1,
            filter={"asin": asin}
        )
        if len(result.matches) > 0:
            existing_ids.add(asin)
    except Exception as e:
        print(f"Error checking {asin}: {e}")

print(f"Already in Pinecone: {len(existing_ids)} vectors")

# Determine missing ASINs
all_ids = set(df["asin"].tolist())
missing_ids = list(all_ids - existing_ids)

print(f"Missing vectors: {len(missing_ids)}")

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# === Upload missing vectors in small batches ===
batch_size = 1   # safest possible upload

for i, asin in enumerate(missing_ids):
    row = df[df["asin"] == asin].iloc[0]
    text = row["text"]

    # embed text
    vector = model.encode([text])[0].tolist()

    metadata = {
        "asin": row["asin"],
        "title": row["title"],
        "description": row["description"],
        "category": row["category"],
    }

    # upsert 1 item at a time (SAFE, NEVER FREEZES)
    index.upsert(vectors=[(asin, vector, metadata)])

    # progress update
    if i % 500 == 0:
        print(f"Uploaded {i} / {len(missing_ids)}")

print("✔ All missing vectors uploaded!")
