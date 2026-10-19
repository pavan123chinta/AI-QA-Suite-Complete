"""
Optional External LLM Provider Implementation.

Integrates with OpenAI-compatible REST endpoints if an API key is provided.
Gracefully falls back to MockAIProvider if key is missing or calls fail.
Zero hardcoded keys.
"""

import json
from typing import Any, Dict, Optional
import requests

from ai.providers.ai_provider import AIProvider
from ai.providers.mock_provider import MockAIProvider
from utils.config import config
from utils.logger import get_logger

logger = get_logger("LLMProvider")


class LLMProvider(AIProvider):
    """
    External LLM Provider for OpenAI / Compatible APIs.
    Safe: Automatically falls back to MockAIProvider if unconfigured or unreachable.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ):
        self.api_key = api_key or config.llm_api_key
        self.base_url = (base_url or config.llm_base_url).rstrip("/")
        self.model = model or config.llm_model
        self.temperature = temperature if temperature is not None else config.llm_temperature
        self._mock_fallback = MockAIProvider()

        if not self.api_key:
            logger.info("No LLM_API_KEY detected. LLMProvider running in Mock Fallback mode.")
        else:
            logger.info(f"LLMProvider initialized with model '{self.model}' at '{self.base_url}'")

    def generate_text(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate text via external LLM with automatic mock fallback."""
        if not self.api_key:
            return self._mock_fallback.generate_text(prompt, system_message)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            logger.warning(f"External LLM API call failed ({exc}). Falling back to MockAIProvider.")
            return self._mock_fallback.generate_text(prompt, system_message)

    def generate_structured_json(
        self, prompt: str, schema_description: Optional[str] = None, system_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate structured JSON via external LLM with automatic mock fallback."""
        if not self.api_key:
            return self._mock_fallback.generate_structured_json(prompt, schema_description, system_message)

        json_sys_msg = (
            (system_message or "")
            + "\nYou MUST respond strictly in valid, parseable JSON format. Do not wrap in markdown tags or extra commentary."
        )
        if schema_description:
            json_sys_msg += f"\nExpected JSON schema structure:\n{schema_description}"

        raw_text = self.generate_text(prompt=prompt, system_message=json_sys_msg)

        try:
            # Clean markdown codeblocks if LLM returned ```json ... ```
            cleaned = raw_text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("```", 1)[0]
            return json.loads(cleaned.strip())
        except Exception as json_err:
            logger.warning(f"Failed to parse external LLM response as JSON ({json_err}). Falling back to Mock Provider.")
            return self._mock_fallback.generate_structured_json(prompt, schema_description, system_message)
