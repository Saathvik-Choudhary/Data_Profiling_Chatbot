"""Example script to test the chatbot with sample queries."""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def test_chat(question: str) -> Dict[str, Any]:
    """
    Test the chat endpoint with a question.
    
    Args:
        question: Natural language question
        
    Returns:
        Response dictionary
    """
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"question": question},
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()


def print_response(response: Dict[str, Any], question: str):
    """Pretty print the chatbot response."""
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")
    print(f"\nAnswer:\n{response['answer']}")
    print(f"\nSQL Query:\n{response['sql_query']}")
    print(f"\nResults Count: {response['results_count']}")
    if response.get('explanation'):
        print(f"\nExplanation: {response['explanation']}")
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    # Example questions to test
    example_questions = [
        "Which columns have high null values?",
        "Show me tables with the most rows",
        "What are the data types in the customer table?",
        "Which columns have null percentage greater than 20%?",
        "Find columns with low distinct counts"
    ]
    
    print("Testing Data Profiling Chatbot")
    print("=" * 60)
    
    # Test health endpoint first
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Health Check: {health.json()}")
        print()
    except Exception as e:
        print(f"Warning: Could not connect to API: {e}")
        print("Make sure the server is running: python -m app.main")
        exit(1)
    
    # Test each example question
    for question in example_questions:
        try:
            response = test_chat(question)
            print_response(response, question)
        except Exception as e:
            print(f"Error processing question '{question}': {e}")
            print()


