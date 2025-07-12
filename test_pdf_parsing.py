from src.pdf_parser import PDFParser
from src.query_processor import QueryProcessor
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_pdf_parsing():
    pdf_path = "data/SVPCET Details.pdf"
    parser = PDFParser()

    # Parse the PDF
    content = parser.parse_pdf(pdf_path)
    print("Parsed PDF Content:")
    print(content[:500])  # Print the first 500 characters

def test_query_processing():
    pdf_path = "data/SVPCET Details.pdf"
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return

    processor = QueryProcessor(pdf_path, gemini_api_key)

    # Simulate a query
    query = "What are the courses offered?"
    response = processor.process_query(query)
    print("Query Response:")
    print(response)

if __name__ == "__main__":
    print("Testing PDF Parsing...")
    test_pdf_parsing()

    print("\nTesting Query Processing...")
    test_query_processing()
