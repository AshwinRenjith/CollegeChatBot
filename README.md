# 🎓 College Graduation Ceremony Chatbot ✨

Meet **Emma**, your friendly and intelligent chatbot designed to assist alumni, faculty, directors, and guests with all queries related to the graduation ceremony. Emma ensures a smooth and memorable event experience by providing quick, accurate, and delightful responses. 🌟

---

## 🌟 Features

- 🤖 **Natural Language Query Processing**: Understands and responds to user queries conversationally.
- 📄 **PDF Document Parsing**: Extracts and analyzes event details from the provided PDF.
- 🎉 **Event-Specific Assistance**: Handles queries about:
  - 🪑 Seating arrangements
  - 👗 Dress codes
  - 🏆 Felicitation schedules
  - 🚪 Guest entry and exit processes
  - 📅 Other ceremony-related details
- 💻 **Multi-Interface Support**:
  - Command-line interface
  - Modern web interface using Streamlit
- 😊 **Engaging Responses**: Uses emojis and a warm tone to make interactions delightful.

---

## 🛠️ Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd CollegeChatBot
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

5. **Add Event Details**:
   - Place the graduation ceremony PDF (e.g., `SVPCET Details.pdf`) in the `data` directory.

---

## 🚀 Usage

### Command-Line Interface
Interact with the chatbot via the terminal:
```bash
python cli.py
```

### Web Interface
Launch the chatbot in your browser using Streamlit:
```bash
streamlit run web_app.py
```

---

## 📂 Project Structure

- **`src/`**: Source code directory
  - `pdf_parser.py`: Extracts and processes text from PDFs
  - `query_processor.py`: Analyzes queries and retrieves relevant information
  - `gemini_client.py`: Integrates with the Gemini API for intelligent responses
- **`data/`**: Directory for storing event-related PDFs
- **`cli.py`**: Command-line interface for the chatbot
- **`web_app.py`**: Streamlit-based web interface

---

## 🎯 Features in Detail

### 📄 PDF Processing
- Efficiently extracts text from PDFs with caching to improve performance.
- Supports section-based content extraction for targeted responses.

### 🤖 Query Processing
- Understands user intent and identifies key entities.
- Provides context-aware, step-by-step, and point-wise responses.

### 💻 User Interface
- **Command-Line**: Simple and interactive terminal-based interface.
- **Web Interface**: Modern, responsive, and user-friendly web app.

---

## 🛡️ Error Handling

The system includes robust error handling for:
- Missing or malformed PDFs
- API connection issues
- Invalid or unsupported queries

---

## ⚡ Performance Optimization

- Caches parsed PDF content to avoid redundant processing.
- Optimized query handling for frequently asked questions.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit a pull request to improve Emma or add new features.

---

## 🎉 Meet Emma

Emma is here to make your graduation ceremony unforgettable! Whether you need help with seating, schedules, or dress codes, Emma has got you covered. Let’s celebrate your achievements together! 🎓✨