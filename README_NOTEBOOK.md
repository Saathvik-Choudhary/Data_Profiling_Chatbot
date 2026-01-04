# SQL Chatbot - Jupyter Notebook Version

This branch contains a self-contained Jupyter notebook that runs the entire SQL Chatbot project.

## Quick Start

1. Open `SQL_Chatbot_Notebook.ipynb` in any Jupyter environment (JupyterLab, Google Colab, JupyterHub, etc.)
2. Run all cells in order
3. Start asking questions using the `ask_question()` function

## Features

- **Self-contained**: All code is included in the notebook
- **Online-ready**: Works in Google Colab, JupyterHub, and other online environments
- **Interactive**: Includes interactive chat interface with widgets
- **Complete functionality**: Natural language to SQL, data profiling, quality analysis

## Requirements

The notebook will automatically install required packages. You only need:
- Python 3.7+
- Jupyter environment
- Access to Ollama (or configure alternative LLM service)

## Usage

After running all setup cells, you can interact with the chatbot:

```python
# Simple usage
ask_question("Which columns have high null percentages?")

# Or use the interactive widget (if ipywidgets is available)
```

## Configuration

For online environments, you may need to:
1. Update `config.ollama_base_url` to point to a remote Ollama server
2. Or modify the `OllamaClient` class to use alternative LLM services (OpenAI, Anthropic, etc.)

## Notes

- The notebook uses SQLite for the database (no external database required)
- All sample data is generated automatically
- The notebook is completely self-contained and doesn't require any external files

