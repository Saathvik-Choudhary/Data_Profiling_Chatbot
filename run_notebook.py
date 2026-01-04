#!/usr/bin/env python3
"""Execute notebook cells programmatically."""
import json
import sys
import subprocess
import os

def execute_notebook(notebook_path):
    """Execute all code cells in the notebook."""
    print("="*60)
    print("Executing SQL Chatbot Notebook")
    print("="*60)
    
    # Read notebook
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    # Extract and execute code cells
    code_cells = [cell for cell in nb['cells'] if cell['cell_type'] == 'code']
    
    print(f"\nFound {len(code_cells)} code cells to execute\n")
    
    # Create execution context - use same dict for globals and locals to maintain state
    # Add display function for Jupyter compatibility
    def display(obj):
        """Simple display function for non-Jupyter environments."""
        if hasattr(obj, 'head'):
            print(obj.head(10).to_string())
        else:
            print(obj)
    
    exec_globals = {
        '__builtins__': __builtins__,
        '__name__': '__main__',
        '__doc__': None,
        'display': display,
    }
    
    for i, cell in enumerate(code_cells):
        source = ''.join(cell['source'])
        
        # Skip pip install commands (we'll handle dependencies separately)
        if '!pip' in source or 'pip install' in source:
            print(f"Cell {i+1}: Skipping pip install command")
            continue
        
        # Skip display/ipywidgets cells for now (they need Jupyter environment)
        if 'ipywidgets' in source and 'display' in source:
            print(f"Cell {i+1}: Skipping widget cell (requires Jupyter UI)")
            continue
        
        print(f"Cell {i+1}: Executing...")
        
        try:
            # Execute the cell - use same dict for both to maintain state
            exec(compile(source, f'<cell_{i}>', 'exec'), exec_globals, exec_globals)
            
            print(f"         ✅ Success")
            
        except Exception as e:
            error_msg = str(e)
            # Some errors are expected (like Ollama connection)
            if 'Ollama' in error_msg or 'Connection' in error_msg or 'Cannot connect' in error_msg:
                print(f"         ⚠️  Expected (Ollama not running): {error_msg[:60]}...")
            elif 'NameError' in error_msg and 'query_router' in error_msg:
                # This happens when example cells run before all components are initialized
                print(f"         ⚠️  Expected (example cell): Component not yet initialized")
            else:
                print(f"         ❌ Error: {error_msg}")
                # Print full traceback for unexpected errors
                import traceback
                traceback.print_exc()
    
    print("\n" + "="*60)
    print("Notebook execution complete!")
    print("="*60)
    
    # Test if key components are available
    print("\nVerifying key components:")
    if 'db' in exec_globals:
        print("  ✅ Database connection initialized")
    if 'llm_client' in exec_globals:
        print("  ✅ LLM client initialized")
    if 'chat' in exec_globals or 'ask_question' in exec_globals:
        print("  ✅ Chat functions available")
    
    # Try a simple test query if database is available
    if 'db' in exec_globals:
        try:
            print("\nTesting database query...")
            results = exec_globals['db'].execute_query("SELECT COUNT(*) as count FROM profiling_table_stats")
            if results:
                print(f"  ✅ Database query successful: {results[0]}")
        except Exception as e:
            print(f"  ⚠️  Database query test: {e}")

if __name__ == "__main__":
    notebook_path = "SQL_Chatbot_Notebook.ipynb"
    if not os.path.exists(notebook_path):
        print(f"Error: {notebook_path} not found")
        sys.exit(1)
    
    execute_notebook(notebook_path)

