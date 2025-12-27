import os
import pandas as pd
from pinecone.grpc import PineconeGRPC as Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("amazon-products")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dimensional embeddings


def build_pinecone_index():
    df = pd.read_csv("data/processed_amazon_products.csv")

    # Create the text for embedding (title + description)
    df["text"] = df["title"].astype(str) + " " + df["description"].astype(str)

    vectors = model.encode(df["text"].tolist(), batch_size=64, show_progress_bar=True)

    # Prepare records for upsert
    records = []
    for i, row in df.iterrows():
        vector = vectors[i].tolist()
        metadata = {
            "asin": row["asin"],
            "title": row["title"],
            "description": row["description"],
            "category": row["category"],
        }

        records.append((row["asin"], vector, metadata))

        # Upload in batches of 100
        if len(records) == 100:
            index.upsert(vectors=records)
            records = []

    # Upload remaining records
    if records:
        index.upsert(vectors=records)

    print("Pinecone index built successfully!")


if __name__ == "__main__":
    build_pinecone_index()
