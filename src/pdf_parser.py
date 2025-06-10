import os
from typing import Dict, List, Optional
import PyPDF2
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFParser:
    def __init__(self, cache_dir: str = "cache"):
        """Initialize the PDF parser with caching support."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self._content_cache: Dict[str, str] = {}

    def parse_pdf(self, pdf_path: str) -> str:
        """
        Parse a PDF file and extract its text content.
        Implements caching to avoid re-parsing the same file.
        """
        pdf_path = Path(pdf_path)
        cache_file = self.cache_dir / f"{pdf_path.stem}_content.txt"

        # Check cache first
        if pdf_path.name in self._content_cache:
            return self._content_cache[pdf_path.name]

        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self._content_cache[pdf_path.name] = content
                return content

        try:
            content = self._extract_text_from_pdf(pdf_path)
            
            # Cache the content
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(content)
            self._content_cache[pdf_path.name] = content
            
            return content
        except Exception as e:
            logger.error(f"Error parsing PDF {pdf_path}: {str(e)}")
            raise

    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text content from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text_content = []
                
                for page in reader.pages:
                    text_content.append(page.extract_text())
                
                return '\n'.join(text_content)
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise

    def get_section_content(self, content: str, section_keywords: List[str]) -> Optional[str]:
        """
        Extract content related to a specific section based on keywords.
        """
        try:
            lines = content.split('\n')
            section_content = []
            in_section = False
            
            for line in lines:
                if any(keyword.lower() in line.lower() for keyword in section_keywords):
                    in_section = True
                    section_content.append(line)
                elif in_section and line.strip():
                    section_content.append(line)
                elif in_section and not line.strip():
                    break
            
            return '\n'.join(section_content) if section_content else None
        except Exception as e:
            logger.error(f"Error extracting section content: {str(e)}")
            return None 