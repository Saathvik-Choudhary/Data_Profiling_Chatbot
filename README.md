# Data Profiling Chatbot

A lightweight, local chatbot that allows users to interact with data profiling statistics using natural language. The system uses Meta's Llama 3.1 8B model running locally via Ollama, ensuring complete data privacy and offline operation. The chatbot supports both SQL query generation and general NLP conversations.

## Features

- **Natural Language to SQL**: Converts user questions into SQL queries
- **Read-Only Access**: Strict validation ensures only SELECT queries on predefined views
- **Rule-Based Explanations**: Deterministic data quality assessments
- **Fully Offline**: No cloud dependencies, all processing happens locally
- **Enterprise-Ready**: Suitable for restricted environments with security constraints

## Architecture

```
User Question → Query Router → [SQL Path: LLM (Llama 3.1) → SQL Query → Validator → Database → Results → Explainer → LLM Summary]
                              → [General NLP Path: LLM (Llama 3.1) → Direct Response]
```

## Prerequisites

1. **Python 3.9+**
2. **Ollama** installed and running with Llama 3.1 8B model
3. **SQL Server** (or SQLite for local development) with profiling database
4. **ODBC Driver** for SQL Server (required for SQL Server, optional for SQLite)
5. **pyodbc** Python package (installed via requirements.txt)

### Installing Ollama and Llama 3.1

**Windows:**
1. Download Ollama from: https://ollama.com/download
2. Install the downloaded `.exe` file
3. Start Ollama (it runs as a service automatically)
4. Pull the model:
   ```cmd
   ollama pull llama3.1:8b
   ```

**macOS:**
```bash
# Install Ollama
brew install ollama

# Start Ollama service
ollama serve

# Pull Llama 3.1 8B model (in another terminal)
ollama pull llama3.1:8b
```

**Linux:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull Llama 3.1 8B model (in another terminal)
ollama pull llama3.1:8b
```

## Installation

> **📘 For detailed step-by-step setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete guide for Windows and macOS

### Quick Start

1. Clone or navigate to the project directory:
```bash
cd "Sql Chatbot"
```

2. Create a virtual environment:

   **Windows:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   **Windows:**
   ```cmd
   copy .env.example .env
   REM Edit .env with your database credentials
   ```

   **macOS/Linux:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

## Configuration

Edit `.env` file with your settings:

```env
# Database Configuration
DB_SERVER=localhost
DB_DATABASE=profiling_db
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 17 for SQL Server

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Application Configuration
LOG_LEVEL=INFO
```

## Database Setup

### SQL Server Setup

1. **Install ODBC Driver for SQL Server** (if not already installed):
   - **Windows**: Usually pre-installed. Verify in "ODBC Data Source Administrator (64-bit)" → Drivers tab. If missing, download from [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - **macOS**: Download from [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) or use Homebrew: `brew install msodbcsql17`
   - **Linux**: Follow [Microsoft's installation guide](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-linux)

2. **Configure your `.env` file** with SQL Server credentials:
   ```env
   DB_SERVER=your_server_name_or_ip
   DB_DATABASE=your_database_name
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   DB_DRIVER=ODBC Driver 17 for SQL Server
   ```

3. **Test the connection**:
   
   **Windows:**
   ```cmd
   python test_sql_server_connection.py
   ```
   
   **macOS/Linux:**
   ```bash
   python3 test_sql_server_connection.py
   ```

4. **Set up database tables and views**:
   
   **Windows:**
   ```cmd
   python setup_sql_server.py
   ```
   
   **macOS/Linux:**
   ```bash
   python3 setup_sql_server.py
   ```
   This script will:
   - Create `profiling_tables` and `profiling_columns` tables
   - Create the required views: `profiling_column_stats`, `profiling_table_stats`, `profiling_data_quality`

5. **Populate the tables** with your profiling data. The views expect this structure:
   ```sql
   -- profiling_tables structure
   table_id (INT, PK)
   table_name (NVARCHAR)
   row_count (INT)
   column_count (INT)
   last_profiled_date (DATE)
   table_size_mb (DECIMAL)
   
   -- profiling_columns structure
   column_id (INT, PK)
   table_id (INT, FK)
   column_name (NVARCHAR)
   data_type (NVARCHAR)
   null_count (INT)
   distinct_count (INT)
   avg_length (DECIMAL)
   min_value (NVARCHAR)
   max_value (NVARCHAR)
   duplicate_count (INT)
   ```

### SQLite Setup (Local Development)

For local testing, you can use SQLite:

1. Set `DB_DATABASE=profiling_sample.db` in `.env`
2. Run:
   - **Windows**: `python init_sample_database.py`
   - **macOS/Linux**: `python3 init_sample_database.py`

The system automatically detects SQLite when the database name ends with `.db`.

## Running the Application

Start the FastAPI server:

**Windows:**
```cmd
python main.py
```

**macOS/Linux:**
```bash
python3 main.py
```

Or using uvicorn directly:

**Windows:**
```cmd
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**macOS/Linux:**
```bash
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Usage

### Health Check

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
```

**Windows (CMD) or macOS/Linux:**
```bash
curl http://localhost:8000/health
```

### Chat Endpoint

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/chat" `
    -Method Post `
    -Headers @{"Content-Type"="application/json"} `
    -Body (@{"question"="Which columns have high null values?"} | ConvertTo-Json)
```

**Windows (CMD) or macOS/Linux:**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "Which columns have high null values?"}'
```

Example response:

```json
{
  "answer": "The data shows that customer.email has a high null percentage of 65%, indicating a data quality issue that requires attention.",
  "sql_query": "SELECT table_name, column_name, null_percentage FROM profiling_column_stats WHERE null_percentage > 50 ORDER BY null_percentage DESC",
  "results_count": 3,
  "explanation": "customer.email: High null percentage indicates data quality issue"
}
```

## Security Features

- **Query Validation**: Only SELECT statements allowed
- **View Whitelist**: Only predefined views can be queried
- **No DML/DDL**: All write operations are blocked
- **Input Sanitization**: SQL injection prevention
- **Read-Only Access**: Database user should have read-only permissions

## Example Questions

- "Which columns have high null values?"
- "Show me tables with the most rows"
- "What are the data types in the customer table?"
- "Which columns have low distinct counts?"
- "Find columns with null percentage greater than 20%"

## Project Structure

```
Sql Chatbot/
├── main.py              # FastAPI application
├── config.py            # Configuration management
├── database.py          # Database connection and queries
├── llm_client.py        # Ollama client for Llama 3.1
├── query_router.py      # Intelligent query routing (SQL vs General NLP)
├── general_nlp.py        # General NLP handler for non-SQL queries
├── sql_validator.py     # SQL safety validation
├── explainer.py         # Rule-based explanations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── SETUP_GUIDE.md       # Complete setup guide (Windows & macOS)
├── SQL_SERVER_SETUP.md  # SQL Server specific setup
├── WINDOWS_SETUP.md     # Windows-specific guide
├── SETUP_CHECK.md       # Setup verification and troubleshooting
└── README.md           # This file
```

## Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete step-by-step setup for Windows and macOS
- **[SQL_SERVER_SETUP.md](SQL_SERVER_SETUP.md)** - Detailed SQL Server configuration
- **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** - Windows-specific setup guide
- **[SETUP_CHECK.md](SETUP_CHECK.md)** - Setup verification and troubleshooting

## Troubleshooting

### Ollama Connection Issues

- Ensure Ollama is running: `ollama serve`
- Check if model is available: `ollama list`
- Verify Ollama URL in `.env` matches your setup

### Database Connection Issues

- **Windows**: Verify ODBC driver in "ODBC Data Source Administrator (64-bit)" → Drivers tab, or check with Python: `python -c "import pyodbc; print(pyodbc.drivers())"`
- **macOS/Linux**: Verify ODBC driver: `odbcinst -q -d` (macOS/Linux) or check System Preferences (macOS)
- Test connection string manually
- Ensure database user has read permissions

### SQL Generation Issues

- Check that allowed views exist in database
- Verify view names in `config.py` match your schema
- Review logs for detailed error messages

## Development

The system follows a modular architecture for easy extension:

- **LLM Client**: Swap models by changing `ollama_model` in config
- **Explainer**: Add custom rules in `explainer.py`
- **Validator**: Extend validation rules in `sql_validator.py`
- **Database**: Support other databases by modifying `database.py`

## License

This project is designed for enterprise use with full local execution and data privacy.

