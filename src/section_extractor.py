"""
Section Extractor Module for extracting specific sections from legislation text.
"""

import google.generativeai as genai
import json
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SectionExtractor:
    """Section extraction from legislation text using Google Gemini API."""
    
    def __init__(self, api_key: str):
        """Initialize the SectionExtractor with Google Gemini API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash",
                                         generation_config={"temperature": 0.3})
        logger.info("SectionExtractor initialized with Gemini 2.5 Flash model (temperature=0.3)")
    
    def extract_sections(self, text: str) -> dict:
        """Extract specific sections from the legislation text."""
        logger.info("Extracting sections from text of length %d", len(text))
        prompt = f"""
        Extract the following from the Act text:
        
        - Definitions
        - Obligations
        - Responsibilities
        - Eligibility
        - Payments
        - Penalties
        - Record-keeping
        
        Return JSON exactly in this format:
        {{
          "definitions": "...",
          "obligations": "...",
          "responsibilities": "...",
          "eligibility": "...",
          "payments": "...",
          "penalties": "...",
          "record_keepin": "..."
        }}
        
        Act text:
        {text}
        """
        response = self.model.generate_content(prompt)
        
        logger.info("Raw LLM response: %s", response.text)
        

        response_text = response.text
        
        json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
            logger.info("Extracted JSON from markdown code block")
        
        try:
            result = json.loads(response_text)
            logger.info("Sections extracted successfully")
            return result
        except json.JSONDecodeError as e:
            
            logger.warning("Failed to parse section extraction response as JSON: %s", str(e))
            logger.warning("Response text: %s", response_text)
            return {
                "definitions": "",
                "obligations": "",
                "responsibilities": "",
                "eligibility": "",
                "payments": "",
                "penalties": "",
                "record_keeping": ""
            }