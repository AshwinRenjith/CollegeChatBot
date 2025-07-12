from src.query_processor import QueryProcessor
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_graduation_queries():
    pdf_path = "data/SVPCET Details.pdf"
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return

    processor = QueryProcessor(pdf_path, gemini_api_key)

    # Simulate graduation ceremony-related queries
    queries = [
        "What is the seating arrangement?",
        "What is the dress code for the ceremony?",
        "Can you provide the schedule for the event?",
        "Where do guests enter and exit?",
        "What are the felicitation details?"
    ]

    for query in queries:
        print(f"Query: {query}")
        response = processor.process_query(query)
        print(f"Response: {response}\n")

if __name__ == "__main__":
    test_graduation_queries()
