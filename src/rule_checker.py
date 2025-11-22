"""
Rule Checker Module for checking compliance of legislation text against predefined rules.
"""

import google.generativeai as genai
import json
import logging
import re
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the 6 specific legal document rules
LEGAL_DOCUMENT_RULES = [
    "Act must define key terms",
    "Act must specify eligibility criteria", 
    "Act must specify what the authority (government) must do",
    "Act must list penalties or enforcement methods",
    "Act must explain how to calculate payments",
    "Act must require records or reporting"
]

class RuleChecker:
    """Rule compliance checking using Google Gemini API."""
    
    def __init__(self, api_key: str):
        """Initialize the RuleChecker with Google Gemini API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash",
                                         generation_config={"temperature": 0.3})
        logger.info("RuleChecker initialized with Gemini 2.5 Flash model (temperature=0.3)")
    
    def apply_rule_checks(self, text: str) -> List[Dict[str, Any]]:
        """Apply legal document rule checks to the legislation text."""
        logger.info("Applying %d legal document rule checks", len(LEGAL_DOCUMENT_RULES))
        
        # Create a prompt that asks for all 6 rules at once in the required JSON format
        prompt = f"""
        Analyze the following legal document/Act text and check if it follows these 6 specific rules:
        
        1. Act must define key terms
        2. Act must specify eligibility criteria
        3. Act must specify what the authority (government) must do
        4. Act must list penalties or enforcement methods
        5. Act must explain how to calculate payments
        6. Act must require records or reporting
        
        For each rule, determine if it 'passes' or 'fails', extract the specific text snippet (evidence) that proves it, and give a confidence score (0-100).
        
        Return the results as a JSON array exactly in this format:
        [
          {{
            "rule": "Act must define key terms",
            "status": "pass",
            "evidence": "Section 2 - Definitions: 'In this Act, unless the context otherwise requires...'",
            "confidence": 95
          }},
          {{
            "rule": "Act must specify eligibility criteria",
            "status": "pass", 
            "evidence": "Section 4 - Eligibility: 'A person is eligible if they are over 18...'",
            "confidence": 90
          }}
          // ... repeat for all 6 rules
        ]
        
        Legal document/Act text:
        {text}
        """
        
        response = self.model.generate_content(prompt)
        # Log the raw response from the LLM
        logger.info("Raw LLM response for legal document rule checks: %s", response.text)
        
        # Try to extract JSON from markdown code blocks if present
        response_text = response.text
        # Remove markdown code block wrappers if present
        json_match = re.search(r'```(?:json)?\s*({.*?}|\[.*?\])\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
            logger.info("Extracted JSON from markdown code block for legal document rule checks")
        
        try:
            result = json.loads(response_text)
            # Ensure we return a list
            if isinstance(result, list):
                logger.info("Legal document rule checks completed successfully with %d rules", len(result))
                return result
            else:
                logger.warning("Expected list response but got: %s", type(result))
                return self._create_default_rule_checks()
        except json.JSONDecodeError as e:
            # If JSON parsing fails, create default rule checks
            logger.warning("Failed to parse legal document rule check response as JSON: %s", str(e))
            logger.warning("Response text: %s", response_text)
            return self._create_default_rule_checks()
    
    def _create_default_rule_checks(self) -> List[Dict[str, Any]]:
        """Create default rule checks when LLM response cannot be parsed."""
        default_checks = []
        for rule in LEGAL_DOCUMENT_RULES:
            default_checks.append({
                "rule": rule,
                "status": "fail",
                "evidence": "Could not process",
                "confidence": 0
            })
        return default_checks