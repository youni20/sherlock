# Sherlock

**A RAG assistant for a detective's case files where answers grounded in the evidence, never guesses.**

Upload `.txt` or `.pdf` case files, then ask questions like *"What was Mrs. Hudson's
alibi?"*. Sherlock answers only from what's actually written in the files and cites
the sources it used. If the evidence isn't there, it says so rather than making
something up:

> I don't have enough evidence to answer that.

---

## What it does

- **Upload case files** — `.txt` or `.pdf`, added to a searchable knowledge base
- **Ask questions** — an LLM answers using RAG (retrieval-augmented generation) over your files
- **Cites its sources** — every answer lists which case files it came from
- **Knows when to stop** — abstains instead of guessing when the files don't hold the answer

---

## Tech stack

- **Backend:** Python 3.12 + FastAPI, served by uvicorn
- **RAG & LLM:** LangChain, Chroma vector store, Google Gemini (embeddings + generation), pypdf
- **Frontend:** vanilla HTML, CSS, and JavaScript
- **Infrastructure:** Docker + Docker Compose, with uv for dependency management

---

## Getting started

### 1. Get a free API key

Create one at **[Google AI Studio](https://aistudio.google.com/apikey)** — sign in
with a Google account and click **Create API key**. It's free, no billing required.

### 2. Add the key to a `.env` file

```bash
cp .env_example .env
```

Then open `.env` and paste your key:

```
GEMINI_API_KEY=your-key-here
```

### 3. Run it

```bash
docker compose up --build
```

Open **http://localhost:8080** in your browser and start asking questions.

Uploaded files and embeddings persist between restarts (stored in `./case_files`
and `./chroma_vector_store`).

### Running without Docker

Needs Python 3.12+ and [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run uvicorn main:app --app-dir src --port 8080 --reload
```

---

## API endpoints

| Method | Path            | Description                                |
|--------|-----------------|--------------------------------------------|
| GET    | `/`             | Web frontend                               |
| GET    | `/health`       | Health check                               |
| POST   | `/ingest_file`  | Upload a `.txt` or `.pdf` case file        |
| POST   | `/get_answer`   | Ask a question; returns `{answer, sources}`|
| GET    | `/get_files`    | List uploaded case files                   |
| DELETE | `/delete_files` | Delete all files and wipe the vector store |

**Example — ask a question:**

```bash
curl -X POST http://localhost:8080/get_answer \
  -H "Content-Type: application/json" \
  -d '{"question": "What was Mrs. Hudson'\''s alibi?"}'
```

---

## Tests

The suite is split into fast offline tests (no API key, safe for CI) and opt-in
integration tests that call the live Gemini API.

```bash
uv run pytest                 # offline unit tests (no API key needed)
uv run pytest -m integration  # live tests against the Gemini API (needs a key)
```

What's covered:

- **`test_ingestion.py`** — text chunking and document loading, including the
  missing-file and unsupported-type errors *(offline)*
- **`test_offline.py`** — the `/get_answer` source-parsing logic and bad-extension
  rejection, with Gemini and Chroma mocked out *(offline)*
- **`test_api.py`** — endpoint smoke tests for the frontend and `/get_files`, plus
  live ingest/answer checks *(mixed)*
- **`test_grounding.py`** — the core guarantee: answerable questions return the
  right facts, and unanswerable ones return the exact abstention sentence
  *(integration)*

---

## How answers stay grounded

Grounding is enforced entirely by the system prompt. Sherlock:

- answers only from the retrieved text, and cites the files it used
- won't complete fragmentary or redacted text (e.g. a torn `...HAMPTON`)
- won't name a culprit from motive or opportunity alone — only a direct statement counts
- abstains when the files don't answer the question

Gemini's safety filters are set to `BLOCK_NONE` so it can discuss crime details in
the case files; grounding comes from the prompt, not the filter. Models used:
`gemini-embedding-001` (embeddings) and `gemini-2.5-flash-lite` (answers).

---

## Architecture & Data Flow

The diagram below traces a request end to end — the browser hits the FastAPI app,
which runs the RAG pipeline (load → chunk → embed → store on ingest; retrieve →
ground → generate on a question) and returns a sourced answer

![Sherlock architecture and data-flow diagram](docs/diagrams/architecture_diagrams/white_architecture_diagram.png)

---

## Further reading

For a deeper write-up of the architecture, grounding strategy, and design
trade-offs, see the full report at [`docs/report.pdf`](docs/report.pdf).
