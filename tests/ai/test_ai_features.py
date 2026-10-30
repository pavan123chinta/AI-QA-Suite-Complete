"""
Tests for AI-Assisted QA Capabilities:
1. AI Test Case Generation
2. AI Bug Analysis & Root Cause Diagnosis
3. AI Log Stream Analysis & Anomaly Detection
4. AI Synthetic Test Data Generation
5. Self-Healing Locator Automation

Runs 100% offline and cost-free via MockAIProvider abstraction.
"""

import pytest
from playwright.sync_api import Page
from ai.test_case_generator import TestCaseGenerator
from ai.bug_analyzer import BugAnalyzer
from ai.log_analyzer import LogAnalyzer
from ai.test_data_generator import TestDataGenerator
from ai.self_healing import SelfHealingLocator
from pages.login_page import LoginPage
from utils.test_data import TestDataManager


@pytest.mark.ai
class TestAIFeatures:
    """Automated verification for all AI-augmented QA services."""

    def test_ai_test_case_generation_from_requirement(
        self, test_case_gen: TestCaseGenerator, test_data: TestDataManager
    ):
        """Verify AI test case generation creates structured, prioritized test suites."""
        req_data = test_data.load_json("sample_requirements.json")
        sample_req = req_data["requirements"][0]

        result = test_case_gen.generate_from_requirement(
            requirement_text=sample_req["text"],
            module=sample_req["module"],
        )

        assert "test_cases" in result
        assert len(result["test_cases"]) > 0
        assert "feature" in result

        # Check structure of generated test cases
        first_tc = result["test_cases"][0]
        assert "test_case_id" in first_tc
        assert "title" in first_tc
        assert "type" in first_tc
        assert "priority" in first_tc
        assert "steps" in first_tc
        assert "expected_result" in first_tc
        assert len(first_tc["steps"]) > 0

    def test_ai_bug_analysis(self, bug_analyzer: BugAnalyzer, test_data: TestDataManager):
        """Verify AI bug analyzer extracts root causes and testing suggestions."""
        bug_data = test_data.load_json("sample_requirements.json")["sample_bugs"][0]

        result = bug_analyzer.analyze_bug(
            title=bug_data["title"],
            description=bug_data["description"],
            error_message=bug_data["error_message"],
            stack_trace=bug_data["stack_trace"],
        )

        assert "probable_category" in result
        assert "suggested_severity" in result
        assert "suggested_priority" in result
        assert "probable_root_cause" in result
        assert "investigation_steps" in result
        assert len(result["investigation_steps"]) > 0
        assert "recommended_additional_tests" in result
        assert len(result["recommended_additional_tests"]) > 0

    def test_ai_log_analysis(self, log_analyzer: LogAnalyzer, test_data: TestDataManager):
        """Verify AI log analyzer identifies anomalies and cascading failures."""
        sample_logs = test_data.load_text("sample_logs.txt")

        result = log_analyzer.analyze_logs(sample_logs)

        assert "summary" in result
        assert result["total_anomalies_found"] > 0
        assert "critical_errors" in result
        assert len(result["critical_errors"]) > 0
        assert "probable_root_cause" in result
        assert "suggested_next_debugging_steps" in result

    def test_ai_test_data_generation(self, test_data_gen: TestDataGenerator):
        """Verify synthetic test data generation produces structured records."""
        result = test_data_gen.generate_dataset(dataset_type="User Accounts")

        assert "dataset_name" in result
        assert "records" in result
        assert len(result["records"]) > 0

        # Assert dataset contains both valid and invalid records for boundary testing
        types = [r["type"] for r in result["records"]]
        assert any("valid" in t for t in types)
        assert any("invalid" in t or "boundary" in t for t in types)


@pytest.mark.ai
@pytest.mark.ui
@pytest.mark.self_healing
class TestSelfHealingLocators:
    """Demonstration of Self-Healing Locator recovery during UI automation."""

    def test_self_healing_button_recovery(self, page: Page):
        """
        Verify that when a primary locator is intentionally broken,
        the SelfHealingLocator recovers using fallback selectors and continues the workflow.
        """
        # Load the Login page
        login_page = LoginPage(page).load()

        # Intentionally broken primary selector + working fallbacks
        broken_primary = "#non-existent-button-id-xyz"
        fallback_strategies = [
            "button.non-existent-class",
            "button[type='submit']",  # Valid working selector
            "//button[contains(., 'Login')]",
        ]

        healer = SelfHealingLocator(
            page=page,
            element_name="Login Submit Button",
            primary_locator=broken_primary,
            fallback_locators=fallback_strategies,
        )

        # Enter credentials
        login_page.fill(login_page.USERNAME_INPUT, "tomsmith")
        login_page.fill(login_page.PASSWORD_INPUT, "SuperSecretPassword!")

        # Trigger action through self-healing locator
        healer.click()

        # Verify healing event was recorded
        assert len(healer.healing_events) == 1, "Expected 1 self-healing event"
        event = healer.healing_events[0]
        assert event["status"] == "HEALED"
        assert event["failed_locator"] == broken_primary
        assert event["healed_with"] == "button[type='submit']"

        # Verify UI test succeeded past the healed interaction
        assert login_page.is_logged_in(), "Login should succeed after healed click"

    def test_self_healing_all_fallbacks_fail_triggers_ai_suggestion(self, page: Page):
        """
        Verify that when primary AND all fallback locators fail,
        the AI suggestion path is triggered and helpful recommendations are included in TimeoutError.
        """
        LoginPage(page).load()

        broken_primary = "#completely-non-existent-id-123"
        failing_fallbacks = [
            ".completely-non-existent-class-123",
            "//div[@data-non-existent='true']",
        ]

        healer = SelfHealingLocator(
            page=page,
            element_name="Submit Button",
            primary_locator=broken_primary,
            fallback_locators=failing_fallbacks,
        )

        with pytest.raises(TimeoutError) as exc_info:
            healer.find(timeout=500)

        err_msg = str(exc_info.value)
        assert "Failed to locate 'Submit Button'" in err_msg
        assert "AI Recommendation" in err_msg
        assert len(healer.healing_events) == 0

    def test_self_healing_extracts_runtime_dom_context(self, page: Page):
        """
        Verify that SelfHealingLocator captures sanitized, bounded runtime DOM context
        from the active page rather than a hardcoded static snippet.
        """
        login_page = LoginPage(page).load()
        login_page.fill(login_page.PASSWORD_INPUT, "SuperSecretPassword!")

        healer = SelfHealingLocator(
            page=page,
            element_name="Login Submit Button",
            primary_locator="#broken-button-locator",
        )

        dom_context = healer._extract_bounded_dom_context(max_chars=800)

        assert isinstance(dom_context, str)
        assert len(dom_context) > 0
        assert len(dom_context) <= 850  # Bounded within max_chars + truncation suffix
        assert "<form" in dom_context or "button" in dom_context
        # Ensure sensitive user password attributes are not leaked in DOM context
        assert "SuperSecretPassword!" not in dom_context
        assert "[REDACTED]" in dom_context

    def test_self_healing_dom_context_fallback_when_page_closed(self, page: Page):
        """
        Verify that if the page is closed or inaccessible, DOM extraction degrades
        gracefully to a placeholder without crashing or masking failures.
        """
        LoginPage(page).load()
        page.close()  # Simulate closed / crashed browser page

        healer = SelfHealingLocator(
            page=page,
            element_name="Detached Button",
            primary_locator="#broken-locator",
        )

        dom_context = healer._extract_bounded_dom_context()
        assert "unavailable" in dom_context or "failed" in dom_context

        # Requesting AI suggestion with closed page should still safely return AI suggestions
        ai_suggestion = healer.request_ai_locator_suggestion()
        assert "suggested_locators" in ai_suggestion
