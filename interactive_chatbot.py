#!/usr/bin/env python3
"""
Interactive chatbot - Run this to interact with the SQL Chatbot.
This script loads all the components from the notebook and provides an interactive chat interface.
"""
import json
import os
import sqlite3
import logging
import re
import requests
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    db_path = "profiling_sample.db"
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    allowed_views = [
        "profiling_column_stats",
        "profiling_table_stats",
        "profiling_data_quality"
    ]

config = Config()

# Import all components from notebook
print("="*60)
print("Initializing SQL Chatbot...")
print("="*60)

# Load notebook and extract code
with open('SQL_Chatbot_Notebook.ipynb', 'r') as f:
    nb = json.load(f)

# Execute all setup cells
exec_globals = {
    '__builtins__': __builtins__,
    '__name__': '__main__',
    '__doc__': None,
    'display': print,  # Simple display function
}

code_cells = [cell for cell in nb['cells'] if cell['cell_type'] == 'code']

for i, cell in enumerate(code_cells):
    source = ''.join(cell['source'])
    
    # Skip pip install and widget cells
    if '!pip' in source or 'pip install' in source or ('ipywidgets' in source and 'display' in source):
        continue
    
    try:
        exec(compile(source, f'<cell_{i}>', 'exec'), exec_globals, exec_globals)
    except Exception as e:
        if 'Ollama' not in str(e) and 'Connection' not in str(e) and 'display' not in str(e):
            logger.warning(f"Cell {i+1} warning: {e}")

# Get chat function
chat = exec_globals.get('chat')
ask_question = exec_globals.get('ask_question')

if not chat and not ask_question:
    print("Error: Could not load chat functions from notebook")
    exit(1)

print("\n✅ Chatbot initialized and ready!")
print("="*60)
print("\nYou can now ask questions about your data profiling statistics.")
print("Examples:")
print("  - 'Which columns have high null percentages?'")
print("  - 'Show me the tables with the most rows'")
print("  - 'What are the data types in the customers table?'")
print("  - 'Explain data profiling'")
print("\nType 'quit' or 'exit' to stop.\n")

# Interactive loop
while True:
    try:
        question = input("\n💬 Your question: ").strip()
        
        if not question:
            continue
            
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        # Use ask_question if available, otherwise use chat
        if ask_question:
            ask_question(question)
        else:
            response = chat(question)
            print(f"\n📊 Answer: {response.get('answer', 'No answer generated')}")
            if response.get('sql_query'):
                print(f"\n🔍 SQL Query: {response['sql_query']}")
            if response.get('results_count', 0) > 0:
                print(f"\n📈 Results: {response['results_count']} row(s) found")
                if 'results' in response and response['results']:
                    import pandas as pd
                    df = pd.DataFrame(response['results'])
                    print("\nFirst few results:")
                    print(df.head(10).to_string())
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Error in chat loop: {e}", exc_info=True)

