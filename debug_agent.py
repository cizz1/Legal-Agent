"""
Debug script for the Legislative AI Agent.
"""

import os
import logging
from dotenv import load_dotenv
from agent import LegislativeAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("Please set GOOGLE_API_KEY in your environment or .env file")
        return
    
    logger.info("Initializing LegislativeAgent")
    agent = LegislativeAgent(api_key)
    
    pdf_path = "temp_pdf.pdf"  # This should be the path to your PDF
    
    if not os.path.exists(pdf_path):
        logger.warning("Sample PDF not found at %s. Please provide a valid PDF file for processing.", pdf_path)
        return
    
    try:
        logger.info("Starting legislation processing pipeline")
        results = agent.process_legislation(
            pdf_path=pdf_path,
            output_path="legislation_analysis.json"
        )
        
        logger.info("Processing completed successfully")
        logger.info("Summary length: %d characters", len(results["summary"]))
        logger.info("Sections extracted: %d", len([k for k, v in results["sections"].items() if v]))
        logger.info("Rule checks performed: %d", len(results["rule_checks"]))
        
        print("\n=== EXECUTIVE SUMMARY ===")
        print(results["summary"])
        
        print("\n=== EXTRACTED SECTIONS ===")
        for section, content in results["sections"].items():
            if content:
                print(f"\n{section.upper()}:")
                print(content[:200] + "..." if len(content) > 200 else content)
        
        print("\n=== RULE CHECKS ===")
        for rule_check in results["rule_checks"]:
            print(f"\nRule: {rule_check['rule']}")
            print(f"Status: {rule_check['status']}")
            print(f"Confidence: {rule_check['confidence']}")
            print(f"Evidence: {rule_check['evidence'][:100]}..." if len(rule_check['evidence']) > 100 else rule_check['evidence'])
        
        logger.info("Debug script completed")
        
    except Exception as e:
        logger.error("Error processing legislation: %s", str(e), exc_info=True)

if __name__ == "__main__":
    main()