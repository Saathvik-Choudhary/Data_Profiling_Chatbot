# Project Setup Guide - Windows & macOS

Complete setup instructions for the SQL Chatbot project on both Windows and macOS platforms.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Install Python](#step-1-install-python)
3. [Step 2: Install Ollama](#step-2-install-ollama)
4. [Step 3: Clone/Download Project](#step-3-clonedownload-project)
5. [Step 4: Set Up Virtual Environment](#step-4-set-up-virtual-environment)
6. [Step 5: Install Dependencies](#step-5-install-dependencies)
7. [Step 6: Configure Environment Variables](#step-6-configure-environment-variables)
8. [Step 7: Install ODBC Driver (SQL Server)](#step-7-install-odbc-driver-sql-server)
9. [Step 8: Test Database Connection](#step-8-test-database-connection)
10. [Step 9: Set Up Database Schema](#step-9-set-up-database-schema)
11. [Step 10: Run the Application](#step-10-run-the-application)
12. [Step 11: Verify Installation](#step-11-verify-installation)
13. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- **Internet connection** for downloading dependencies
- **Administrator/Admin access** (may be required for some installations)
- **SQL Server** (optional - only needed if connecting to SQL Server)
- **At least 8GB RAM** recommended for running Ollama models

---

## Step 1: Install Python

### Windows

1. **Download Python:**
   - Visit: https://www.python.org/downloads/
   - Download the latest Python 3.9+ (64-bit installer)
   - Choose "Windows installer (64-bit)"

2. **Install Python:**
   - Run the downloaded `.exe` file
   - **IMPORTANT:** Check "Add Python to PATH" checkbox
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation:**
   ```cmd
   python --version
   ```
   Should display: `Python 3.x.x`

4. **Verify pip:**
   ```cmd
   python -m pip --version
   ```

### macOS

1. **Check if Python is installed:**
   ```bash
   python3 --version
   ```

2. **If not installed, install via Homebrew:**
   ```bash
   brew install python3
   ```

3. **Or download from python.org:**
   - Visit: https://www.python.org/downloads/
   - Download macOS installer
   - Run the `.pkg` file and follow instructions

4. **Verify Installation:**
   ```bash
   python3 --version
   ```

5. **Verify pip:**
   ```bash
   python3 -m pip --version
   ```

---

## Step 2: Install Ollama

### Windows

1. **Download Ollama:**
   - Visit: https://ollama.com/download
   - Click "Download for Windows"
   - Download the `.exe` installer

2. **Install Ollama:**
   - Run the downloaded `.exe` file
   - Follow the installation wizard
   - Ollama will automatically start as a Windows service

3. **Verify Installation:**
   ```cmd
   ollama --version
   ```

4. **Pull Required Model:**
   ```cmd
   ollama pull llama3.1:8b
   ```
   This may take several minutes depending on your internet speed.

5. **Verify Model:**
   ```cmd
   ollama list
   ```
   Should show `llama3.1:8b` in the list

### macOS

1. **Install via Homebrew (Recommended):**
   ```bash
   brew install ollama
   ```

2. **Or download from website:**
   - Visit: https://ollama.com/download
   - Download macOS installer
   - Run the installer

3. **Start Ollama Service:**
   ```bash
   ollama serve
   ```
   Keep this terminal window open, or run in background:
   ```bash
   ollama serve &
   ```

4. **In a new terminal, pull the model:**
   ```bash
   ollama pull llama3.1:8b
   ```
   This may take several minutes depending on your internet speed.

5. **Verify Model:**
   ```bash
   ollama list
   ```
   Should show `llama3.1:8b` in the list

---

## Step 3: Clone/Download Project

### Windows

1. **Navigate to your desired location:**
   ```cmd
   cd C:\Users\YourUsername\Desktop
   ```

2. **If using Git:**
   ```cmd
   git clone <repository-url>
   cd "Sql Chatbot"
   ```

3. **Or extract from ZIP:**
   - Extract the project ZIP file
   - Navigate to the extracted folder:
   ```cmd
   cd "Sql Chatbot"
   ```

### macOS

1. **Navigate to your desired location:**
   ```bash
   cd ~/Desktop
   ```

2. **If using Git:**
   ```bash
   git clone <repository-url>
   cd "Sql Chatbot"
   ```

3. **Or extract from ZIP:**
   - Extract the project ZIP file
   - Navigate to the extracted folder:
   ```bash
   cd "Sql Chatbot"
   ```

---

## Step 4: Set Up Virtual Environment

### Windows

1. **Create virtual environment:**
   ```cmd
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```
   Your prompt should now show `(venv)` at the beginning.

3. **To deactivate later:**
   ```cmd
   deactivate
   ```

### macOS

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```
   Your prompt should now show `(venv)` at the beginning.

3. **To deactivate later:**
   ```bash
   deactivate
   ```

---

## Step 5: Install Dependencies

### Windows

```cmd
pip install -r requirements.txt
```

This will install:
- fastapi
- uvicorn
- pydantic
- pyodbc
- requests
- python-dotenv

### macOS

```bash
pip install -r requirements.txt
```

This will install:
- fastapi
- uvicorn
- pydantic
- pyodbc
- requests
- python-dotenv

**Note:** If you encounter issues with `pyodbc` on macOS, you may need to install unixODBC first:
```bash
brew install unixodbc
```

---

## Step 6: Configure Environment Variables

### Windows

1. **Create `.env` file:**
   ```cmd
   copy .env.example .env
   ```
   Or create manually if `.env.example` doesn't exist.

2. **Edit `.env` file** using Notepad or any text editor:
   ```cmd
   notepad .env
   ```

3. **Add your configuration:**
   ```env
   # SQL Server Configuration (if using SQL Server)
   DB_SERVER=localhost
   DB_DATABASE=your_database_name
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   DB_DRIVER=ODBC Driver 17 for SQL Server

   # SQLite Configuration (for local development)
   # DB_DATABASE=profiling_sample.db

   # Ollama Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.1:8b

   # Logging
   LOG_LEVEL=INFO
   ```

4. **Save and close the file.**

### macOS

1. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```
   Or create manually if `.env.example` doesn't exist.

2. **Edit `.env` file:**
   ```bash
   nano .env
   ```
   Or use any text editor of your choice.

3. **Add your configuration:**
   ```env
   # SQL Server Configuration (if using SQL Server)
   DB_SERVER=localhost
   DB_DATABASE=your_database_name
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   DB_DRIVER=ODBC Driver 17 for SQL Server

   # SQLite Configuration (for local development)
   # DB_DATABASE=profiling_sample.db

   # Ollama Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.1:8b

   # Logging
   LOG_LEVEL=INFO
   ```

4. **Save and close:**
   - In nano: Press `Ctrl+X`, then `Y`, then `Enter`

---

## Step 7: Install ODBC Driver (SQL Server)

**Note:** This step is only required if you're connecting to SQL Server. Skip if using SQLite.

### Windows

1. **Check if ODBC Driver is installed:**
   - Press `Win + R`, type `odbcad32.exe`, press Enter
   - Or search "ODBC Data Source Administrator (64-bit)" in Start Menu
   - Go to the "Drivers" tab
   - Look for "ODBC Driver 17 for SQL Server" or "ODBC Driver 18 for SQL Server"

2. **If not installed:**
   - Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   - Run the installer
   - Restart your computer if prompted

3. **Verify with Python:**
   ```cmd
   python -c "import pyodbc; print(pyodbc.drivers())"
   ```
   Should list SQL Server drivers.

### macOS

1. **Install via Homebrew (Recommended):**
   ```bash
   brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
   brew update
   brew install msodbcsql17
   ```

2. **Install unixODBC (if not already installed):**
   ```bash
   brew install unixodbc
   ```

3. **Verify installation:**
   ```bash
   odbcinst -q -d
   ```
   Should show "ODBC Driver 17 for SQL Server" or similar.

4. **Verify with Python:**
   ```bash
   python3 -c "import pyodbc; print(pyodbc.drivers())"
   ```
   Should list SQL Server drivers.

---

## Step 8: Test Database Connection

### Windows

**For SQL Server:**
```cmd
python test_sql_server_connection.py
```

**For SQLite (local development):**
1. First, create the sample database:
   ```cmd
   python init_sample_database.py
   ```
2. Then test:
   ```cmd
   python -c "from database import get_db; db = get_db(); print('Database connection successful!')"
   ```

### macOS

**For SQL Server:**
```bash
python3 test_sql_server_connection.py
```

**For SQLite (local development):**
1. First, create the sample database:
   ```bash
   python3 init_sample_database.py
   ```
2. Then test:
   ```bash
   python3 -c "from database import get_db; db = get_db(); print('Database connection successful!')"
   ```

**Expected Output:**
- ✅ Connection successful!
- SQL Server version information
- List of available views (if using SQL Server)

---

## Step 9: Set Up Database Schema

**Note:** This step is only required for SQL Server. SQLite setup is handled automatically.

### Windows

```cmd
python setup_sql_server.py
```

Follow the prompts:
- The script will test the connection first
- Type `y` when asked to create tables and views
- Wait for confirmation message

### macOS

```bash
python3 setup_sql_server.py
```

Follow the prompts:
- The script will test the connection first
- Type `y` when asked to create tables and views
- Wait for confirmation message

**This creates:**
- `profiling_tables` table
- `profiling_columns` table
- Three views: `profiling_column_stats`, `profiling_table_stats`, `profiling_data_quality`

---

## Step 10: Run the Application

### Windows

**Option 1: Using main.py**
```cmd
python main.py
```

**Option 2: Using uvicorn directly**
```cmd
python -m uvicorn main:app --reload
```

**Option 3: Run in background (PowerShell)**
```powershell
Start-Process python -ArgumentList "main.py"
```

### macOS

**Option 1: Using main.py**
```bash
python3 main.py
```

**Option 2: Using uvicorn directly**
```bash
python3 -m uvicorn main:app --reload
```

**Option 3: Run in background**
```bash
python3 main.py &
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Access the application:**
- API: http://localhost:8000
- Web UI: http://localhost:8000/ui
- API Docs: http://localhost:8000/docs

---

## Step 11: Verify Installation

### Windows

**1. Health Check (PowerShell):**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
```

**2. Health Check (Command Prompt with curl):**
```cmd
curl http://localhost:8000/health
```

**3. Test Chat Endpoint (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/chat" `
    -Method Post `
    -Headers @{"Content-Type"="application/json"} `
    -Body (@{"question"="Which columns have high null values?"} | ConvertTo-Json)
```

**4. Use Test Script:**
```cmd
check_and_test.bat
```
Or PowerShell:
```powershell
.\check_and_test.ps1
```

### macOS

**1. Health Check:**
```bash
curl http://localhost:8000/health
```

**2. Test Chat Endpoint:**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "Which columns have high null values?"}'
```

**3. Use Test Script:**
```bash
bash check_and_test.sh
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "ollama": "connected"
}
```

---

## Troubleshooting

### Common Issues

#### Python Not Found

**Windows:**
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Python39\python.exe`
- Restart Command Prompt after installation

**macOS:**
- Use `python3` instead of `python`
- Install via Homebrew: `brew install python3`

#### Ollama Connection Failed

**Windows:**
- Check if Ollama service is running: `ollama list`
- Restart Ollama service from Services (services.msc)
- Or restart the application

**macOS:**
- Make sure `ollama serve` is running
- Check if port 11434 is available: `lsof -i :11434`
- Restart Ollama: `pkill ollama && ollama serve`

#### ODBC Driver Not Found

**Windows:**
- Open "ODBC Data Source Administrator (64-bit)"
- Check Drivers tab for SQL Server drivers
- Download from Microsoft if missing
- Verify driver name matches exactly in `.env`

**macOS:**
- Install via Homebrew: `brew install msodbcsql17`
- Verify: `odbcinst -q -d`
- Check driver name in `.env` matches exactly

#### Port 8000 Already in Use

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**macOS:**
```bash
lsof -ti:8000 | xargs kill -9
```

Or change port in `main.py` or use:
```bash
python3 -m uvicorn main:app --port 8001
```

#### pyodbc Installation Fails

**Windows:**
- Ensure you're using 64-bit Python
- Install Visual C++ Build Tools
- Try: `pip install --upgrade pip` then `pip install pyodbc`

**macOS:**
- Install unixODBC first: `brew install unixodbc`
- Then: `pip install pyodbc`

#### Database Connection Errors

**Check:**
1. SQL Server is running (if using SQL Server)
2. Credentials in `.env` are correct
3. Firewall settings allow connection
4. Database name exists
5. User has proper permissions

**Test connection manually:**
- Windows: `python test_sql_server_connection.py`
- macOS: `python3 test_sql_server_connection.py`

#### Module Not Found Errors

**Solution:**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check you're in the project directory

#### Permission Denied Errors

**Windows:**
- Run Command Prompt as Administrator
- Check folder permissions

**macOS:**
- Use `sudo` if needed (not recommended)
- Check file/folder permissions: `chmod +x <file>`

---

## Quick Reference

### Windows Commands

| Task | Command |
|------|---------|
| Activate venv | `venv\Scripts\activate` |
| Run app | `python main.py` |
| Test connection | `python test_sql_server_connection.py` |
| Setup database | `python setup_sql_server.py` |
| Check health | `curl http://localhost:8000/health` |

### macOS Commands

| Task | Command |
|------|---------|
| Activate venv | `source venv/bin/activate` |
| Run app | `python3 main.py` |
| Test connection | `python3 test_sql_server_connection.py` |
| Setup database | `python3 setup_sql_server.py` |
| Check health | `curl http://localhost:8000/health` |

---

## Next Steps

After successful setup:

1. **Access Web UI:** http://localhost:8000/ui
2. **View API Docs:** http://localhost:8000/docs
3. **Try Example Queries:**
   - "Which columns have high null values?"
   - "Show me tables with the most rows"
   - "What is data profiling?"

## Additional Resources

- **General Documentation:** See `README.md`
- **SQL Server Setup:** See `SQL_SERVER_SETUP.md`
- **Windows-Specific:** See `WINDOWS_SETUP.md`
- **Troubleshooting:** See `SETUP_CHECK.md`

---

## Support

If you encounter issues not covered in this guide:

1. Check the troubleshooting section above
2. Review error messages carefully
3. Verify all prerequisites are installed
4. Check that services (Ollama, SQL Server) are running
5. Review log files for detailed error information

---

**Setup Complete!** 🎉

Your SQL Chatbot is now ready to use. Start the application and begin querying your data profiling statistics using natural language!

