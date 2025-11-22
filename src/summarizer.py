"""
Summarizer Module for text summarization using Google Gemini API.
"""

import google.generativeai as genai
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Summarizer:
    """Text summarization using Google Gemini API."""
    
    def __init__(self, api_key: str):
        """Initialize the Summarizer with Google Gemini API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash", 
                                         generation_config={"temperature": 0.3})
        logger.info("Summarizer initialized with Gemini 2.5 Flash model (temperature=0.3)")
    
    def summarize_chunk(self, chunk: str) -> str:
        """Summarize a single text chunk using Gemini."""
        logger.info("Summarizing chunk of length %d", len(chunk))
        prompt = f"""
        Summarize the following text in 3–4 bullet points:
        
        {chunk}
        """
        response = self.model.generate_content(prompt)
        # Log the raw response from the LLM
        logger.info("Raw LLM response for chunk: %s", response.text)
        result = response.text if response.text else ""
        logger.info("Chunk summary generated with length %d", len(result))
        return result
    
    def summarize_chunks(self, chunks: List[str]) -> List[str]:
        """Generate summaries for all text chunks."""
        logger.info("Summarizing %d chunks", len(chunks))
        summaries = []
        for i, chunk in enumerate(chunks):
            logger.info("Processing chunk %d/%d", i+1, len(chunks))
            summary = self.summarize_chunk(chunk)
            summaries.append(summary)
        logger.info("All chunks summarized")
        return summaries
    
    def combine_summaries(self, chunk_summaries: List[str]) -> str:
        """Combine chunk summaries into a final comprehensive summary."""
        logger.info("Combining %d chunk summaries", len(chunk_summaries))
        combined_text = "\n\n".join(chunk_summaries)
        prompt = f"""
        Using these sub-summaries, create one final summary (5–10 bullet points) covering:
        - Purpose
        - Definitions
        - Eligibility
        - Obligations
        - Enforcement
        
        Sub-summaries:
        {combined_text}
        """
        response = self.model.generate_content(prompt)
        # Log the raw response from the LLM
        logger.info("Raw LLM response for combined summary: %s", response.text)
        result = response.text if response.text else ""
        logger.info("Final summary generated with length %d", len(result))
        return result