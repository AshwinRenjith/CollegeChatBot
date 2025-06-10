from typing import Dict, Any, Optional
import logging
from .pdf_parser import PDFParser
from .gemini_client import GeminiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryProcessor:
    def __init__(self, pdf_path: str):
        """Initialize the query processor with PDF parser and Gemini client."""
        self.pdf_parser = PDFParser()
        self.gemini_client = GeminiClient()
        self.pdf_content = self.pdf_parser.parse_pdf(pdf_path)
        
        # Common section keywords for quick lookup
        self.section_keywords = {
            'courses': ['course', 'program', 'degree', 'major', 'curriculum'],
            'admissions': ['admission', 'apply', 'application', 'requirements', 'deadline'],
            'fees': ['fee', 'tuition', 'cost', 'payment', 'scholarship'],
            'facilities': ['facility', 'campus', 'infrastructure', 'building', 'lab'],
            'events': ['event', 'activity', 'program', 'seminar', 'workshop']
        }

    def process_query(self, query: str) -> str:
        """
        Process a user query and generate a response.
        """
        try:
            # Analyze the query
            analysis = self.gemini_client.analyze_query(query)
            
            # Get relevant content based on intent
            relevant_content = self._get_relevant_content(analysis)
            
            if not relevant_content:
                return "I apologize, but I couldn't find specific information about that in the college document."
            
            # Generate response using Gemini
            response = self.gemini_client.generate_response(query, relevant_content)
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "I apologize, but I encountered an error while processing your query. Please try again."

    def _get_relevant_content(self, analysis: Dict[str, Any]) -> Optional[str]:
        """
        Extract relevant content from the PDF based on query analysis.
        """
        try:
            intent = analysis['intent'].lower()
            
            # Find matching section keywords
            matching_sections = []
            for section, keywords in self.section_keywords.items():
                if any(keyword in intent for keyword in keywords):
                    matching_sections.extend(keywords)
            
            if not matching_sections:
                # If no specific section matches, return a larger context
                return self.pdf_content[:2000]  # First 2000 characters as context
            
            # Get content from matching sections
            section_content = self.pdf_parser.get_section_content(
                self.pdf_content,
                matching_sections
            )
            
            return section_content if section_content else self.pdf_content[:2000]
            
        except Exception as e:
            logger.error(f"Error getting relevant content: {str(e)}")
            return None 