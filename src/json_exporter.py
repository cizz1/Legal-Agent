"""
JSON Exporter Module for exporting results to JSON files.
"""

import json
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JSONExporter:
    """Export results to JSON files."""
    
    @staticmethod
    def export_json(summary: str, sections: Dict[str, str], 
                   rule_checks: List[Dict[str, Any]], path: str) -> None:
        """Export the results to a JSON file."""
        logger.info("Exporting results to JSON file: %s", path)
        output = {
            "summary": summary,
            "sections": sections,
            "rule_checks": rule_checks
        }
        with open(path, 'w') as f:
            json.dump(output, f, indent=2)
        logger.info("JSON export completed")
    
    @staticmethod
    def export_chunk_summaries(summaries: List[str], path: str) -> None:
        """Export chunk summaries to a JSON file."""
        logger.info("Exporting chunk summaries to JSON file: %s", path)
        output = {
            "chunk_summaries": summaries
        }
        with open(path, 'w') as f:
            json.dump(output, f, indent=2)
        logger.info("Chunk summaries export completed")