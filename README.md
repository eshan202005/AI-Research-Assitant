# AI Research Assistant

A Retrieval-Augmented Generation (RAG) application built using **LangChain, FastAPI, Streamlit, ChromaDB, and OpenAI**. The project is designed as a hands-on AI Engineering learning project focused on understanding production-style architectures, retrieval systems, vector databases, and modern LLM workflows.

---

## Features

* Multi-PDF document ingestion
* Cross-document question answering
* OpenAI Embeddings (`text-embedding-3-small`)
* ChromaDB vector database
* FastAPI backend with REST APIs
* LangChain LCEL-based RAG pipeline
* MMR (Max Marginal Relevance) retrieval
* Metadata-aware document processing
* Persistent chat history using Streamlit Session State
* Modular service-based architecture

---

## Architecture

```text
Streamlit Frontend
        ↓ HTTP
FastAPI Backend
        ↓
RAG Pipeline (LangChain LCEL)
        ↓
ChromaDB
        ↓
OpenAI
```

### RAG Workflow

```text
PDF Upload
    ↓
Load Documents
    ↓
Split into Chunks
    ↓
Generate Embeddings
    ↓
Store in ChromaDB
    ↓
Retrieve Relevant Chunks (MMR)
    ↓
Generate Response with LLM
```

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI
* Pydantic

### AI & RAG

* LangChain
* LCEL
* OpenAI
* ChromaDB

### Document Processing

* PyPDFLoader
* RecursiveCharacterTextSplitter

---

## Project Structure

```text
ai-research-assistant/

├── backend/
│   ├── main.py
│   ├── models.py
│   └── services/
│       └── rag_service.py
│
├── frontend/
│   └── app.py
│
├── ingest.py
├── uploads/
├── chroma_db/
├── requirements.txt
├── .env
└── .gitignore
```

---

## Current Capabilities

### Multi-PDF Support

Upload multiple PDF files and create a single searchable knowledge base.

```text
PDF 1
PDF 2
PDF 3
    ↓
Combined Knowledge Base
```

---

### Metadata Tracking

Each document stores metadata such as:

```python
{
    "source": "filename.pdf"
}
```

This metadata is preserved through:

```text
Loading
↓
Chunking
↓
Embedding
↓
Storage
↓
Retrieval
```

and enables future source citations.

---

### MMR Retrieval

Uses Max Marginal Relevance (MMR) retrieval:

```python
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10
    }
)
```

Benefits:

* Reduced duplicate chunks
* Improved context diversity
* Better cross-document retrieval

---

## API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "message": "AI Research Assistant Backend Running"
}
```

---

### Upload PDFs

```http
POST /upload
```

Accepts:

```text
Multiple PDF Files
```

Returns:

```json
{
  "message": "PDFs processed successfully",
  "pages": 10,
  "chunks": 45
}
```

---

### Chat

```http
POST /chat
```

Request:

```json
{
  "question": "What are the key skills mentioned?"
}
```

Response:

```json
{
  "answer": "..."
}
```

---

## Setup

### Clone Repository

```bash
git clone <repository-url>
cd ai-research-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

---

## Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

## Run Frontend

```bash
streamlit run frontend/app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## Learning Objectives

This project is being built to gain practical experience with:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* LangChain LCEL
* FastAPI
* LLM Application Architecture
* Metadata Handling
* Semantic Search
* AI Engineering Workflows

---

## Roadmap

### Phase 1 ✅ Completed

* PDF Upload
* Chunking
* Embeddings
* ChromaDB
* Basic RAG
* Streamlit UI

### Phase 2 ✅ Completed

* FastAPI Backend
* Multi-PDF Support
* Metadata Tracking
* MMR Retrieval
* Modular Service Architecture

### Phase 3 🚀 Next

* LangGraph Fundamentals
* Graph-Based RAG Workflow
* State Management
* Nodes and Edges

### Future Enhancements

* Source Citations
* Router-Based Workflows
* General LLM + RAG Routing
* Reflection Loops
* Multi-Agent Systems

---

## Status

Current Version:

```text
Phase 2 Complete ✅
```

Next Milestone:

```text
LangGraph Integration 🚀
```
