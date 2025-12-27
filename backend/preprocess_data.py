import json
import gzip
import pandas as pd
from collections import Counter

# ---------- PROCESS AMAZON METADATA ----------
def process_amazon_metadata():
    input_path = "data/meta_Electronics.json.gz"
    output_path = "data/processed_amazon_products.csv"

    products = []

    with gzip.open(input_path, 'rt', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)

            products.append({
                "asin": item.get("asin"),
                "title": item.get("title"),
                "description": " ".join(item.get("feature", [])) if item.get("feature") else None,
                "category": " > ".join(item.get("categories")[0]) if item.get("categories") else None,
                "price": item.get("price")
            })

    df = pd.DataFrame(products)
    df.dropna(subset=["title"], inplace=True)
    df.to_csv(output_path, index=False)

    print("Saved:", output_path)


# ---------- PROCESS INSTACART DATA ----------
def process_instacart():
    products = pd.read_csv("data/products.csv")
    orders = pd.read_csv("data/orders.csv")
    order_prior = pd.read_csv("data/order_products__prior.csv")

    # Merge prior orders with order info
    merged = order_prior.merge(orders, on="order_id")

    # Top-selling (popularity)
    popularity = merged["product_id"].value_counts().reset_index()
    popularity.columns = ["product_id", "purchase_count"]

    # Frequently bought together (simple co-occurrence counts)
    co_occurrence = Counter()

    for order_id, group in merged.groupby("order_id"):
        items = list(group["product_id"])
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                pair = tuple(sorted((items[i], items[j])))
                co_occurrence[pair] += 1

    co_df = pd.DataFrame([
        {"product_1": k[0], "product_2": k[1], "count": v}
        for k, v in co_occurrence.items()
    ])

    popularity.to_csv("data/instacart_popularity.csv", index=False)
    co_df.to_csv("data/instacart_cooccurrence.csv", index=False)

    print("Saved Instacart popularity + co-occurrence.")


# ---------- RUN BOTH ----------
if __name__ == "__main__":
    print("Processing Amazon metadata...")
    process_amazon_metadata()

    print("Processing Instacart data...")
    process_instacart()
