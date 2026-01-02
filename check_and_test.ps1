# PowerShell script to check model status and test project
Write-Host "Checking model status and testing project..." -ForegroundColor Cyan

# Check if model is downloaded
$ollamaList = ollama list 2>&1
if ($ollamaList -match "llama3.1") {
    Write-Host "✅ llama3.1:8b is available!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Running tests..." -ForegroundColor Cyan
    
    # Test SQL query
    Write-Host "1. Testing SQL Query..." -ForegroundColor Yellow
    $response1 = Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" `
        -Method Post `
        -Headers @{"Content-Type"="application/json"} `
        -Body (@{"question"="Which columns have high null values?"} | ConvertTo-Json)
    $response1 | ConvertTo-Json -Depth 10 | Select-Object -First 20
    
    Write-Host ""
    Write-Host "2. Testing General NLP..." -ForegroundColor Yellow
    $response2 = Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" `
        -Method Post `
        -Headers @{"Content-Type"="application/json"} `
        -Body (@{"question"="What is data profiling?"} | ConvertTo-Json)
    $response2 | ConvertTo-Json -Depth 10 | Select-Object -First 15
    
    Write-Host ""
    Write-Host "✅ All tests complete!" -ForegroundColor Green
} else {
    Write-Host "⏳ Model still downloading..." -ForegroundColor Yellow
    Write-Host "Run this script again when download completes:" -ForegroundColor Yellow
    Write-Host "  .\check_and_test.ps1" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit"

