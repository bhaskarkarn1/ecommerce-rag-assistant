import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

# Load dataset
df = pd.read_csv("data/processed_amazon_products.csv")

# Fill missing text fields
df["title"] = df["title"].fillna("")
df["description"] = df["description"].fillna("")
df["text"] = df["title"] + " " + df["description"]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert text → vectors
print("Embedding all Amazon products...")
embeddings = model.encode(df["text"].tolist(), batch_size=64, show_progress_bar=True)
embeddings = embeddings.astype("float32")

# Create FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)

print("Adding vectors to FAISS index...")
index.add(embeddings)

# Save FAISS index + metadata
faiss.write_index(index, "data/faiss_index.bin")
df[["asin", "title", "description", "category"]].to_pickle("data/metadata.pkl")

print("FAISS index created successfully!")
print("Total vectors stored:", index.ntotal)
