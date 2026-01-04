#!/bin/bash
# Navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "Checking model status and testing project..."

# Check if model is downloaded
if ollama list | grep -q llama3.1; then
    echo "✅ llama3.1:8b is available!"
    echo ""
    echo "Running tests..."
    
    # Test SQL query
    echo "1. Testing SQL Query..."
    curl -s -X POST "http://127.0.0.1:8000/chat" \
         -H "Content-Type: application/json" \
         -d '{"question": "Which columns have high null values?"}' | python3 -m json.tool | head -20
    
    echo ""
    echo "2. Testing General NLP..."
    curl -s -X POST "http://127.0.0.1:8000/chat" \
         -H "Content-Type: application/json" \
         -d '{"question": "What is data profiling?"}' | python3 -m json.tool | head -15
    
    echo ""
    echo "✅ All tests complete!"
else
    echo "⏳ Model still downloading..."
    echo "Run this script again when download completes:"
    echo "  bash scripts/check_and_test.sh"
fi
