"""FastAPI application for data profiling chatbot."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
from typing import Optional
import os

from llm_client import OllamaClient
from sql_validator import SQLValidator
from database import get_db
from explainer import DataQualityExplainer
from query_router import QueryRouter
from general_nlp import GeneralNLPHandler
from config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize components
app = FastAPI(
    title="Data Profiling Chatbot",
    description="Local chatbot for querying data profiling statistics using natural language",
    version="1.0.0"
)

# CORS middleware (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_client = OllamaClient()
sql_validator = SQLValidator()
explainer = DataQualityExplainer()
query_router = QueryRouter()
general_nlp = GeneralNLPHandler()

# Serve static files (web UI)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/ui")
async def serve_ui():
    """Serve the web UI."""
    ui_path = os.path.join(static_dir, "index.html")
    if os.path.exists(ui_path):
        return FileResponse(ui_path)
    raise HTTPException(status_code=404, detail="UI not found")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str
    sql_query: Optional[str] = None
    results_count: int = 0
    explanation: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Data Profiling Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db = get_db()
        with db.get_connection():
            db_status = "connected"
    except ImportError as e:
        db_status = f"not_configured: {str(e)}"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        db_status = f"error: {str(e)}"
    
    # Test Ollama connection
    try:
        import requests
        response = requests.get(f"{settings.ollama_base_url}/api/tags", timeout=5)
        ollama_status = "connected" if response.status_code == 200 else "error"
    except Exception as e:
        logger.error(f"Ollama health check failed: {e}")
        ollama_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "connected" and ollama_status == "connected" else "degraded",
        "database": db_status,
        "ollama": ollama_status
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that handles both SQL queries and general NLP questions.
    
    Flow:
    1. Route query (SQL vs General NLP)
    2. If SQL: Generate → Validate → Execute → Summarize
    3. If General: Process with general NLP handler
    """
    question = request.question.strip()
    
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    logger.info(f"Received question: {question}")
    
    # Route the query
    query_type, needs_sql = query_router.route(question)
    logger.info(f"Query routed as: {query_type} (needs_sql: {needs_sql})")
    
    try:
        if needs_sql:
            # SQL Query Path
            return await _handle_sql_query(question)
        else:
            # General NLP Path
            return await _handle_general_query(question)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


async def _handle_sql_query(question: str) -> ChatResponse:
    """Handle SQL query generation and execution."""
    # Step 1: Generate SQL from natural language
    sql_query = llm_client.generate_sql(question)
    
    if not sql_query:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate SQL query. Please check Ollama connection."
        )
    
    # Step 2: Validate SQL query
    is_valid, error_message = sql_validator.validate(sql_query)
    
    if not is_valid:
        logger.warning(f"SQL validation failed: {error_message}")
        raise HTTPException(
            status_code=400,
            detail=f"Generated SQL query is not safe: {error_message}"
        )
    
    # Sanitize query
    sql_query = sql_validator.sanitize(sql_query)
    
    # Step 3: Execute query
    try:
        db = get_db()
        results = db.execute_query(sql_query)
    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database not configured: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )
    
    # Step 4: Generate rule-based explanation
    explanation = explainer.explain(results, question)
    
    # Step 5: Generate natural language summary
    answer = llm_client.summarize_results(question, results, explanation)
    
    # Fallback to explanation if LLM summarization fails
    if not answer or len(answer.strip()) < 10:
        answer = explanation
    
    logger.info(f"Successfully processed SQL question. Returned {len(results)} results")
    
    return ChatResponse(
        answer=answer,
        sql_query=sql_query,
        results_count=len(results),
        explanation=explanation
    )


async def _handle_general_query(question: str) -> ChatResponse:
    """Handle general NLP queries with conversational responses."""
    # Get context about available data (optional, non-blocking)
    context = {}
    try:
        db = get_db()
        tables_result = db.execute_query(
            "SELECT DISTINCT table_name FROM profiling_table_stats LIMIT 10"
        )
        context['available_tables'] = [row['table_name'] for row in tables_result]
        context['database_info'] = "Sample profiling database with data quality metrics"
    except:
        pass  # Continue without context if database unavailable
    
    # Process with general NLP - more conversational
    answer = general_nlp.process_query(question, context)
    
    logger.info("Successfully processed general NLP question")
    
    return ChatResponse(
        answer=answer,
        sql_query=None,
        results_count=0,
        explanation=None
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

