"""Ollama client for interacting with Llama 3.1 model."""
import re
import requests
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
    
    def generate_sql(self, user_question: str) -> Optional[str]:
        """
        Generate SQL query from natural language question.
        
        Args:
            user_question: Natural language question about data profiling
            
        Returns:
            SQL query string or None if generation fails
        """
        prompt = self._build_sql_prompt(user_question)
        
        try:
            # First check if model is available
            models_response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if models_response.status_code == 200:
                models = models_response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                if self.model not in model_names:
                    logger.error(f"Model '{self.model}' not found. Available models: {model_names}")
                    logger.error(f"Please run: ollama pull {self.model}")
                    return None
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,  # Low temperature for deterministic SQL
                        "top_p": 0.9,
                    }
                },
                timeout=120  # Increased timeout for larger model
            )
            response.raise_for_status()
            
            result = response.json()
            sql_query = result.get("response", "").strip()
            
            # Extract SQL from markdown code blocks if present
            sql_query = self._extract_sql_from_response(sql_query)
            
            logger.info(f"Generated SQL query: {sql_query}")
            return sql_query
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Cannot connect to Ollama at {self.base_url}. Is Ollama running?")
            logger.error(f"Start Ollama with: ollama serve")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {e}")
            # Check if it's a model not found error
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if "model" in str(error_data).lower() and "not found" in str(error_data).lower():
                        logger.error(f"Model '{self.model}' not found. Run: ollama pull {self.model}")
                except:
                    pass
            return None
    
    def summarize_results(self, question: str, results: list, explanation: str) -> str:
        """
        Generate a natural language summary of query results.
        
        Args:
            question: Original user question
            results: Query results
            explanation: Rule-based explanation
            
        Returns:
            Natural language summary
        """
        prompt = self._build_summary_prompt(question, results, explanation)
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                    }
                },
                timeout=90  # Increased timeout for larger model
            )
            response.raise_for_status()
            
            result = response.json()
            summary = result.get("response", "").strip()
            
            logger.info("Generated summary from LLM")
            return summary
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error during summarization: {e}")
            # Fallback to rule-based explanation
            return explanation
    
    def _build_sql_prompt(self, question: str) -> str:
        """Build prompt for SQL generation."""
        allowed_views = ", ".join(settings.allowed_views)
        
        return f"""You are a SQL query generator for data profiling statistics.

Available views:
- {allowed_views}

These views contain data profiling information with columns like:
- table_name
- column_name
- null_percentage
- distinct_count
- data_type
- row_count

Generate a SQL SELECT query to answer this question: {question}

Rules:
1. Only use SELECT statements
2. Only query from the allowed views listed above
3. Return only the SQL query, no explanations
4. Use SQLite syntax (LIMIT instead of TOP, no semicolons needed)

SQL Query:"""
    
    def _build_summary_prompt(self, question: str, results: list, explanation: str) -> str:
        """Build prompt for result summarization."""
        results_str = str(results[:10])  # Limit to first 10 rows for context
        
        return f"""User asked: {question}

Query returned {len(results)} results.

Data quality assessment: {explanation}

Provide a concise, natural language answer (2-3 sentences) explaining what the data shows:"""
    
    def _extract_sql_from_response(self, response: str) -> str:
        """Extract SQL query from LLM response (handles markdown code blocks)."""
        # Check for SQL code blocks
        sql_pattern = r'```(?:sql)?\s*(.*?)```'
        match = re.search(sql_pattern, response, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        # Check for SELECT statement
        if 'SELECT' in response.upper():
            # Extract from first SELECT to end or semicolon
            start = response.upper().find('SELECT')
            sql = response[start:]
            # Remove trailing markdown or explanations
            lines = sql.split('\n')
            sql_lines = []
            for line in lines:
                if line.strip() and not line.strip().startswith('```'):
                    sql_lines.append(line)
                if line.strip().endswith(';'):
                    break
            return ' '.join(sql_lines).rstrip(';').strip()
        
        return response.strip()

