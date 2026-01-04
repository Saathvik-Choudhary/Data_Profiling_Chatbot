# SQL Server Setup Status Check

## Current Status

✅ **pyodbc installed**: Version 5.3.0  
❌ **ODBC Driver**: Not installed  
❌ **.env file**: Not found (using defaults)

## Required Steps to Connect to SQL Server/SSMS

### Step 1: Install Microsoft ODBC Driver for SQL Server

**Windows:**
1. ODBC drivers are usually **pre-installed** with Windows
2. **Verify installation**:
   - Open "ODBC Data Source Administrator (64-bit)" from Start Menu
   - Go to the "Drivers" tab
   - Look for "ODBC Driver 17 for SQL Server" or "ODBC Driver 18 for SQL Server"
3. **If not installed**, download from:
   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
4. **Verify with Python**:
   ```cmd
   python -c "import pyodbc; print(pyodbc.drivers())"
   ```

**macOS:**
**Option A: Using Homebrew (Recommended)**
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql17
# For Apple Silicon (M1/M2), also install:
brew install mssql-tools
```

**Option B: Manual Download**
1. Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
2. Install the `.pkg` file
3. Verify installation:
   ```bash
   odbcinst -q -d
   ```
   You should see "ODBC Driver 17 for SQL Server" or "ODBC Driver 18 for SQL Server"

### Step 2: Install unixODBC (macOS/Linux only)

**macOS:**
```bash
brew install unixodbc
```

**Linux:**
Follow Microsoft's installation guide for your distribution.

### Step 3: Create .env File

Create a `.env` file in the project root with your SQL Server credentials:

```env
# SQL Server Configuration
DB_SERVER=localhost                    # or your SQL Server instance name/IP
DB_DATABASE=your_database_name        # Your database name
DB_USERNAME=your_username             # SQL Server username
DB_PASSWORD=your_password             # SQL Server password
DB_DRIVER=ODBC Driver 17 for SQL Server

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Logging
LOG_LEVEL=INFO
```

**Important Notes:**
- For local SQL Server: `DB_SERVER=localhost` or `DB_SERVER=localhost\SQLEXPRESS`
- For remote SQL Server: `DB_SERVER=server_name_or_ip`
- For Azure SQL: `DB_SERVER=your_server.database.windows.net`
- The driver name must match exactly what's installed:
  - **Windows**: Check in ODBC Data Source Administrator or use: `python -c "import pyodbc; print(pyodbc.drivers())"`
  - **macOS/Linux**: `odbcinst -q -d`

### Step 4: Verify Installation

After installing the ODBC driver, verify it's available:

**Windows:**
```cmd
python -c "import pyodbc; drivers = [x for x in pyodbc.drivers()]; print('Available drivers:'); [print(f'  - {d}') for d in drivers]"
```

**macOS/Linux:**
```bash
python3 -c "import pyodbc; drivers = [x for x in pyodbc.drivers()]; print('Available drivers:'); [print(f'  - {d}') for d in drivers]"
```

You should see at least one SQL Server driver listed.

### Step 5: Test Connection

**Windows:**
```cmd
python scripts/test_sql_server_connection.py
```

**macOS/Linux:**
```bash
python3 scripts/test_sql_server_connection.py
```

### Step 6: Set Up Database Schema

**Windows:**
```cmd
python scripts/setup_sql_server.py
```

**macOS/Linux:**
```bash
python3 scripts/setup_sql_server.py
```

## Database Type Detection

The system automatically detects which database to use:
- **SQLite**: If `DB_DATABASE` ends with `.db` (e.g., `profiling_sample.db`)
- **SQL Server**: If `DB_DATABASE` does NOT end with `.db` (e.g., `profiling_sample`)

## Troubleshooting

### "No drivers found"
- Install Microsoft ODBC Driver (see Step 1)
- **Windows**: Verify in ODBC Data Source Administrator or use: `python -c "import pyodbc; print(pyodbc.drivers())"`
- **macOS/Linux**: Verify with: `odbcinst -q -d`

### "pyodbc is not available"
- Already installed ✅
- If issues persist, reinstall: `pip install --upgrade pyodbc`

### Connection Errors
- Verify SQL Server is running
- Check firewall settings
- Verify credentials in `.env` file
- Test connection string manually

## Current Configuration

- **DB_SERVER**: localhost
- **DB_DATABASE**: profiling_sample (will use SQL Server mode)
- **DB_USERNAME**: test_user
- **DB_DRIVER**: ODBC Driver 17 for SQL Server

**Note**: Since `profiling_sample` doesn't end with `.db`, the system will attempt to use SQL Server. Make sure you have:
1. ODBC driver installed
2. Valid `.env` file with correct credentials
3. SQL Server running and accessible

