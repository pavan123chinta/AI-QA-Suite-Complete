"""
End-to-End AI QA Workflow Integration Test.

Demonstrates the full AI-augmented QA lifecycle:
1. Requirement Ingestion
2. AI Test Case Generation
3. Automated API & UI Test Execution
4. Simulated Failure Capture
5. AI Log & Bug Root Cause Analysis
6. Final QA Assessment Report
"""

import pytest
from playwright.sync_api import Page
from ai.test_case_generator import TestCaseGenerator
from ai.bug_analyzer import BugAnalyzer
from ai.log_analyzer import LogAnalyzer
from pages.login_page import LoginPage
from api.clients.posts_client import PostsClient
from utils.test_data import TestDataManager
from utils.logger import get_logger

logger = get_logger("AIQAWorkflowIntegration")


@pytest.mark.ai
@pytest.mark.regression
class TestAIQAWorkflowIntegration:
    """End-to-end integration of requirement -> AI test cases -> execution -> AI failure triage."""

    def test_complete_ai_qa_lifecycle(
        self,
        page: Page,
        posts_client: PostsClient,
        test_case_gen: TestCaseGenerator,
        bug_analyzer: BugAnalyzer,
        log_analyzer: LogAnalyzer,
        test_data: TestDataManager,
    ):
        logger.info("=== STEP 1: Ingest Requirement & Generate AI Test Cases ===")
        reqs = test_data.load_json("sample_requirements.json")["requirements"]
        auth_req = reqs[0]

        generated_suite = test_case_gen.generate_from_requirement(
            requirement_text=auth_req["text"], module=auth_req["module"]
        )
        assert len(generated_suite["test_cases"]) >= 2
        logger.info(f"Generated {len(generated_suite['test_cases'])} test cases from requirement.")

        logger.info("=== STEP 2: Execute Automated API Validation ===")
        api_res = posts_client.get_post_by_id(1)
        assert api_res.status_code == 200

        logger.info("=== STEP 3: Execute Automated UI Validation via POM ===")
        ui_creds = test_data.load_json("ui_data.json")["login"]["valid_user"]
        login_page = LoginPage(page).load()
        login_page.login(ui_creds["username"], ui_creds["password"])
        assert login_page.is_logged_in()

        logger.info("=== STEP 4: Ingest Simulated Failure Logs into AI Log Analyzer ===")
        raw_logs = test_data.load_text("sample_logs.txt")
        log_diagnosis = log_analyzer.analyze_logs(raw_logs)
        assert log_diagnosis["total_anomalies_found"] > 0
        logger.info(f"AI Root Cause Summary: {log_diagnosis['probable_root_cause']}")

        logger.info("=== STEP 5: Triage Defect using AI Bug Analyzer ===")
        sample_bug = test_data.load_json("sample_requirements.json")["sample_bugs"][0]
        bug_diagnosis = bug_analyzer.analyze_bug(
            title=sample_bug["title"],
            description=sample_bug["description"],
            error_message=sample_bug["error_message"],
            stack_trace=sample_bug["stack_trace"],
        )
        assert bug_diagnosis["suggested_priority"] in ("P1 - Urgent", "P1", "High")
        logger.info(f"AI Bug Severity: {bug_diagnosis['suggested_severity']}, Category: {bug_diagnosis['probable_category']}")
