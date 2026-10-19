"""
AI Provider Factory.

Instantiates configured AI provider (Mock or LLM) based on configuration.
"""

from typing import Optional
from ai.providers.ai_provider import AIProvider
from ai.providers.mock_provider import MockAIProvider
from ai.providers.llm_provider import LLMProvider
from utils.config import config
from utils.logger import get_logger

logger = get_logger("AIProviderFactory")


def get_ai_provider(provider_type: Optional[str] = None) -> AIProvider:
    """
    Factory method to retrieve configured AI Provider.

    :param provider_type: Optional override ('mock' or 'llm')
    :return: AIProvider instance
    """
    ptype = (provider_type or config.ai_provider).lower()

    if ptype == "llm":
        logger.debug("Creating LLMProvider instance.")
        return LLMProvider()
    else:
        logger.debug("Creating MockAIProvider instance (Default zero-cost mode).")
        return MockAIProvider()
