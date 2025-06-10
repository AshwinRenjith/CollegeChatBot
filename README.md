# College Information Chatbot

An intelligent chatbot that uses Google's Gemini API to answer questions about college information by analyzing PDF documents.

## Features

- Natural language query processing
- PDF document parsing and analysis
- Intelligent response generation using Gemini API
- Command-line interface
- Web interface using Streamlit
- Efficient PDF text extraction with caching
- Section-based content extraction

## Setup Instructions

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
5. Place your college information PDF in the `data` directory

## Usage

### Command Line Interface
```bash
python cli.py
```

### Web Interface
```bash
streamlit run web_app.py
```

## Project Structure

- `src/`: Source code directory
  - `pdf_parser.py`: PDF parsing and text extraction
  - `query_processor.py`: Query analysis and intent recognition
  - `gemini_client.py`: Gemini API integration
  - `utils.py`: Utility functions
- `data/`: Directory for PDF files
- `cli.py`: Command-line interface
- `web_app.py`: Streamlit web interface

## Features in Detail

### PDF Processing
- Efficient PDF text extraction with caching
- Section-based content extraction
- Automatic text chunking for large documents

### Query Processing
- Natural language understanding
- Context-aware responses
- Intelligent section matching

### User Interface
- Interactive command-line interface
- Modern web interface using Streamlit
- Real-time response generation

## Error Handling

The system includes robust error handling for:
- PDF parsing errors
- API connection issues
- Invalid queries
- Missing or malformed data

## Performance Optimization

- PDF content is cached after initial parsing
- Query results are cached for frequently asked questions
- Efficient text chunking for large documents

## Requirements

- Python 3.6+
- Google Generative AI
- PyPDF2
- Streamlit
- Python-dotenv
- Other dependencies listed in requirements.txt

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 