# Project Structure

This document describes the organization of the Data Profiling Chatbot project.

## Directory Structure

```
Sql Chatbot/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration management
│   ├── database.py              # Database connection and query execution
│   ├── llm_client.py            # Ollama client for LLM interactions
│   ├── sql_validator.py         # SQL query validation and sanitization
│   ├── query_router.py          # Intelligent query routing (SQL vs General NLP)
│   ├── general_nlp.py           # General NLP handler for non-SQL queries
│   └── explainer.py             # Rule-based data quality explanations
│
├── scripts/                      # Utility and setup scripts
│   ├── init_sample_database.py  # Initialize SQLite sample database
│   ├── setup_sql_server.py      # Set up SQL Server tables and views
│   ├── test_sql_server_connection.py  # Test SQL Server connection
│   ├── example_queries.py       # Example usage script
│   ├── check_and_test.sh        # macOS/Linux test script
│   ├── check_and_test.bat       # Windows batch test script
│   └── check_and_test.ps1       # Windows PowerShell test script
│
├── docs/                         # Documentation
│   ├── SETUP_GUIDE.md           # Complete setup guide (Windows & macOS)
│   ├── WINDOWS_SETUP.md          # Windows-specific setup guide
│   ├── SQL_SERVER_SETUP.md      # SQL Server configuration guide
│   └── SETUP_CHECK.md           # Setup verification and troubleshooting
│
├── sql/                          # SQL scripts
│   └── setup_database.sql       # Database schema setup SQL
│
├── static/                       # Static web files
│   └── index.html               # Web UI for the chatbot
│
├── tests/                        # Test files (placeholder)
│   └── __init__.py
│
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── README.md                     # Main project documentation
└── PROJECT_STRUCTURE.md          # This file
```

## Key Files

### Application Code (`app/`)

- **`main.py`**: FastAPI application with all API endpoints
- **`config.py`**: Settings management using Pydantic
- **`database.py`**: Database connection handling (SQL Server and SQLite)
- **`llm_client.py`**: Integration with Ollama for LLM queries
- **`sql_validator.py`**: Security validation for SQL queries
- **`query_router.py`**: Routes queries between SQL and general NLP
- **`general_nlp.py`**: Handles conversational queries
- **`explainer.py`**: Generates rule-based explanations

### Scripts (`scripts/`)

- **`init_sample_database.py`**: Creates SQLite sample database for testing
- **`setup_sql_server.py`**: Sets up SQL Server schema (tables and views)
- **`test_sql_server_connection.py`**: Tests SQL Server connectivity
- **`example_queries.py`**: Demonstrates API usage
- **`check_and_test.*`**: Platform-specific test scripts

### Documentation (`docs/`)

All setup and configuration guides are organized in the `docs/` directory.

### Entry Point

- **`run.py`**: Main entry point to start the application
  ```bash
  python run.py
  # or
  python -m uvicorn app.main:app --reload
  ```

## Running the Application

### Option 1: Using run.py (Recommended)
```bash
python run.py
```

### Option 2: Using uvicorn directly
```bash
python -m uvicorn app.main:app --reload
```

### Option 3: Using Python module syntax
```bash
python -m app.main
```

## Import Structure

All application code uses absolute imports from the `app` package:

```python
from app.config import settings
from app.database import get_db
from app.llm_client import OllamaClient
```

Scripts in the `scripts/` directory add the project root to the path:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings
```

## Path Conventions

- **Database files**: Stored in project root (e.g., `profiling_sample.db`)
- **Static files**: Served from `static/` directory
- **Configuration**: Loaded from `.env` file in project root
- **Logs**: Can be configured to write to project root or dedicated logs directory

## Adding New Features

1. **New application modules**: Add to `app/` directory
2. **New scripts**: Add to `scripts/` directory
3. **New documentation**: Add to `docs/` directory
4. **New tests**: Add to `tests/` directory
5. **New SQL files**: Add to `sql/` directory

## Best Practices

1. **Imports**: Always use absolute imports from `app` package
2. **Paths**: Use `os.path.join()` and relative paths from project root
3. **Configuration**: Access settings via `app.config.settings`
4. **Logging**: Use the standard logging module with appropriate loggers
5. **Error Handling**: Provide clear, actionable error messages

