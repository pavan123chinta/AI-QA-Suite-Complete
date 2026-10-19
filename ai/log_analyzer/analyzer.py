"""
AI-Assisted Log File Analyzer.

Parses multi-line log streams, extracts error cascades, and surfaces actionable remediation.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from ai.providers import AIProvider, get_ai_provider
from ai.prompts import LOG_ANALYSIS_SYSTEM_PROMPT, LOG_ANALYSIS_USER_PROMPT
from utils.logger import get_logger

logger = get_logger("LogAnalyzer")


class LogAnalysisResult(BaseModel):
    """Structured output for log file analysis."""
    summary: str
    total_anomalies_found: int
    critical_errors: List[Dict[str, Any]]
    probable_root_cause: str
    affected_components: List[str]
    suggested_next_debugging_steps: List[str]


class LogAnalyzer:
    """Service to analyze execution logs and system traces using AI."""

    def __init__(self, provider: Optional[AIProvider] = None):
        self.provider = provider or get_ai_provider()

    def analyze_logs(self, log_content: str) -> Dict[str, Any]:
        """
        Analyze multi-line log content for anomalies and failure cascades.

        :param log_content: String containing raw log lines
        :return: Structured log diagnosis
        """
        logger.info(f"Analyzing log stream ({len(log_content)} chars)...")
        prompt = LOG_ANALYSIS_USER_PROMPT.format(log_content=log_content)
        schema_desc = """
        {
            "summary": "string",
            "total_anomalies_found": int,
            "critical_errors": [
                {
                    "service": "string",
                    "level": "ERROR|WARN",
                    "type": "string",
                    "frequency": "string",
                    "impact": "string"
                }
            ],
            "probable_root_cause": "string",
            "affected_components": ["string"],
            "suggested_next_debugging_steps": ["string"]
        }
        """
        result = self.provider.generate_structured_json(
            prompt=prompt,
            schema_description=schema_desc,
            system_message=LOG_ANALYSIS_SYSTEM_PROMPT,
        )
        logger.info(f"Log analysis complete. Anomalies found: {result.get('total_anomalies_found', 0)}")
        return result
