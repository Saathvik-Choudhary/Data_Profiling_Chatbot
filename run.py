#!/usr/bin/env python3
"""
Entry point for the Data Profiling Chatbot application.
Run this file to start the FastAPI server.
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

