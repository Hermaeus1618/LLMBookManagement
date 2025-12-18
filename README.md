# Intelligent Book Management System

This project is an intelligent book management system built with **FastAPI**, **PostgreSQL**, and a locally running **Ollama AI model**. It supports CRUD operations on books, user reviews, AI-generated summaries, recommendations, and JWT-based authentication.

---

## Features

- User registration & login (JWT-based)
- CRUD for books
- Add & retrieve book reviews
- Generate AI-powered book & review summaries
- Book recommendations
- Async operations with SQLAlchemy & asyncpg
- Modular, testable, and cloud-ready
- Dockerized for easy deployment

---

## Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Pydantic
- Uvicorn
- Docker & Docker Compose
- Ollama API for AI summaries

---

## Installation

### 1. Clone repository
```bash
git clone <repo-url>
cd <repo>
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Running Locally
- Start PostgreSQL (update app/core/config.py if needed)
- Initialize DB:
```bash
python -m app.db.session
```

- Run FastAPI app:
```bash
uvicorn app.main:app --reload
```

### Testing

#### Run unit tests:
```bash
pytest -v
```
Tests cover authentication, books, and reviews, Fully async-safe.
