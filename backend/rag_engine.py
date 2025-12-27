import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import subprocess
import json
import pickle

# Load FAISS index
faiss_index = faiss.read_index("data/faiss_index.bin")

# Load metadata
metadata = pickle.load(open("data/metadata.pkl", "rb"))


# Load product dataset
df = pd.read_csv("data/processed_amazon_products.csv")
df["title"] = df["title"].fillna("")
df["description"] = df["description"].fillna("")
df["category"] = df["category"].fillna("")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(text):
    return model.encode([text])[0].astype("float32")


def query_faiss(query, top_k=5):
    vector = embed(query)
    vector = np.array([vector]).astype("float32")

    distances, indices = faiss_index.search(vector, top_k)

    results = []

    for idx in indices[0]:
        row = df.iloc[idx]
        results.append({
            "asin": row["asin"],
            "title": row["title"],
            "description": row["description"],
            "category": row["category"]
        })

    return results


def ask_llama(prompt):
    """Send prompt to Ollama llama3 model."""
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout


def rag_answer(user_query):
    retrieved = query_faiss(user_query, top_k=5)

    context_str = json.dumps(retrieved, indent=2)

    prompt = f"""
You are an AI product expert for an e-commerce platform.

User query:
{user_query}

Relevant product data:
{context_str}

Using ONLY this information, give a helpful and concise answer.
"""

    return ask_llama(prompt)


if __name__ == "__main__":
    q = "best wireless headphones under 1000 rupees"
    print(rag_answer(q))
