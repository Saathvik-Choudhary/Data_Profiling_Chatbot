"""SQL query validation for security and safety."""
import re
import logging
from typing import Optional, Tuple
from config import settings

logger = logging.getLogger(__name__)


class SQLValidator:
    """Validates SQL queries to ensure they are safe and read-only."""
    
    # Dangerous SQL keywords that should not appear in queries
    DANGEROUS_KEYWORDS = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
        'TRUNCATE', 'EXEC', 'EXECUTE', 'GRANT', 'REVOKE', 'MERGE'
    ]
    
    # Allowed SQL keywords
    ALLOWED_KEYWORDS = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY',
                        'HAVING', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',
                        'UNION', 'AS', 'AND', 'OR', 'NOT', 'IN', 'LIKE', 'BETWEEN',
                        'IS NULL', 'IS NOT NULL', 'COUNT', 'SUM', 'AVG', 'MAX', 'MIN',
                        'DISTINCT', 'TOP', 'LIMIT', 'OFFSET']
    
    def __init__(self):
        self.allowed_views = settings.allowed_views
    
    def validate(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a SQL query for safety.
        
        Args:
            query: SQL query string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not query or not query.strip():
            return False, "Query is empty"
        
        # Normalize query for validation
        query_upper = query.upper().strip()
        
        # Must start with SELECT
        if not query_upper.startswith('SELECT'):
            return False, "Only SELECT queries are allowed"
        
        # Check for dangerous keywords
        for keyword in self.DANGEROUS_KEYWORDS:
            # Use word boundaries to avoid false positives
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, query_upper):
                return False, f"Dangerous keyword '{keyword}' is not allowed"
        
        # Check that only allowed views are referenced
        view_pattern = r'\bFROM\s+(\w+)\b'
        matches = re.findall(view_pattern, query_upper)
        
        if matches:
            referenced_views = [match.upper() for match in matches]
            allowed_upper = [view.upper() for view in self.allowed_views]
            
            for view in referenced_views:
                if view not in allowed_upper:
                    return False, f"View '{view}' is not in the allowed list"
        
        # Check for semicolons (potential SQL injection risk)
        if ';' in query:
            # Allow semicolon only at the end
            if query.rstrip().rstrip(';') != query.rstrip():
                return False, "Semicolons are only allowed at the end of queries"
        
        logger.info("SQL query validation passed")
        return True, None
    
    def sanitize(self, query: str) -> str:
        """
        Sanitize a SQL query by removing trailing semicolons and extra whitespace.
        
        Args:
            query: SQL query string to sanitize
            
        Returns:
            Sanitized query string
        """
        # Remove trailing semicolons
        query = query.rstrip().rstrip(';')
        
        # Normalize whitespace
        query = ' '.join(query.split())
        
        return query

