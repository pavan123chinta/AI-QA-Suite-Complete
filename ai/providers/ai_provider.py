"""
AI Provider Abstract Base Class.

Defines the contract for AI operations across local/mock implementations and external LLMs.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class AIProvider(ABC):
    """
    Abstract AI Provider Interface.

    Enables pluggable AI backends (Mock/Rule-based, OpenAI, Gemini, Local Ollama)
    without breaking test automation or requiring paid API access.
    """

    @abstractmethod
    def generate_text(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Generate raw text response from prompt.

        :param prompt: User prompt / instruction
        :param system_message: Optional system role prompt
        :return: Generated text string
        """
        pass

    @abstractmethod
    def generate_structured_json(
        self, prompt: str, schema_description: Optional[str] = None, system_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response adhering to expected schema.

        :param prompt: User prompt
        :param schema_description: Description or structure expected
        :param system_message: System instructions
        :return: Parsed JSON dictionary
        """
        pass
