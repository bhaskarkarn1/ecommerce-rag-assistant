# 🛒 AI E-Commerce Shopping Assistant (RAG-based)

An AI-powered **E-Commerce Product Recommendation Assistant** that understands **natural language queries** and returns **relevant product suggestions** using **vector search + LLMs**.

Built to handle **large-scale datasets (~7.8 lakh products)** efficiently using a **Retrieval-Augmented Generation (RAG)** pipeline.

---

## 🚀 Features

- 🔍 Natural language product search (e.g. *"best headphones under 1000"*)
- ⚡ Ultra-fast similarity search using **FAISS**
- 🧠 Context-aware recommendations via **Llama-3 (Ollama)**
- 🎯 Accurate results grounded in real product data (no hallucinations)
- 🖥️ Clean, modern **Streamlit UI**
- 🔌 Decoupled backend using **FastAPI**

---

## 🧠 System Architecture (RAG Pipeline)


This is the same architecture used in **modern AI search systems** (ChatGPT RAG, Amazon recommendations, enterprise AI assistants).

---

## 🛠️ Tech Stack

### Backend
- **Python**
- **FAISS** – Fast vector similarity search
- **Sentence Transformers** (`all-MiniLM-L6-v2`)
- **FastAPI** – API server
- **Ollama (Llama-3)** – Local LLM inference
- **Pandas** – Data preprocessing

### Frontend
- **Streamlit**
- Custom CSS (dark theme, product cards, icons)

### Other
- **Git & GitHub**
- `.gitignore` for large files

---

## 📊 Dataset

- ~ **7,80,000 Amazon products**
- Product titles, descriptions, categories
- Missing values handled during preprocessing

### Data Cleaning Steps
- Removed invalid rows
- Filled missing titles/descriptions
- Combined text fields for better embeddings
- Saved processed CSV for indexing

---

## 📦 Vector Store (FAISS)

- Embedding Model: `all-MiniLM-L6-v2` (384-dim)
- Index Type: `IndexFlatL2`
- Stored locally as:



- Batched embedding generation for memory efficiency

---

## 🔌 API Design (FastAPI)

### Endpoint




### Input
```json
{
  "question": "best laptop under 50000"
}

uvicorn backend.api:app --reload
