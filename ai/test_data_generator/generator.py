"""
AI-Assisted Test Data Generator.

Generates realistic structured datasets for API payloads, boundary testing, and negative tests.
"""

from typing import Any, Dict, Optional
from ai.providers import AIProvider, get_ai_provider
from ai.prompts import TEST_DATA_GENERATION_PROMPT
from utils.logger import get_logger

logger = get_logger("TestDataGenerator")


class TestDataGenerator:
    """Generates synthetic test data using AI provider abstraction."""

    def __init__(self, provider: Optional[AIProvider] = None):
        self.provider = provider or get_ai_provider()

    def generate_dataset(self, dataset_type: str = "User Accounts") -> Dict[str, Any]:
        """
        Generate structured test data records.

        :param dataset_type: Description of dataset
        :return: JSON object containing generated records
        """
        logger.info(f"Generating synthetic test dataset for '{dataset_type}'...")
        prompt = TEST_DATA_GENERATION_PROMPT.format(dataset_type=dataset_type)
        schema_desc = """
        {
            "dataset_name": "string",
            "total_records": int,
            "records": [
                {
                    "type": "valid|boundary|invalid",
                    "username": "string",
                    "email": "string",
                    "age": int,
                    "role": "string",
                    "status": "string"
                }
            ]
        }
        """
        result = self.provider.generate_structured_json(
            prompt=prompt,
            schema_description=schema_desc,
        )
        logger.info(f"Generated {result.get('total_records', 0)} synthetic test data records.")
        return result
