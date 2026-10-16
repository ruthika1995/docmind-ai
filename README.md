# DocMind AI — Enterprise Document Intelligence & Grounded RAG Platform

> **Modern Intelligent Document Processing (IDP)** powered by an **OpenRouter AI Gateway**, **Decoupled Local Vector Embeddings**, and the **Impeccable Design System**.

---

## 🏛️ System Architecture

```text
                         [ Browser / User ]
                                │
                                ▼
                   ┌──────────────────────────┐
                   │    Frontend (Vercel)     │
                   │ React 19 + TS + Impeccable│
                   └────────────┬─────────────┘
                                │ HTTPS / SSE Streaming
                                ▼
                   ┌──────────────────────────┐
                   │    Backend (Render)      │
                   │     FastAPI Python       │
                   └──────┬────────────┬──────┘
                          │            │
            ┌─────────────┴─────┐      └──────────────┐
            ▼                   ▼                     ▼
┌───────────────────────┐ ┌───────────────┐ ┌──────────────────┐
│   OpenRouter Gateway  │ │ Vector Engine │ │  PostgreSQL /    │
│  Llama 3.3 / Gemini   │ │  Decoupled    │ │     pgvector     │
│  DeepSeek / Mistral   │ │  384-Dim Dense│ │  (Supabase / DB) │
└───────────────────────┘ └───────────────┘ └──────────────────┘
```

---

## ⚡ Core Principles & Architectural Decisions

### 1. Centralized AI Service Layer (`backend/app/ai/`)
- **No Direct Frontend LLM Calls**: Frontend communicates exclusively with the FastAPI backend. API keys never leak to browser bundles.
- **Model Agnostic**: Configurable via `OPENROUTER_MODEL` (e.g. `meta-llama/llama-3.3-70b-instruct:free`, `google/gemini-2.0-flash-001`, `deepseek/deepseek-chat`). Swapping models requires zero code refactoring.
- **Offline Heuristic Fallback**: Includes a built-in deterministic simulator when API keys are unset or network quotas are exceeded, ensuring demonstrations and interviews never crash.

### 2. Provider Separation (LLM $\ne$ Embeddings)
- **Decoupled Embedding Engine**: Generates 384-dimensional dense semantic vectors locally.
- **Zero API Quota Spend on Indexing**: High-volume PDF ingestion never consumes OpenRouter model tokens.
- **Cosine Distance Vector Search**: Indexed natively with `pgvector` in production (and SQLite dense vectors in local dev).

### 3. Impeccable Design Standard ([impeccable.style](http://impeccable.style/))
- **No AI Slop Tells**: Eliminates unnecessary diffuse neon halos, pastel blob backgrounds, status-chip soup, and nested card slop.
- **Kinpaku Ink Surfaces**: Deep obsidian surfaces (`--ks-bg: #0b0d13`, `--ks-surface-1: #11141d`, `--ks-surface-sunken: #0c0e15`).
- **Tactile Hierarchy**: Segmented instrument strips, crisp structural borders (`rgba(255, 255, 255, 0.08)`), and high-contrast typographic pairings (`Albert Sans` + `JetBrains Mono`).

---

## 🚀 5 Core Document Capabilities

| Module | Input | AI Processing | Structured Output |
|---|---|---|---|
| **1. Classification** | PDF / DOCX / TXT | OpenRouter few-shot taxonomy classifier | Category (Invoice, Contract, Resume, Financial Report, Research Paper) + Confidence % + Reason |
| **2. Structured Extraction** | Invoices, Contracts, Resumes | Schema-validated JSON mode | Clean JSON schemas (totals, line items, parties, liabilities, skills, experience) |
| **3. Summarization** | Multi-page text | Hierarchical synthesis | Executive summary, key bullet takeaways, TL;DR, and action items |
| **4. Comparison & Diff** | Document A vs Document B | Clause alignment & divergence audit | Side-by-side clause breakdown (Modified, Added, Removed), risk ratings, and legal guidance |
| **5. Grounded RAG Chat** | User natural language query | Semantic vector search $\to$ Grounded LLM | Multi-turn streaming conversation with verified chunk citations `[Chunk X \| Page Y]` |

---

## 🛠️ Project Structure

```text
docmind-ai/
├── backend/
│   ├── app/
│   │   ├── config.py             # Environment settings
│   │   ├── database.py           # SQLAlchemy & vector connection
│   │   ├── models/               # Document, DocumentChunk, Comparison, Chat
│   │   ├── schemas/              # Pydantic v2 validation models
│   │   ├── services/
│   │   │   ├── document_parser.py # PDF/DOCX chunker & embedder
│   │   │   └── sample_data.py    # Pre-seeded enterprise datasets
│   │   ├── api/v1/
│   │   │   ├── documents.py      # Upload, list, delete, seed
│   │   │   ├── extract.py        # Structured JSON extraction
│   │   │   ├── compare.py        # Contract & clause diffing
│   │   │   ├── rag.py            # Grounded Q&A with citations
│   │   │   └── health.py         # Gateway connectivity check
│   │   └── ai/
│   │       ├── openrouter_client.py # Central LLM gateway client
│   │       ├── embeddings.py        # Decoupled 384-dim dense embedder
│   │       ├── classifier.py        # Document taxonomy engine
│   │       ├── extractor.py         # JSON schema extractor
│   │       ├── summarizer.py        # Multi-format synthesizer
│   │       ├── comparator.py        # Dual-document diff engine
│   │       └── rag.py               # Grounded retrieval assistant
│   ├── tests/
│   │   └── test_api.py           # Pytest test suite
│   ├── requirements.txt
│   └── run.py                    # Local server launcher
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Navbar.tsx           # Instrument strip header
    │   │   ├── WorkspaceView.tsx    # Library, upload dropzone, KPIs
    │   │   ├── ExtractionStudio.tsx # Side-by-side JSON schema extractor
    │   │   ├── CompareView.tsx      # Contract divergence matrix
    │   │   ├── RAGChatView.tsx      # Grounded chat with citation drawer
    │   │   └── ConfigView.tsx       # Architecture & gateway settings
    │   ├── services/api.ts          # Backend API client
    │   ├── types/index.ts           # Shared TypeScript interfaces
    │   └── index.css                # Impeccable CSS design system
    ├── package.json
    ├── vercel.json                  # Vercel deployment config
    └── vite.config.ts
```

---

## 🏃 Local Quickstart

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run test suite
PYTHONPATH=. pytest tests/test_api.py

# Launch development server
python run.py
# Backend runs at http://localhost:8000 (Swagger docs: http://localhost:8000/docs)
```

### 2. Frontend Setup
```bash
cd frontend
npm ci
npm run dev
# Frontend runs at http://localhost:5173
```

---

## 🚢 Free Production Deployment

1. **Backend (Render)**:
   - Create a Web Service connected to your repository.
   - Root directory: `.`
   - Build command: `cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt`
   - Start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Set environment variables: `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`.

2. **Frontend (Vercel)**:
   - Import repository on Vercel.
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment Variable: `VITE_API_URL=https://your-backend.onrender.com/api/v1`

---

## 🎯 Key Interview Talking Points for Ruthi

1. **Why use OpenRouter as an AI Gateway?**
   - Single unified endpoint to access over 100+ models (Meta Llama 3.3, Google Gemini Flash, DeepSeek, Mistral).
   - Zero vendor lock-in: models can be benchmarked and swapped with an environment variable.
   - Security: Keeps credentials strictly on the backend, preventing client-side API key exposure.

2. **Why decouple LLM inference from vector embeddings?**
   - Ingestion cost control: indexing 10,000 PDF pages does not consume expensive LLM tokens.
   - High availability: if an external LLM gateway experiences latency, vector indexing and retrieval continue running uninterrupted.

3. **Why PostgreSQL + pgvector?**
   - Eliminates the operational fragmentation and licensing cost of standalone vector databases (Pinecone, Milvus).
   - Enables hybrid transactional and vector queries in a single ACID-compliant database.
