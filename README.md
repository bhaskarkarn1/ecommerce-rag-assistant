## Problem Motivation
Large language models often hallucinate or provide incomplete answers when answering domain-specific queries such as product search. Retrieval-Augmented Generation (RAG) is commonly used to ground LLM responses in external data, but its behavior under real-world e-commerce queries is not well understood.

## Research Questions
This project explores:
1. How much does retrieval improve answer quality compared to using an LLM alone?
2. How sensitive is RAG performance to retrieval parameters such as top-k and chunk size?
3. What types of queries cause RAG systems to fail or partially hallucinate?

## System Overview
We implement a standard RAG pipeline consisting of:
- Dense retrieval using sentence embeddings
- FAISS-based vector search over a large product catalog
- LLM-based response generation conditioned on retrieved context

## Experimental Setup
- Dataset: ~780K Amazon product entries
- Embedding model: all-MiniLM-L6-v2 (384-d)
- Vector index: FAISS IndexFlatL2
- LLM: Llama-3 via Ollama
- Queries: Manually curated set of real-world e-commerce queries

## Experiments
We compare:
- LLM-only responses (no retrieval)
- RAG with varying top-k values (k = 3, 5, 10)

Evaluation is performed via qualitative analysis of relevance, grounding, and hallucination.

## Observations
- Retrieval significantly reduces hallucinations for factual queries.
- Increasing top-k improves recall but often introduces noisy context.
- Ambiguous price-based queries remain challenging.

## Error Analysis
Common failure modes include:
- Retrieval of semantically similar but irrelevant products
- Partial answers when product attributes are missing
- Overconfident responses for under-specified queries

## Limitations
- Evaluation is qualitative and limited in scale
- Single-domain (e-commerce) dataset
- English-only queries

## Future Work
- Multilingual product catalogs (Indic languages)
- Lightweight automatic evaluation metrics
- Hybrid sparse + dense retrieval
