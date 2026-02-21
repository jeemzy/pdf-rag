# PDF RAG Application

A full-stack **Retrieval-Augmented Generation (RAG)** app for asking questions against your own PDF documents. Upload PDFs, organize them into collections, and chat with an AI that answers based strictly on your document content.

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React + Vite + Shadcn UI (TypeScript) |
| **Backend** | FastAPI (Python) |
| **RAG** | LangChain + OpenAI Embeddings (`text-embedding-ada-002`) |
| **Vector Store** | Qdrant |
| **Orchestration** | Docker Compose |
| **CI** | GitHub Actions |

## Architecture

```
┌──────────────┐     HTTP      ┌──────────────┐     gRPC     ┌─────────┐
│   Frontend   │ ────────────► │   Backend    │ ───────────► │ Qdrant  │
│  (port 5173) │               │  (port 8000) │              │ (6333)  │
└──────────────┘               └──────────────┘              └─────────┘
                                      │
                                      │ OpenAI API
                                      ▼
                               text-embedding-ada-002
                               gpt-4o-mini (chat)
```

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js 20+](https://nodejs.org/) and [pnpm](https://pnpm.io/) (for local frontend dev)
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/jeemzy/pdf-rag.git
   cd pdf-rag
   ```

2. **Create your `.env` file** in the project root:
   ```env
   OPENAI_API_KEY=sk-proj-...
   ```

3. **Start all services**
   ```bash
   docker compose up -d --build
   ```

   This starts:
   - `backend` at `http://localhost:8000`
   - `qdrant` at `http://localhost:6333`

4. **Start the frontend** (dev server):
   ```bash
   cd frontend
   pnpm install
   pnpm run dev
   ```
   Open `http://localhost:5173` in your browser.

## Usage

1. **Create a collection** — Click **New Collection** in the sidebar and give it a name.
2. **Upload a PDF** — Select the collection, then click **Upload PDF**. The backend will chunk and embed the document automatically.
3. **Chat** — Select your collection and ask questions in the chat interface. The AI will answer based solely on your documents.

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/collections/` | List all collections |
| `POST` | `/collections/` | Create a new collection |
| `DELETE` | `/collections/{name}` | Delete a collection |
| `POST` | `/documents/upload` | Upload & embed a PDF |
| `POST` | `/chat/` | Ask a question against a collection |

Interactive API docs: `http://localhost:8000/docs`

## Project Structure

```
pdf-rag/
├── backend/
│   ├── api/
│   │   ├── routes_chat.py          # POST /chat/
│   │   ├── routes_collections.py   # Collection CRUD
│   │   └── routes_documents.py     # PDF upload & embedding
│   ├── services/
│   │   ├── qdrant_service.py       # Qdrant client wrapper
│   │   └── rag_service.py          # LangChain RAG pipeline
│   ├── core/config.py              # Pydantic settings
│   ├── main.py                     # FastAPI app entry point
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.tsx
│       ├── lib/api.ts              # Typed HTTP client
│       └── components/
│           ├── AppSidebar.tsx
│           ├── ChatInterface.tsx
│           ├── NewCollectionDialog.tsx
│           └── UploadDocumentDialog.tsx
├── docker-compose.yml
├── .github/workflows/ci.yml       # Build verification CI
└── .env                           # Not committed — add your own
```

## CI/CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push to `main` and verifies:
- Docker Compose configuration is valid
- Docker images build successfully
- Frontend TypeScript compiles without errors

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ | Your OpenAI API key |
| `QDRANT_HOST` | Set by Docker | Qdrant hostname (default: `qdrant`) |
| `QDRANT_PORT` | Set by Docker | Qdrant port (default: `6333`) |

## License

MIT