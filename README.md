# AI Document Assistant

A small RAG (Retrieval-Augmented Generation) backend. Upload a PDF, ask questions about it in natural language, and get answers grounded in the document with page citations.

Built as a learning project to understand how RAG works end to end, without relying on LangChain or similar frameworks.

## How it works

**Ingest:** the PDF is parsed page by page, split into overlapping chunks, embedded with a local sentence-transformers model, and stored in PostgreSQL with pgvector.

**Query:** the question is embedded with the same model, the closest chunks are retrieved by cosine distance, and they are passed to an LLM as context. The prompt instructs the model to answer only from that context — if the answer isn't there, it says so instead of guessing. The retrieved chunks are returned as sources with page numbers.

## Stack

Python 3.12, FastAPI, SQLAlchemy + Alembic, PostgreSQL + pgvector, PyMuPDF, sentence-transformers (`paraphrase-multilingual-MiniLM-L12-v2`, 384 dim), Google Gemini 2.5 Flash, pytest, Docker Compose.

## Running it

Requires Python 3.12, [uv](https://docs.astral.sh/uv/), Docker, and a Gemini API key ([free tier](https://aistudio.google.com/apikey)).

```bash
uv sync
cp .env.example .env          # then fill in GEMINI_API_KEY
docker compose up -d
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Interactive docs at `http://127.0.0.1:8000/docs`.

## API

```bash
# Upload a document
curl -X POST http://127.0.0.1:8000/documents -F "file=@document.pdf"

# Ask a question
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the supplier obligations?"}'
```

The query response contains the answer and the passages it was based on:

```json
{
  "answer": "The supplier is required to...",
  "sources": [
    { "document_id": "71037e43-...", "page": 6, "text": "..." }
  ]
}
```

If the answer isn't in the documents, the response is `"Tato informace se v dokumentech nenachází."` with no sources.

## Tests

```bash
uv run pytest
```

Covers chunking, prompt construction, and query orchestration. The LLM client is mocked through the `LLMClient` interface, so tests are deterministic and don't call the API.

## Design decisions

- **No LangChain.** The point was to understand the pipeline, not hide it behind an abstraction.
- **Local embeddings** instead of an embeddings API — free, private, and handles Czech. Slower on CPU, and PyTorch is a heavy dependency.
- **pgvector instead of a dedicated vector DB.** Metadata and vectors live in the same database, which keeps operations simple. A specialised store would offer more vector-specific features.
- **Provider abstractions** (`LLMClient`, `EmbeddingClient`) so Gemini can be swapped for a local model without touching the rest of the code.
- **Synchronous SQLAlchemy** — easier to reason about than async, at the cost of throughput.
- **Fixed-size chunking with overlap.** Simple and predictable, but it can cut through a sentence. Visible when a definition spans a chunk boundary.

## Limitations and next steps

- No relevance threshold — retrieval always returns the top-k chunks, even when none are relevant. Grounding is currently enforced by the prompt alone.
- Exact nearest-neighbour search. An HNSW or IVFFlat index would be needed at scale.
- Embeddings are generated in the request thread; this belongs in a background worker.
- No integration tests or CI yet.
- Scanned PDFs aren't handled (no OCR), and tables are extracted poorly.