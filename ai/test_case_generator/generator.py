"""
AI-Assisted Test Case Generator.

Takes user stories or requirement texts and produces structured, prioritized test suites.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ai.providers import AIProvider, get_ai_provider
from ai.prompts import TEST_CASE_GENERATION_SYSTEM_PROMPT, TEST_CASE_GENERATION_USER_PROMPT
from utils.logger import get_logger

logger = get_logger("TestCaseGenerator")


class TestCase(BaseModel):
    """Data model representing a single structured test case."""
    test_case_id: str = Field(..., description="Unique test case ID e.g. TC-AUTH-001")
    title: str = Field(..., description="Concise test scenario summary")
    type: str = Field(..., description="Positive / Negative / Boundary / Security / Edge")
    priority: str = Field(..., description="High / Medium / Low")
    preconditions: str = Field(..., description="Initial state required")
    steps: List[str] = Field(..., description="Ordered action steps")
    expected_result: str = Field(..., description="Expected outcome / assertion")


class GeneratedTestSuite(BaseModel):
    """Collection of generated test cases for a feature."""
    feature: str
    total_test_cases: int
    generated_by: str
    test_cases: List[TestCase]


class TestCaseGenerator:
    """Service to generate test suites from requirements using AI abstraction."""

    def __init__(self, provider: Optional[AIProvider] = None):
        self.provider = provider or get_ai_provider()

    def generate_from_requirement(
        self, requirement_text: str, module: str = "General", platform: str = "Web/API"
    ) -> Dict[str, Any]:
        """
        Generate structured test cases for a given requirement.

        :param requirement_text: Requirement description or acceptance criteria
        :param module: Feature module name
        :param platform: Target platform
        :return: Structured dictionary of test cases
        """
        logger.info(f"Generating AI test cases for module '{module}'...")
        prompt = TEST_CASE_GENERATION_USER_PROMPT.format(
            requirement_text=requirement_text, module=module, platform=platform
        )
        schema_desc = """
        {
            "feature": "string",
            "total_test_cases": int,
            "generated_by": "string",
            "test_cases": [
                {
                    "test_case_id": "string",
                    "title": "string",
                    "type": "string",
                    "priority": "string",
                    "preconditions": "string",
                    "steps": ["string"],
                    "expected_result": "string"
                }
            ]
        }
        """
        result = self.provider.generate_structured_json(
            prompt=prompt,
            schema_description=schema_desc,
            system_message=TEST_CASE_GENERATION_SYSTEM_PROMPT,
        )
        logger.info(f"Generated {result.get('total_test_cases', len(result.get('test_cases', [])))} test cases.")
        return result
