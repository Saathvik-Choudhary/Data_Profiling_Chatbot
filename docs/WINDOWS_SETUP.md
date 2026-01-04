# Windows Setup Guide

This guide provides Windows-specific instructions for setting up the SQL Chatbot project.

## Prerequisites

1. **Python 3.9+** - Download from [python.org](https://www.python.org/downloads/)
2. **Ollama** - Download from [ollama.com](https://ollama.com/download)
3. **SQL Server** (optional, for SQL Server connections)
4. **ODBC Driver** - Usually pre-installed with Windows

## Step 1: Install Python

1. Download Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```cmd
   python --version
   ```

## Step 2: Install Ollama

1. Download Ollama from https://ollama.com/download
2. Run the installer (`.exe` file)
3. Ollama will run as a Windows service automatically
4. Pull the required model:
   ```cmd
   ollama pull llama3.1:8b
   ```

## Step 3: Set Up Project

1. **Navigate to project directory:**
   ```cmd
   cd "Sql Chatbot"
   ```

2. **Create virtual environment:**
   ```cmd
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

## Step 4: Configure Database Connection

1. **Create `.env` file** (copy from `.env.example` if it exists):
   ```cmd
   copy .env.example .env
   ```

2. **Edit `.env` file** with your database credentials:
   ```env
   # SQL Server Configuration
   DB_SERVER=localhost
   DB_DATABASE=your_database_name
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   DB_DRIVER=ODBC Driver 17 for SQL Server

   # Ollama Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.1:8b

   # Logging
   LOG_LEVEL=INFO
   ```

## Step 5: Verify ODBC Driver (for SQL Server)

1. **Check if ODBC driver is installed:**
   - Open "ODBC Data Source Administrator (64-bit)" from Start Menu
   - Go to the "Drivers" tab
   - Look for "ODBC Driver 17 for SQL Server" or "ODBC Driver 18 for SQL Server"

2. **Or verify with Python:**
   ```cmd
   python -c "import pyodbc; print(pyodbc.drivers())"
   ```

3. **If not installed**, download from:
   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

## Step 6: Test SQL Server Connection

```cmd
python scripts/test_sql_server_connection.py
```

## Step 7: Set Up Database Schema (SQL Server)

```cmd
python scripts/setup_sql_server.py
```

## Step 8: Run the Application

**Option 1: Using run.py (Recommended)**
```cmd
python run.py
```

**Option 2: Using uvicorn directly**
```cmd
python -m uvicorn app.main:app --reload
```

The application will be available at: http://localhost:8000

## Testing the API

### Using PowerShell

**Health Check:**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
```

**Chat Endpoint:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/chat" `
    -Method Post `
    -Headers @{"Content-Type"="application/json"} `
    -Body (@{"question"="Which columns have high null values?"} | ConvertTo-Json)
```

### Using Command Prompt (with curl)

If you have curl installed (Windows 10+ includes it):

```cmd
curl http://localhost:8000/health
```

```cmd
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"question\": \"Which columns have high null values?\"}"
```

### Using Test Scripts

**Batch script:**
```cmd
scripts\check_and_test.bat
```

**PowerShell script:**
```powershell
.\scripts\check_and_test.ps1
```

## Common Windows-Specific Issues

### Issue: "python is not recognized"

**Solution:**
- Make sure Python is added to PATH
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Python39\python.exe`

### Issue: "ODBC Driver not found"

**Solution:**
1. Open "ODBC Data Source Administrator (64-bit)"
2. Check the Drivers tab
3. If missing, download from Microsoft's website
4. Verify driver name matches exactly in `.env` file

### Issue: "pyodbc installation fails"

**Solution:**
1. Make sure you're using 64-bit Python (check: `python -c "import platform; print(platform.architecture())"`)
2. Install Visual C++ Build Tools if needed
3. Try: `pip install --upgrade pip` then `pip install pyodbc`

### Issue: "Permission denied" errors

**Solution:**
- Run Command Prompt as Administrator
- Or adjust folder permissions

### Issue: "Port 8000 already in use"

**Solution:**
- Change port in `main.py` or use: `python -m uvicorn main:app --port 8001`
- Or stop the process using port 8000:
  ```cmd
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```

## Windows Firewall

If you can't access the API from other machines:

1. Open Windows Defender Firewall
2. Allow Python through firewall
3. Or add an inbound rule for port 8000

## Next Steps

1. Access the web UI: http://localhost:8000/ui
2. Test with questions like:
   - "Which columns have high null values?"
   - "Show me tables with the most rows"
   - "What is data profiling?"

## Additional Resources

- See `README.md` for general documentation
- See `SQL_SERVER_SETUP.md` for detailed SQL Server setup
- See `SETUP_CHECK.md` for troubleshooting

