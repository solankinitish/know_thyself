# KnowThyself
<img width="800" height="450" alt="KnowThyself_demo" src="https://github.com/user-attachments/assets/cdc04ef9-b3e7-4b54-bedd-32bb39cb156f" />


![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-yellow)
![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-purple)
![Groq](https://img.shields.io/badge/LLM-Groq%2FLlama3.1-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![GCP](https://img.shields.io/badge/Cloud-Google%20Cloud%20Run-red)
![License](https://img.shields.io/badge/MIT-License-lightgrey)

KnowThyself is a **stateful multi-track AI coaching system** built from first principles.
It remembers who you are across sessions, ingests your structured data, runs classical ML on it, and gives grounded, evidence-based coaching — across Fitness, Habits, and Relationships.

---

## What This Project Demonstrates

- Building a **stateful LLM coaching system** with persistent cross-session memory
- **Two-layer memory architecture** — session memory for precision, Pinecone for long-term recall
- **Classical ML grounding** — LinearRegression, K-Means, Z-score, distilBERT injected into LLM prompts
- **Multi-track OOP design** — BaseTrack polymorphism with track-specific ML and summarization
- **Production deployment** — Dockerized, deployed on Google Cloud Run with GCS persistence
- **Cloud LLM integration** — Groq (Llama 3.1 8B) with Ollama local fallback

---

## Features

- **Three coaching tracks** — Fitness, Habits/Productivity, Relationships — each with distinct personas and ML layers
- **Persistent memory** — Pinecone stores session summaries with recency boost retrieval
- **ML-grounded coaching** — "your squat is improving at 2.87kg/session" not "keep it up"
- **Auto-summarization** — LLM generates structured summaries every N exchanges, stored in Pinecone
- **Lazy model loading** — ML models load on first use, not on startup — Cloud Run compatible
- **GCS data persistence** — workout and habit CSVs survive container restarts
- **Streamlit frontend** — login, track selection, chat interface, tabular data entry forms
- **Domain grounding** — each coach stays strictly within its track; off-topic questions redirected to coaching goals

---

## Tech Stack

| Component | Technology |
|---|---|
| API | FastAPI, Uvicorn |
| Frontend | Streamlit |
| LLM | Groq (Llama 3.1 8B), Ollama/Mistral fallback |
| Orchestration | LangChain (ChatGroq, ChatOllama, ChatPromptTemplate) |
| Memory | ConversationSummaryBufferMemory (session), Pinecone (persistent) |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| ML | scikit-learn (LinearRegression, KMeans), scipy (Z-score), HuggingFace (distilBERT) |
| Storage | Google Cloud Storage (CSV persistence) |
| Containerization | Docker, docker-compose |
| Cloud | Google Cloud Run, Google Container Registry |
| Language | Python 3.11 |

---

## Architecture

```
User Message (Streamlit)
│
▼
POST /chat (FastAPI)
│
▼
CoachingService        — orchestrator, routes to correct track
│
▼
BaseTrack.respond()
├── PersistentMemory.retrieve()  — Pinecone semantic search + recency boost
├── get_insights()               — ML insights (lazy loaded)
└── SessionMemory.get_history()  — current session context
│
▼
ChatPromptTemplate
[system | ML insights | session history | past memories | human message]
│
▼
LLMClient.generate()   — Groq primary → Ollama fallback → ValueError 503
│
▼
Response
├── SessionMemory.add_interaction()
└── N exchanges reached → _summarize_and_store() → Pinecone
│
▼
Streamlit renders response
```

---

## ML Layer

```
Fitness Track
├── LinearRegression  — slope of weight_kg over sessions = kg/session progression
└── Z-score           — flags anomalous sleep/body weight (|Z| > 2)

Habits Track
├── K-Means (n=3)     — clusters habits by completion_rate + avg_score
│                       → high / medium / low consistency labels
└── Exponential decay — streak_score = Σ(completed * e^(-0.1 * days_ago_normalized))

Relationships Track
├── distilBERT        — sentiment trend on Mood field across session summaries
└── Cosine similarity — current message vs past issues → prevents coaching drift
```

---

## Memory System

```
Session Memory (ConversationSummaryBufferMemory)
├── Within-session context
├── Recent exchanges verbatim, older compressed
└── Injected into prompt via MessagesPlaceholder

Persistent Memory (Pinecone)
├── Cross-session recall
├── Auto-summarization every N exchanges (Fitness=5, Habits=3, Relationships=10)
├── Retrieval: top_k*2 → recency boost → threshold 0.4 → top_k
└── Recency boost: final_score = similarity + (session_no/max_session) * 0.1
```

---

## Evaluation

5 tests run against live Cloud Run backend (`python -m scripts.evaluate`):

| Test | What it validates | Result |
|---|---|---|
| test_health | Backend live and responding on Cloud Run | PASS ✅ |
| test_user_registration | User registration and track selection via API | PASS ✅ |
| test_chat | End-to-end coaching response — Pinecone + ML + Groq | PASS ✅ |
| test_data_logging | Fitness data logging to Google Cloud Storage | PASS ✅ |
| test_summarization | Auto-summarization triggers after n_exchanges | PASS ✅ |

**Score: 5/5**

---

## Live Demo

- **Frontend:** https://knowthyself-frontend-799604771720.us-central1.run.app
- **Backend:** https://knowthyself-backend-799604771720.us-central1.run.app/health

---

## How to Run

**1. Clone and install dependencies**
```bash
git clone https://github.com/solankinitish/know_thyself
cd know_thyself
pip install -r requirements.txt
```

**2. Set environment variables**
```bash
cp .env.example .env
# Add: PINECONE_API_KEY, GROQ_API_KEY, GCS_BUCKET
```

**3. Run locally**
```bash
# Terminal 1 — Backend
uvicorn app.api.server:app --reload

# Terminal 2 — Frontend
streamlit run streamlit_app.py
```

**4. Run with Docker**
```bash
docker-compose up --build
```

**5. Run tests**
```bash
python -m scripts.test_coaching_service
python -m scripts.test_ml
python -m scripts.test_memory
```

---

## Project Structure

```
knowthyself/
├── app/
│   ├── api/
│   │   └── server.py              — FastAPI app, all routes
│   ├── llm/
│   │   └── llm_client.py          — LangChain LLM wrapper (Groq + Ollama fallback)
│   ├── memory/
│   │   ├── session_memory.py      — ConversationSummaryBufferMemory per session
│   │   └── persistent_memory.py   — Pinecone long-term memory
│   ├── tracks/
│   │   ├── base_track.py          — Base class all tracks inherit from
│   │   ├── fitness_track.py       — Fitness prompt + ML logic
│   │   ├── habits_track.py        — Habits prompt + ML logic
│   │   └── relationships_track.py — Relationships prompt + ML logic
│   ├── ingestion/
│   │   └── csv_ingestor.py        — CSV upload and parsing
│   ├── ml/
│   │   ├── fitness_ml.py          — Linear regression, Z-score
│   │   ├── habits_ml.py           — K-Means, streak scoring
│   │   └── relationships_ml.py    — Sentiment analysis, cosine similarity
│   ├── prompts/
│   │   ├── prompt_builder.py      — Track-specific prompt construction
│   │   └── summary_prompts.py     — Track-specific summarization prompts
│   ├── services/
│   │   └── coaching_service.py    — Main orchestrator
│   └── utils/
│       ├── logger.py              — Logging
│       └── config.py              — Settings and environment variables
├── scripts/
│   ├── test_coaching_service.py
│   ├── test_ml.py
│   ├── test_memory.py
│   └── evaluate.py
├── streamlit_app.py               — Streamlit frontend
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

---

## Known Limitations

- **Heavy image (1.81GB)** — torch + distilBERT + SentenceTransformer; lighter sentiment library would reduce significantly
- **No authentication** — user_id is a plain string; JWT auth needed for production
- **ConversationSummaryBufferMemory deprecated** — LangChain migration to RunnableWithMessageHistory deferred
- **CSV persistence local vs cloud** — local Docker uses volume mount, cloud uses GCS; unification planned

---

## Summary

KnowThyself demonstrates a **production-style stateful AI coaching system** combining persistent cross-session memory, classical ML grounding, multi-track OOP design, cloud LLM integration, Docker containerization, and Google Cloud Run deployment — built and understood from first principles.
