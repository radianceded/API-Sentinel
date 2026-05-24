# API Sentinel

API Sentinel is an API monitoring and alerting backend system built with FastAPI.

Current features:

- FastAPI backend architecture
- Dockerized MySQL database
- SQLAlchemy ORM integration
- Alembic database migrations
- User model and database schema management

Tech stack:

- FastAPI
- SQLAlchemy 2.x
- Alembic
- MySQL 8
- Docker

## Local Development

### 1. Create virtual environment

```bash
python -m venv .venv
```

### 2. Activate virtual environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` file:

```env
DATABASE_URL=mysql+pymysql://root:api_sentinel_root@127.0.0.1:3307/api_sentinel
```

### 5. Start MySQL with Docker

```bash
docker run --name api-sentinel-mysql ^
-e MYSQL_ROOT_PASSWORD=api_sentinel_root ^
-e MYSQL_DATABASE=api_sentinel ^
-p 3307:3306 ^
-v api-sentinel-mysql-data:/var/lib/mysql ^
-d mysql:8.0
```

### 6. Run database migrations

```bash
python -m alembic upgrade head
```

### 7. Start FastAPI server

```bash
uvicorn app.main:app --reload
```

## Project Structure

```text
app/
├─ core/          # configuration
├─ db/            # database session and base
├─ models/        # ORM models
├─ main.py

alembic/          # database migrations
```


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
