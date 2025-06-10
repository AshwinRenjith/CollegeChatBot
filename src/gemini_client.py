import os
from typing import Optional, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        """Initialize the Gemini client with API key."""
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Initialize the model with default settings
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize chat
        self.chat = None

    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze the user query to determine intent and context.
        """
        try:
            # Create a new chat for each query
            self.chat = self.model.start_chat(history=[])
            
            prompt = f"""
            Analyze the following query about college information and determine:
            1. The main intent (e.g., course info, admission process, campus facilities)
            2. Key entities mentioned
            3. Specific information being requested
            
            Query: {query}
            
            Provide the analysis in a structured format.
            """
            
            response = self.chat.send_message(prompt)
            return self._parse_analysis(response.text)
        except Exception as e:
            logger.error(f"Error analyzing query: {str(e)}")
            raise

    def generate_response(self, query: str, context: str) -> str:
        """
        Generate a response based on the query and context from PDF.
        """
        try:
            # Create a new chat for each response
            self.chat = self.model.start_chat(history=[])
            
            prompt = f"""
            Based on the following context from a college information document, 
            provide a clear and concise answer to the user's query.
            
            Context:
            {context}
            
            Query:
            {query}
            
            Provide a natural, conversational response that directly addresses the query
            while staying true to the information in the context.
            """
            
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def _parse_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """
        Parse the analysis text into a structured format.
        """
        try:
            # Basic parsing logic - can be enhanced based on actual response format
            lines = analysis_text.split('\n')
            analysis = {
                'intent': '',
                'entities': [],
                'specific_info': []
            }
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if 'intent' in line.lower():
                    current_section = 'intent'
                    analysis['intent'] = line.split(':', 1)[1].strip()
                elif 'entities' in line.lower():
                    current_section = 'entities'
                elif 'specific' in line.lower():
                    current_section = 'specific_info'
                elif current_section and line.startswith('-'):
                    analysis[current_section].append(line[1:].strip())
            
            return analysis
        except Exception as e:
            logger.error(f"Error parsing analysis: {str(e)}")
            return {
                'intent': 'unknown',
                'entities': [],
                'specific_info': []
            } 