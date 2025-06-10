import streamlit as st
import os
from src.query_processor import QueryProcessor
import logging
from datetime import datetime
import time

# Set page config first
st.set_page_config(
    page_title="College Information Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
        padding: 0;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    /* Header styling */
    .header {
        background-color: white;
        padding: 1rem 2rem;
        border-bottom: 1px solid #e0e0e0;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .title {
        color: #1a73e8;
        font-size: 1.5rem;
        font-weight: 500;
        margin: 0;
    }
    .subtitle {
        color: #5f6368;
        font-size: 0.9rem;
        margin: 0.25rem 0 0 0;
    }

    /* Suggested queries styling */
    .suggested-queries {
        background-color: white;
        padding: 1rem 2rem;
        border-bottom: 1px solid #e0e0e0;
    }
    .query-bubbles {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    .query-bubble {
        background-color: #e8f0fe;
        color: #1a73e8;
        padding: 0.5rem 1rem;
        border-radius: 16px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid #c2d7f5;
    }
    .query-bubble:hover {
        background-color: #d2e3fc;
        transform: translateY(-1px);
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .suggested-title {
        color: #5f6368;
        font-size: 0.9rem;
        margin: 0;
    }

    /* Chat container styling */
    .chat-container {
        background-color: white;
        padding: 1rem 2rem;
        flex: 1;
        overflow-y: auto;
        scroll-behavior: smooth;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.75rem;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 1rem;
        max-width: 85%;
        animation: fadeIn 0.3s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .chat-message.user {
        background-color: #e8f0fe;
        margin-left: auto;
    }
    .chat-message.bot {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
    }
    .chat-message .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        object-fit: cover;
        flex-shrink: 0;
    }
    .chat-message .message {
        flex: 1;
        line-height: 1.5;
        font-size: 0.95rem;
        color: #202124;
    }
    .chat-message.user .message {
        color: #1a73e8;
    }

    /* Input container styling */
    .input-container {
        background-color: white;
        padding: 1rem 2rem;
        border-top: 1px solid #e0e0e0;
        position: sticky;
        bottom: 0;
        z-index: 100;
    }
    .stTextInput>div>div>input {
        border-radius: 24px;
        padding: 12px 20px;
        font-size: 0.95rem;
        border: 1px solid #e0e0e0;
        background-color: #f8f9fa;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #1a73e8;
        box-shadow: 0 1px 6px rgba(26,115,232,0.2);
        background-color: white;
    }
    .stButton>button {
        border-radius: 24px;
        background-color: #1a73e8;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1557b0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    /* Clear button styling */
    .clear-button {
        text-align: center;
        padding: 0.5rem;
        background-color: white;
    }
    .clear-button button {
        background-color: transparent;
        color: #5f6368;
        border: 1px solid #e0e0e0;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    .clear-button button:hover {
        background-color: #f8f9fa;
        border-color: #dadce0;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    ::-webkit-scrollbar-thumb {
        background: #dadce0;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #bdc1c6;
    }

    /* Fix for Streamlit's default container */
    .stApp > div {
        height: 100%;
    }
    .stApp > div > div {
        height: 100%;
    }
    .stApp > div > div > div {
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'processor' not in st.session_state:
        st.session_state.processor = QueryProcessor("data/SVPCET Details.pdf")
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def display_chat_message(role, content):
    """Display a chat message with appropriate styling."""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=user&backgroundColor=b6e3f4" class="avatar"/>
            <div class="message">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=bot&backgroundColor=ffdfbf" class="avatar"/>
            <div class="message">{content}</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    initialize_session_state()

    # Header
    st.markdown("""
        <div class="header">
            <h1 class="title">🎓 College Information Assistant</h1>
            <p class="subtitle">Ask me anything about SVPCET</p>
        </div>
    """, unsafe_allow_html=True)

    # Chat interface
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.messages:
            display_chat_message(message["role"], message["content"])

        st.markdown('</div>', unsafe_allow_html=True)

    # Input container
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    
    with col1:
        prompt = st.text_input("", placeholder="Ask a question about SVPCET...", key="chat_input")
    
    with col2:
        send_button = st.button("Send", use_container_width=True)

    if (prompt and send_button) or (prompt and st.session_state.get("_last_prompt") != prompt):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt)

        # Get bot response with typing animation
        with st.spinner(''):
            try:
                response = st.session_state.processor.process_query(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                display_chat_message("assistant", response)
            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                display_chat_message("assistant", error_message)
        
        # Clear the input
        st.session_state["_last_prompt"] = prompt
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Clear chat button
    st.markdown('<div class="clear-button">', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 