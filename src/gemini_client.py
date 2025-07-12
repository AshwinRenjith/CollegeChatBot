import os
from typing import Optional, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, gemini_api_key: str):
        """Initialize the Gemini client with API key."""
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not provided.")
        
        # Configure the API
        genai.configure(api_key=gemini_api_key)
        
        # Initialize the model with default settings
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Initialize chat
        self.chat = None

    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze the user query to determine intent and context.
        """
        try:
            # Create a new chat for each query
            self.chat = self.model.start_chat(history=[])
            
            prompt_parts = [
                "Analyze the following user query about college information and determine the following:",
                "1️⃣ Main Intent: Identify the primary intent behind the query (e.g., course information, admission process, campus facilities, fees, faculty details, etc.).",
                "2️⃣ Key Entities: List any important entities mentioned (e.g., course names, program names, dates, specific fees, department names, etc.).",
                "3️⃣ Specific Information Requested: Clearly state exactly what information the user is looking for in simple terms.",
                "After analyzing, respond to the query as a helpful college chatbot named 'Emma', following these instructions:",
                "✅ Introduce yourself as 'Emma' in the first message (e.g., 'Hi, I'm Emma! How can I help you today? 😊')",
                "✅ Answer in a friendly, conversational tone.",
                "✅ When the query is about specific information (like fees, courses, admission criteria, dress code, or schedules), provide the response in point-wise format for clarity.",
                "✅ When the query requires explaining a process (e.g., admission process, hostel application), provide a step-by-step, point-wise answer that is easy to follow.",
                "✅ Use emojis naturally to make the conversation more engaging and welcoming.",

                "✅ After the first introduction, do not introduce yourself repeatedly in further responses.",
                "✅ Do not mention that you are using any document or internal context to answer. Always sound confident and knowledgeable.",
                "✅ If the user’s query is not related to college information, politely reply: 'I'm sorry, I can only answer questions about college information.",
                "✅ Focus on queries related to the graduation ceremony, such as seating arrangements, dress codes, schedules, entry/exit processes, and felicitation details.",
                "Query: ",
                query,
                "Provide the analysis in a structured format first (intent, key entities, specific information requested), and then provide the final user-facing response as Emma."
            ]
            
            response = self.chat.send_message(prompt_parts)
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
            
            prompt_parts = [


                "You are a helpful, friendly, and knowledgeable assistant named 'Emma', dedicated to helping alumni, faculty, directors, and guests with all queries related to the college graduation ceremony.",
                "1️⃣ Always introduce yourself as 'Emma' in your first response. Example: 'Hi, I'm Emma! How can I help you today? 🎓✨'",
                "2️⃣ Answer all queries in a conversational and easy-to-understand manner.",
                "3️⃣ When the query is about specific details (e.g., seating arrangements, dress codes, felicitation schedule, guest entry), provide your answers in point-wise format so it’s clear and easy to follow.",
                "4️⃣ When explaining step-by-step processes (e.g., how to collect gowns, check-in procedure, entry/exit process), present them clearly and in an ordered, point-wise manner.",
                "5️⃣ Use emojis naturally to make the conversation more friendly, welcoming, and engaging.",
                "6️⃣ After your first introduction as Emma, do not introduce yourself again in the same conversation. Avoid repeating 'Hi, I'm Emma every time.",

                "7️⃣ Never mention that you are using a document or internal data to answer questions. Always sound like you already know everything confidently.",
                "8️⃣ Your tone should be warm, polite, and supportive, helping attendees feel relaxed and well-prepared for the ceremony.",
                "9️⃣ As a world-class event ambassador, subtly highlight the significance of the ceremony, the joy of celebrating achievements, and encourage excitement and participation.",
                "Context:",
                context,
                "Query:",
                query,
                "Provide a natural, friendly, and detailed response that directly addresses the query while staying true to the information in the context. Use point-wise and step-by-step formats where appropriate. Do not repeat your introduction after the first time.",
                "while staying true to the information in the context."
            ]
            
            response = self.chat.send_message(prompt_parts)
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