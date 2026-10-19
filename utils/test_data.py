"""
Test Data Management Utilities.

Loads structured test datasets (JSON, text) with caching and schema helper functions.
"""

import json
from typing import Any, Dict, List, Union
from utils.config import config
from utils.logger import get_logger

logger = get_logger("TestDataManager")


class TestDataManager:
    """Utility class to read and manage test data files from test_data directory."""

    @staticmethod
    def load_json(file_name: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Load and parse a JSON test data file.

        :param file_name: Name of the JSON file (e.g. 'api_data.json')
        :return: Parsed dictionary or list
        """
        file_path = config.test_data_dir / file_name
        if not file_path.exists():
            error_msg = f"Test data file not found: {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"Successfully loaded JSON test data from {file_name}")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON file {file_name}: {e}")
            raise

    @staticmethod
    def load_text(file_name: str) -> str:
        """
        Load raw text content (e.g., sample log files).

        :param file_name: Name of the text file
        :return: String content of file
        """
        file_path = config.test_data_dir / file_name
        if not file_path.exists():
            error_msg = f"Test data file not found: {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            logger.debug(f"Loaded raw text data from {file_name} ({len(content)} chars)")
            return content
