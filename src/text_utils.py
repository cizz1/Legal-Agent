"""
Text Utilities Module for PDF text extraction, cleaning, and chunking.
"""

import re
import fitz  # PyMuPDF
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file using PyMuPDF."""
    logger.info("Extracting text from PDF: %s", pdf_path)
    doc = fitz.open(pdf_path)
    text = ""
    for page_num, page in enumerate(doc):
        page_text = page.get_text()
        text += page_text
        logger.debug("Extracted text from page %d, length: %d", page_num, len(page_text))
    doc.close()
    logger.info("PDF text extraction completed, total length: %d", len(text))
    return text

def clean_text(text: str) -> str:
    """Clean extracted text by removing artifacts and normalizing whitespace."""
    logger.info("Cleaning text of length %d", len(text))
    # Remove page numbers and page indicators
    text = re.sub(r"Page\s*\d+\s*of\s*\d+", "", text)
    
    # Multiple blank lines → one
    text = re.sub(r"\n{2,}", "\n", text)
    
    # Remove isolated numbers (often page numbers)
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    
    # Remove non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)
    
    result = text.strip()
    logger.info("Text cleaning completed, final length: %d", len(result))
    return result

def chunk_text(text: str, chunk_size: int = 6000) -> list:
    """Split text into chunks of specified size."""
    logger.info("Chunking text of length %d with chunk size %d", len(text), chunk_size)
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    logger.info("Text chunking completed, created %d chunks", len(chunks))
    return chunks