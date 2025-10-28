# Machine Learning RAG System

**Candidate**: Daniel Mendoza  
**Interview Task**: End-to-end RAG pipeline for Machine Learning Wikipedia document

## Overview

Retrieval-Augmented Generation system that enables question-answering over a 40 page Machine Learning Wikipedia PDF using local LLMs.

**Key Components:**
- **Preprocessing**: Text extraction, noise removal, citation cleaning
- **Chunking**: RecursiveCharacterTextSplitter (700 chars, 150 overlap)
- **Embeddings**: nomic-embed-text via Ollama (768-dim vectors)
- **Vector Store**: ChromaDB (local, persistent)
- **Generator**: Llama 3.2:3b via Ollama

**Total Chunks**: 126 from 66K characters of cleaned text

---

## Prerequisites

- Python 3.8+
- Ollama installed ([https://ollama.com](https://ollama.com))
- 8GB+ RAM recommended

---

## Setup

### 1. Install Dependencies
```bash
pip install chromadb ollama langchain-text-splitters PyMuPDF
```

### 2. Pull Ollama Models
```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

### 3. Verify Ollama Running
```bash
ollama list
```

---

## Usage

### Run Complete Pipeline
```bash
# 1. Preprocess PDF (output: ml_clean.txt)
python data_preprocessing.py

# 2. Create chunks
python chunking.py

# 3. Generate embeddings and store in ChromaDB
python embedding_storage.py

# 4. Query the RAG system
python RAG.py
```

### Query Examples
The system can answer questions like:
- "Who coined the term 'machine learning'?"
- "What is Tom M. Mitchell's definition of machine learning?"
- "What was the 'Cybertron' machine developed by Raytheon Company in the 1960s?"


## Project Structure
```
├── data_preprocessing.py          # PDF → clean text extraction
├── chunking.py              # Text → 126 semantic chunks
├── embedding_storage.py     # Chunks → vector embeddings → ChromaDB
├── RAG.py                   # Query → retrieve → generate pipeline
├── data.ml_clean.txt             # Preprocessed document (66K chars)
├── data/chunks.json              # 126 text chunks with metadata
└── chroma_db/               # Persistent vector database
```
