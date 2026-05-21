# API Sentinel

API Sentinel is a lightweight API monitoring and alerting platform built with FastAPI.

## Current Stage

Stage 1: FastAPI project skeleton.

Implemented:

- Health check endpoint: GET /health
- Basic dependency file
- Environment variable example
- Git ignore rules

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- MySQL
- SQLAlchemy
- Alembic
- Redis
- JWT
- pytest
- Docker Compose

## Run Locally

Create and activate virtual environment, then install dependencies:

python -m pip install -r requirements.txt

Start the development server:

python -m uvicorn app.main:app --reload

Visit:

http://127.0.0.1:8000/health

Expected response:

{
  "status": "ok",
  "service": "api-sentinel",
  "version": "0.1.0"
}

## Roadmap

- Database configuration
- User authentication
- RBAC permission control
- Application management
- API event reporting
- Metrics statistics
- Alert rules
- Alert event lifecycle
- Operation logs
- Redis deduplication and rate limiting
- pytest tests
- Docker Compose deployment
