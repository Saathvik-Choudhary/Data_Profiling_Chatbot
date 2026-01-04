"""Rule-based explanation system for data quality metrics."""
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class DataQualityExplainer:
    """Generates rule-based explanations for data profiling results."""
    
    # Thresholds for data quality assessment
    NULL_PERCENTAGE_HIGH = 50.0  # >50% nulls = high issue
    NULL_PERCENTAGE_MODERATE = 10.0  # 10-50% nulls = moderate issue
    DISTINCT_COUNT_LOW = 2  # <2 distinct values = low diversity
    
    def explain(self, results: List[Dict[str, Any]], question: str) -> str:
        """
        Generate rule-based explanation for query results.
        
        Args:
            results: Query results from database
            question: Original user question
            
        Returns:
            Explanation string
        """
        if not results:
            return "No data found matching your query."
        
        # Analyze results based on common profiling metrics
        explanations = []
        
        for row in results:
            row_explanation = self._explain_row(row)
            if row_explanation:
                explanations.append(row_explanation)
        
        if explanations:
            return " | ".join(explanations)
        
        # Default explanation
        return f"Found {len(results)} result(s). Data appears to be within normal parameters."
    
    def _explain_row(self, row: Dict[str, Any]) -> str:
        """Generate explanation for a single row of results."""
        explanations = []
        
        # Check null percentage
        null_pct = self._get_numeric_value(row, 'null_percentage')
        if null_pct is not None:
            if null_pct > self.NULL_PERCENTAGE_HIGH:
                explanations.append("High null percentage indicates data quality issue")
            elif null_pct > self.NULL_PERCENTAGE_MODERATE:
                explanations.append("Moderate null percentage requires data cleaning")
            elif null_pct > 0:
                explanations.append("Low null percentage - good data quality")
            else:
                explanations.append("No null values - excellent data quality")
        
        # Check distinct count
        distinct_count = self._get_numeric_value(row, 'distinct_count')
        if distinct_count is not None and distinct_count < self.DISTINCT_COUNT_LOW:
            explanations.append("Low distinct count suggests limited data diversity")
        
        # Check for table/column context
        table_name = row.get('table_name', '')
        column_name = row.get('column_name', '')
        
        if table_name and column_name:
            context = f"{table_name}.{column_name}"
        elif table_name:
            context = table_name
        elif column_name:
            context = column_name
        else:
            context = None
        
        if explanations and context:
            return f"{context}: {', '.join(explanations)}"
        elif explanations:
            return ', '.join(explanations)
        
        return None
    
    def _get_numeric_value(self, row: Dict[str, Any], key: str) -> Optional[float]:
        """Safely extract numeric value from row."""
        value = row.get(key)
        if value is None:
            return None
        
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

