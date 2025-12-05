# My-Work-Report-Fastapi

## Notebook

A FastAPI-based application for managing work reports and tasks with user authentication and role-based access control.

## 🚀 Features

- User authentication and authorization
- Task management (CRUD operations)
- User management (Admin only)
- RESTful API endpoints
- CORS enabled
- Database integration
- Logging
- Environment configuration

## 🛠️ Prerequisites

- Python 3.11+
- UV (Python package manager)
- SQLite (for development)

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/jeetendra29gupta/My-Work-Report-Fastapi.git
cd My-Work-Report-Fastapi
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On Unix or MacOS
```

### 3. Install dependencies

```bash
uv init
uv add fastapi uvicorn sqlmodel email-validator bcrypt pyjwt python-multipart markdown python-dotenv
uv add --group dev ruff pytest httpx
uv sync
```

### 4. Set up environment variables

Create a `.env` file in the root directory and add the following variables:

```env
# API metadata
TITLE="Work Report API"
DESCRIPTION="API for managing work reports, users, and tasks"
VERSION=1.0.0
SECRET_KEY=U30l0kte7vJhyus7YvKKJzG_v-TLf4W28NjQyiswJHQ

# FastAPI server
HOST=0.0.0.0
PORT=8181
RELOAD=true


# Logging
LOG_DIR=logs
LOG_FILE=work-report.log
MAX_BYTES=5242880
BACKUP_COUNT=5

# Database
DATABASE_DIR=database
DATABASE_NAME=work-report.db

# JWT
JWT_SECRET_KEY=e559643e21d0e97d16be90ea2e941d21a6a89d646fca2e6a6d48ba1ef12e41f8
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15000
REFRESH_TOKEN_EXPIRE_HOURS=24000

# Security
SALT_LENGTH=12
```

### 5. Run the application

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8181
```

The API will be available at `http://localhost:8181`

## 📚 API Documentation

Once the application is running, you can access the following documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗️ Project Structure

```
my-work-report-fastapi/
├── app/                    # Main application package
│   ├── main.py            # Application entry point
│   ├── models/            # Database models
│   ├── routes/            # API routes
│   ├── schemas/           # Pydantic models
│   └── utilities/         # Utility functions and configurations
├── tests/                 # Test files
├── .env                  # Environment variables
├── pyproject.toml        # Project dependencies
└── README.md             # This file
```

## 🧪 Development

Run linting and formatting:

```bash
uv run ruff check --fix .
uv run ruff format .
```

Run tests:

```bash
uv run pytest
```

## 📧 Contact

Jeetendra Gupta - [@jeetendra29gupta](https://github.com/jeetendra29gupta)

Project
Link: [https://github.com/jeetendra29gupta/My-Work-Report-Fastapi](https://github.com/jeetendra29gupta/My-Work-Report-Fastapi)