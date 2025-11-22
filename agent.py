"""
Main Legislative Agent Module for processing legislation PDFs using Google Gemini API.
"""

import sys
import os
import logging
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import google.generativeai as genai
from src.text_utils import extract_text_from_pdf, clean_text, chunk_text
from src.summarizer import Summarizer
from src.section_extractor import SectionExtractor
from src.rule_checker import RuleChecker
from src.json_exporter import JSONExporter
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LegislativeAgent:
    """Main agent for processing legislation PDFs."""
    
    def __init__(self, api_key: str):
        """Initialize the LegislativeAgent with Google Gemini API key."""
        self.api_key = api_key
        self.summarizer = Summarizer(api_key)
        self.section_extractor = SectionExtractor(api_key)
        self.rule_checker = RuleChecker(api_key)
        self.json_exporter = JSONExporter()
        logger.info("LegislativeAgent initialized")
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        logger.info("Starting text extraction from PDF: %s", pdf_path)
        return extract_text_from_pdf(pdf_path)
    
    def clean_text(self, raw_text: str) -> str:
        """Clean extracted text by removing artifacts and normalizing."""
        logger.info("Starting text cleaning")
        return clean_text(raw_text)
    
    def chunk_text(self, text: str, chunk_size: int = 6000) -> List[str]:
        """Split text into chunks of specified size."""
        logger.info("Starting text chunking with chunk size: %d", chunk_size)
        return chunk_text(text, chunk_size)
    
    def summarize_chunks(self, chunks: List[str]) -> List[str]:
        """Generate summaries for all chunks."""
        logger.info("Starting chunk summarization")
        return self.summarizer.summarize_chunks(chunks)
    
    def combine_summaries(self, chunk_summaries: List[str]) -> str:
        """Combine all chunk summaries into a final comprehensive summary."""
        logger.info("Starting summary combination")
        return self.summarizer.combine_summaries(chunk_summaries)
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract specific sections from the legislation text."""
        logger.info("Starting section extraction")
        return self.section_extractor.extract_sections(text)
    
    def apply_rule_checks(self, text: str) -> List[Dict[str, Any]]:
        """Apply legal document rule checks to the legislation text."""
        logger.info("Starting legal document rule checks")
        return self.rule_checker.apply_rule_checks(text)
    
    def export_json(self, summary: str, sections: Dict[str, str], 
                   rule_checks: List[Dict[str, Any]], path: str) -> None:
        """Export the results to a JSON file."""
        logger.info("Starting JSON export to: %s", path)
        self.json_exporter.export_json(summary, sections, rule_checks, path)
    
    def export_chunk_summaries(self, summaries: List[str], path: str) -> None:
        """Export chunk summaries to a JSON file."""
        logger.info("Starting chunk summaries export to: %s", path)
        self.json_exporter.export_chunk_summaries(summaries, path)
    
    def load_existing_chunk_summaries(self, path: str = "chunk_summaries.json") -> List[str]:
        """Load existing chunk summaries from file if available."""
        if os.path.exists(path):
            logger.info("Loading existing chunk summaries from: %s", path)
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    if "chunk_summaries" in data:
                        logger.info("Successfully loaded %d chunk summaries", len(data["chunk_summaries"]))
                        return data["chunk_summaries"]
            except Exception as e:
                logger.warning("Failed to load existing chunk summaries: %s", str(e))
        return None
    
    def process_legislation(self, pdf_path: str, output_path: str = "output.json") -> Dict[str, Any]:
        """Complete processing pipeline for legislation PDF."""
        logger.info("Starting legislation processing pipeline")
        logger.info("PDF Path: %s", pdf_path)
        logger.info("Output Path: %s", output_path)
        
       
        logger.info("Step 1: Extracting text from PDF...")
        raw_text = self.extract_text(pdf_path)
        
        logger.info("Step 2: Cleaning text...")
        cleaned_text = self.clean_text(raw_text)
        
        logger.info("Step 3: Chunking text...")
        chunks = self.chunk_text(cleaned_text)
        
        logger.info("Step 4: Summarizing chunks...")
        chunk_summaries = self.load_existing_chunk_summaries()
        if chunk_summaries is None:
            logger.info("No existing chunk summaries found, generating new ones...")
            chunk_summaries = self.summarize_chunks(chunks)
            # Export chunk summaries for future use
            self.export_chunk_summaries(chunk_summaries, "chunk_summaries.json")
        else:
            logger.info("Using existing chunk summaries")
    
        logger.info("Step 5: Combining summaries...")
        final_summary = self.combine_summaries(chunk_summaries)

        logger.info("Step 6: Extracting sections...")
        sections = self.extract_sections(cleaned_text)
        
        logger.info("Step 7: Applying legal document rule checks...")
        rule_checks = self.apply_rule_checks(cleaned_text)
        
        logger.info("Step 8: Exporting results...")
        self.export_json(final_summary, sections, rule_checks, output_path)
        
        results = {
            "summary": final_summary,
            "sections": sections,
            "rule_checks": rule_checks,
            "chunk_summaries": chunk_summaries
        }
        logger.info("Legislation processing pipeline completed")
        return results