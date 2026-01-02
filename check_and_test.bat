@echo off
echo Checking model status and testing project...

REM Check if model is downloaded (requires ollama to be in PATH)
ollama list | findstr /C:"llama3.1" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ llama3.1:8b is available!
    echo.
    echo Running tests...
    
    REM Test SQL query
    echo 1. Testing SQL Query...
    curl -s -X POST "http://127.0.0.1:8000/chat" ^
         -H "Content-Type: application/json" ^
         -d "{\"question\": \"Which columns have high null values?\"}" | python -m json.tool | more
    
    echo.
    echo 2. Testing General NLP...
    curl -s -X POST "http://127.0.0.1:8000/chat" ^
         -H "Content-Type: application/json" ^
         -d "{\"question\": \"What is data profiling?\"}" | python -m json.tool | more
    
    echo.
    echo ✅ All tests complete!
) else (
    echo ⏳ Model still downloading...
    echo Run this script again when download completes:
    echo   check_and_test.bat
)

pause

