import os
import sys
from src.query_processor import QueryProcessor
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the command-line interface."""
    if len(sys.argv) != 2:
        print("Usage: python cli.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        sys.exit(1)

    try:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            print("Error: GEMINI_API_KEY not found in environment variables. Please check your .env file.")
            sys.exit(1)
            
        processor = QueryProcessor(pdf_path, gemini_api_key)
        print("\nCollege Information Chatbot")
        print("Type 'quit' or 'exit' to end the conversation\n")

        while True:
            query = input("You: ").strip()
            
            if query.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
                
            if not query:
                continue
                
            response = processor.process_query(query)
            print(f"\nBot: {response}\n")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 