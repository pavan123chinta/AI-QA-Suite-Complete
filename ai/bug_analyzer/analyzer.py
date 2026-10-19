"""
AI-Assisted Bug Analyzer.

Analyzes defect descriptions, runtime errors, and stack traces to provide root cause analysis and QA triage.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from ai.providers import AIProvider, get_ai_provider
from ai.prompts import BUG_ANALYSIS_SYSTEM_PROMPT, BUG_ANALYSIS_USER_PROMPT
from utils.logger import get_logger

logger = get_logger("BugAnalyzer")


class BugAnalysisResult(BaseModel):
    """Structured output for bug analysis."""
    probable_category: str
    suggested_severity: str
    suggested_priority: str
    probable_root_cause: str
    investigation_steps: List[str]
    recommended_additional_tests: List[str]
    disclaimer: str = "AI-assisted suggestion. Requires human confirmation."


class BugAnalyzer:
    """Service to diagnose defect logs, stack traces, and test failures."""

    def __init__(self, provider: Optional[AIProvider] = None):
        self.provider = provider or get_ai_provider()

    def analyze_bug(
        self,
        title: str,
        description: str,
        error_message: str = "",
        stack_trace: str = "",
    ) -> Dict[str, Any]:
        """
        Perform automated defect root cause analysis.

        :param title: Defect summary
        :param description: Defect description
        :param error_message: Exact error string
        :param stack_trace: Stack trace dump
        :return: Structured analysis result
        """
        logger.info(f"Analyzing defect: '{title}'...")
        prompt = BUG_ANALYSIS_USER_PROMPT.format(
            title=title,
            description=description,
            error_message=error_message,
            stack_trace=stack_trace,
        )
        schema_desc = """
        {
            "probable_category": "string",
            "suggested_severity": "Critical|High|Medium|Low",
            "suggested_priority": "P1|P2|P3|P4",
            "probable_root_cause": "string",
            "investigation_steps": ["string"],
            "recommended_additional_tests": ["string"],
            "disclaimer": "string"
        }
        """
        result = self.provider.generate_structured_json(
            prompt=prompt,
            schema_description=schema_desc,
            system_message=BUG_ANALYSIS_SYSTEM_PROMPT,
        )
        logger.info(f"Bug analysis completed. Category: {result.get('probable_category')}")
        return result
