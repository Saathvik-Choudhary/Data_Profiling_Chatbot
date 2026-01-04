# SQL Server Setup Guide

This guide will help you configure the chatbot to connect to SQL Server Management Studio (SSMS).

## Step 1: Install ODBC Driver

### macOS
1. Download the Microsoft ODBC Driver from:
   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
2. Install the driver package
3. Verify installation:
   ```bash
   odbcinst -q -d
   ```
   You should see "ODBC Driver 17 for SQL Server" or similar

### Windows
1. **ODBC drivers are usually pre-installed** with Windows
2. **Verify installation**:
   - Open "ODBC Data Source Administrator" (64-bit) from Start Menu
   - Go to the "Drivers" tab
   - Look for "ODBC Driver 17 for SQL Server" or "ODBC Driver 18 for SQL Server"
3. **If not installed**, download from:
   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
4. **Verify with Python**:
   ```python
   import pyodbc
   print(pyodbc.drivers())
   ```
   You should see SQL Server drivers listed

## Step 2: Configure .env File

Create or update your `.env` file with SQL Server credentials:

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
- The driver name must match exactly what's installed on your system

## Step 3: Test Connection

Run the test script to verify your connection:

**Windows:**
```cmd
python scripts/test_sql_server_connection.py
```

**macOS/Linux:**
```bash
python3 scripts/test_sql_server_connection.py
```

This will:
- Test the connection to SQL Server
- Check if required views exist
- Display SQL Server version information

## Step 4: Set Up Database Schema

Run the setup script to create tables and views:

**Windows:**
```cmd
python scripts/setup_sql_server.py
```

**macOS/Linux:**
```bash
python3 scripts/setup_sql_server.py
```

This script will:
1. Test the connection
2. Create `profiling_tables` table
3. Create `profiling_columns` table
4. Create three views:
   - `profiling_column_stats`
   - `profiling_table_stats`
   - `profiling_data_quality`

## Step 5: Populate Data

After creating the schema, populate the tables with your profiling data:

```sql
-- Example: Insert table information
INSERT INTO profiling_tables (table_name, row_count, column_count, last_profiled_date, table_size_mb)
VALUES ('customers', 15000, 12, '2024-01-15', 12.5);

-- Example: Insert column information
INSERT INTO profiling_columns (table_id, column_name, data_type, null_count, distinct_count, avg_length, min_value, max_value, duplicate_count)
VALUES (1, 'customer_id', 'INT', 0, 15000, NULL, '1', '15000', 0);
```

## Step 6: Verify Setup

1. Check that views are accessible:
   ```sql
   SELECT TOP 10 * FROM profiling_column_stats;
   SELECT TOP 10 * FROM profiling_table_stats;
   SELECT TOP 10 * FROM profiling_data_quality;
   ```

2. Test the chatbot connection:
   
   **Windows:**
   ```cmd
   python run.py
   ```
   Or:
   ```cmd
   python -m uvicorn app.main:app --reload
   ```
   
   **macOS/Linux:**
   ```bash
   python3 run.py
   ```
   Or:
   ```bash
   python3 -m uvicorn app.main:app --reload
   ```

3. Check health endpoint:
   
   **Windows (PowerShell):**
   ```powershell
   Invoke-WebRequest -Uri http://localhost:8000/health
   ```
   
   **Windows (CMD) or macOS/Linux:**
   ```bash
   curl http://localhost:8000/health
   ```

## Troubleshooting

### Connection Issues

**Error: "pyodbc is not available"**
- Install pyodbc: `pip install pyodbc`
- **Windows**: ODBC drivers are usually pre-installed. If not, download from Microsoft.
- **macOS**: Install unixODBC: `brew install unixodbc`
- **Linux**: Install unixODBC and Microsoft ODBC Driver

**Error: "Driver not found"**
- **Windows**: Check ODBC Data Source Administrator (64-bit) in Start Menu → Drivers tab
- **macOS/Linux**: List available drivers: `odbcinst -q -d`
- **Python**: Check with `python -c "import pyodbc; print(pyodbc.drivers())"`
- Update `DB_DRIVER` in `.env` to match an installed driver exactly
- Common driver names:
  - `ODBC Driver 17 for SQL Server`
  - `ODBC Driver 18 for SQL Server`
  - `SQL Server` (older versions)

**Error: "Login failed"**
- Verify username and password
- Check SQL Server authentication mode (SQL Server Authentication vs Windows Authentication)
- Ensure the user has access to the database

**Error: "Cannot open database"**
- Verify database name is correct
- Ensure the user has permissions to access the database
- Check if database exists: `SELECT name FROM sys.databases;`

### View Issues

**Error: "Invalid object name"**
- Run `setup_sql_server.py` to create views
- Verify views exist: `SELECT * FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_NAME LIKE 'profiling%'`

## Security Best Practices

1. **Use Read-Only Database User**:
   ```sql
   CREATE USER chatbot_user WITH PASSWORD 'secure_password';
   GRANT SELECT ON profiling_column_stats TO chatbot_user;
   GRANT SELECT ON profiling_table_stats TO chatbot_user;
   GRANT SELECT ON profiling_data_quality TO chatbot_user;
   ```

2. **Use Encrypted Connections**:
   - For Azure SQL, encryption is enabled by default
   - For on-premises, consider enabling SSL/TLS

3. **Store Credentials Securely**:
   - Never commit `.env` file to version control
   - Use environment variables in production
   - Consider using Azure Key Vault or similar for production

## Next Steps

Once your SQL Server connection is working:
1. Start the chatbot:
   - **Windows**: `python run.py`
   - **macOS/Linux**: `python3 run.py`
   Or using uvicorn:
   - **Windows**: `python -m uvicorn app.main:app --reload`
   - **macOS/Linux**: `python3 -m uvicorn app.main:app --reload`
2. Access the web UI: http://localhost:8000/ui
3. Test with questions like:
   - "Which columns have high null values?"
   - "Show me tables with the most rows"
