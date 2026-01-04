"""Query routing to determine if query needs SQL generation or general NLP."""
import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class QueryRouter:
    """Routes queries to appropriate handlers (SQL vs General NLP)."""
    
    # Keywords that suggest SQL/database queries
    SQL_KEYWORDS = [
        'table', 'column', 'row', 'null', 'data type', 'distinct',
        'profiling', 'statistics', 'quality', 'percentage', 'count',
        'show me', 'which', 'what are', 'find', 'list', 'get',
        'query', 'select', 'database', 'schema'
    ]
    
    # Keywords that suggest general conversation
    GENERAL_KEYWORDS = [
        'explain', 'how', 'why', 'what is', 'tell me about',
        'help', 'describe', 'compare', 'analyze', 'summarize',
        'difference', 'similar', 'example', 'definition'
    ]
    
    def route(self, question: str) -> Tuple[str, bool]:
        """
        Route a question to determine if it needs SQL generation.
        Defaults to general NLP for more natural conversations.
        
        Args:
            question: User's question
            
        Returns:
            Tuple of (query_type, needs_sql)
            query_type: 'sql', 'general', or 'mixed'
            needs_sql: True if SQL generation is needed
        """
        question_lower = question.lower().strip()
        
        # Check for specific data requests first (explicit SQL queries)
        is_data_request = any([
            'which columns' in question_lower and ('null' in question_lower or 'high' in question_lower or 'percentage' in question_lower),
            'which tables' in question_lower and ('most' in question_lower or 'largest' in question_lower or 'rows' in question_lower),
            'show me' in question_lower and ('table' in question_lower or 'column' in question_lower),
            'what are the' in question_lower and ('columns' in question_lower or 'tables' in question_lower or 'data types' in question_lower) and ('in' in question_lower or 'of' in question_lower),
            'list' in question_lower and ('columns' in question_lower or 'tables' in question_lower),
            'find' in question_lower and ('columns' in question_lower or 'tables' in question_lower),
        ])
        
        # Very explicit SQL patterns
        explicit_sql_patterns = [
            r'\b(show|list|find|get|query|select).*\b(table|column|row|data).*\b(null|percentage|count|distinct|type)',
            r'\bwhich\s+(columns?|tables?|rows?).*\b(have|with|contain|show)',
            r'\bwhat\s+(are|is)\s+the\s+(columns?|tables?|rows?|data\s+types?)\s+(in|of|with)',
        ]
        has_explicit_sql = any(re.search(pattern, question_lower) for pattern in explicit_sql_patterns)
        
        # General conversation indicators - these override SQL routing
        general_indicators = [
            question_lower.startswith(('what is', 'how does', 'why', 'explain', 'tell me about', 'can you help', 'help me understand')),
            question_lower.startswith(('i want to', 'i need to', 'i\'m looking to', 'i\'d like to')),
            len(question.split()) < 5 and '?' in question,  # Very short questions are usually conversational
            question_lower in ['hello', 'hi', 'hey', 'help', 'what can you do'],
        ]
        
        has_general = any(general_indicators)
        
        # Route to SQL only if it's clearly a data request and not a general question
        if (is_data_request or has_explicit_sql) and not has_general:
            return ('sql', True)
        else:
            # Default to general NLP for more natural conversations
            return ('general', False)


