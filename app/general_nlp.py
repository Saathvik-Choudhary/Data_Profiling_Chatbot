"""General NLP capabilities for non-SQL queries."""
import requests
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class GeneralNLPHandler:
    """Handles general NLP queries that don't require SQL generation."""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
    
    def process_query(self, question: str, context: Optional[dict] = None) -> str:
        """
        Process a general NLP query.
        
        Args:
            question: User's question
            context: Optional context (e.g., previous conversation, data info)
            
        Returns:
            Natural language response
        """
        prompt = self._build_general_prompt(question, context)
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,  # Higher temperature for more natural, conversational responses
                        "top_p": 0.95,
                    }
                },
                timeout=120  # Increased timeout for larger model
            )
            response.raise_for_status()
            
            result = response.json()
            answer = result.get("response", "").strip()
            
            logger.info("Generated general NLP response")
            return answer
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again."
    
    def _build_general_prompt(self, question: str, context: Optional[dict] = None) -> str:
        """Build prompt for general NLP queries - more conversational and helpful."""
        base_prompt = f"""You are a friendly and knowledgeable data profiling assistant. You help users understand data quality, analytics, and answer questions in a natural, conversational way.

User question: {question}
"""
        
        if context:
            context_info = f"\nContext:\n"
            if context.get('available_tables'):
                context_info += f"Available tables: {', '.join(context['available_tables'])}\n"
            if context.get('database_info'):
                context_info += f"Database: {context['database_info']}\n"
            base_prompt += context_info
        
        base_prompt += """
Instructions:
- Be conversational, friendly, and helpful
- Answer naturally as if you're having a conversation
- If asked about data profiling concepts, explain them clearly with examples
- If the question is about specific data in the database, you can offer to help query it
- Feel free to ask clarifying questions if needed
- Keep responses concise but informative
- You can discuss data quality, analytics, best practices, and general data topics

Provide a natural, helpful response:"""
        
        return base_prompt

