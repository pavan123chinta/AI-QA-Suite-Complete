"""
Local / Mock AI Provider Implementation.

Provides 100% offline, zero-cost, deterministic intelligence for QA workflows:
- Test Case Generation (Positive, Negative, Boundary, Edge cases)
- Bug Analysis & Root Cause Diagnosis
- Log File Analysis & Anomaly Detection
- Synthetic Test Data Generation
- Self-Healing Locator Suggestions

Zero API keys or external network calls required.
"""

from typing import Any, Dict, Optional

from ai.providers.ai_provider import AIProvider
from utils.logger import get_logger

logger = get_logger("MockAIProvider")


class MockAIProvider(AIProvider):
    """
    Intelligent Rule-Based Mock AI Provider.
    Parses prompts dynamically to synthesize realistic, structured responses for QA tasks.
    """

    def __init__(self):
        logger.debug("MockAIProvider initialized (Offline & Zero-Cost Mode).")

    def generate_text(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Simulate free-form AI text synthesis."""
        prompt_lower = prompt.lower()
        if "test case" in prompt_lower:
            return "Generated Test Suite:\n1. Positive Path Verification\n2. Invalid Input Validation\n3. Security & Boundary Check"
        elif "bug" in prompt_lower or "error" in prompt_lower:
            return "Bug Analysis Summary: Detected potential null pointer / timeout exception in upstream service."
        elif "log" in prompt_lower:
            return "Log Analysis: Found 2 critical errors related to upstream timeout and connection pool exhaustion."
        return f"[MockAI Provider Response for prompt: '{prompt[:60]}...']"

    def generate_structured_json(
        self, prompt: str, schema_description: Optional[str] = None, system_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Synthesize structured JSON matching the specific QA intent."""
        full_context = f"{system_message or ''} {schema_description or ''} {prompt}".lower()

        # 1. Log Analysis Intent
        if "log content" in full_context or "log analysis" in full_context or "anomalies_found" in full_context or "service logs" in full_context:
            return self._synthesize_log_analysis(prompt)

        # 2. Bug Analysis Intent (check bug report, stack trace, root cause, error_message, defect)
        elif "bug report" in full_context or "stack trace" in full_context or "root cause" in full_context or "error message" in full_context or "probable_category" in full_context:
            return self._synthesize_bug_analysis(prompt)

        # 3. Test Case Generation Intent
        elif "test case" in full_context or "requirement" in full_context:
            return self._synthesize_test_cases(prompt)

        # 4. Test Data Generation Intent
        elif "test data" in full_context or "synthetic" in full_context or "dataset" in full_context:
            return self._synthesize_test_data(prompt)

        # 5. Self-Healing Locator Suggestion Intent
        elif "locator" in full_context or "selector" in full_context or "healing" in full_context:
            return self._synthesize_locator_healing(prompt)

        # Default fallback structure
        return {
            "status": "success",
            "provider": "MockAIProvider",
            "analysis": f"Evaluated prompt of length {len(prompt)} characters.",
            "recommendations": ["Proceed with standardized QA validation pipeline."],
        }

    def _synthesize_test_cases(self, prompt: str) -> Dict[str, Any]:
        """Generate positive, negative, and edge test scenarios."""
        # Extract keywords to contextualize
        is_login = "log in" in prompt.lower() or "login" in prompt.lower() or "auth" in prompt.lower()
        is_payment = "payment" in prompt.lower() or "card" in prompt.lower() or "checkout" in prompt.lower()

        if is_login:
            feature = "Authentication"
            scenarios = [
                {
                    "test_case_id": "TC-AUTH-001",
                    "title": "Verify successful login with valid credentials",
                    "type": "Positive",
                    "priority": "High",
                    "preconditions": "User account exists and is active",
                    "steps": [
                        "Navigate to login page",
                        "Enter valid username and valid password",
                        "Click submit button",
                    ],
                    "expected_result": "User is redirected to secure dashboard with welcome banner.",
                },
                {
                    "test_case_id": "TC-AUTH-002",
                    "title": "Verify login rejection with invalid password",
                    "type": "Negative",
                    "priority": "High",
                    "preconditions": "User account exists",
                    "steps": [
                        "Navigate to login page",
                        "Enter valid username and wrong password",
                        "Click submit button",
                    ],
                    "expected_result": "Error notification 'Your password is invalid!' is displayed.",
                },
                {
                    "test_case_id": "TC-AUTH-003",
                    "title": "Verify login validation on empty credentials submission",
                    "type": "Boundary",
                    "priority": "Medium",
                    "preconditions": "Login page loaded",
                    "steps": [
                        "Leave username and password empty",
                        "Click submit button",
                    ],
                    "expected_result": "Validation error shown; request is blocked.",
                },
                {
                    "test_case_id": "TC-AUTH-004",
                    "title": "Verify SQL injection sanitization on username field",
                    "type": "Security / Edge",
                    "priority": "High",
                    "preconditions": "Login page loaded",
                    "steps": [
                        "Enter payload ' OR 1=1; -- into username",
                        "Enter arbitrary password",
                        "Click submit button",
                    ],
                    "expected_result": "Input is sanitized; login rejected with 401/error banner without DB error leak.",
                },
            ]
        elif is_payment:
            feature = "Payment Gateway"
            scenarios = [
                {
                    "test_case_id": "TC-PAY-001",
                    "title": "Verify successful payment transaction with valid VISA card",
                    "type": "Positive",
                    "priority": "High",
                    "preconditions": "Cart has items with valid total",
                    "steps": [
                        "Enter valid VISA card number, expiration, and CVV",
                        "Click 'Process Payment'",
                    ],
                    "expected_result": "Payment authorized; 200 OK returned with confirmation order ID.",
                },
                {
                    "test_case_id": "TC-PAY-002",
                    "title": "Verify 2FA challenge trigger for transactions > $10,000",
                    "type": "Boundary",
                    "priority": "High",
                    "preconditions": "Transaction amount is $10,000.01",
                    "steps": [
                        "Submit high-value checkout",
                    ],
                    "expected_result": "Two-factor authentication challenge prompt triggered.",
                },
                {
                    "test_case_id": "TC-PAY-003",
                    "title": "Verify rejection on zero or negative payment amount",
                    "type": "Negative",
                    "priority": "High",
                    "preconditions": "Cart total set to $0.00 or -$5.00",
                    "steps": [
                        "Attempt payment processing",
                    ],
                    "expected_result": "HTTP 400 Bad Request returned; transaction rejected.",
                },
            ]
        else:
            feature = "General Feature"
            scenarios = [
                {
                    "test_case_id": "TC-GEN-001",
                    "title": "Verify standard happy-path workflow",
                    "type": "Positive",
                    "priority": "High",
                    "preconditions": "System in steady state",
                    "steps": ["Trigger main operation with valid input parameters"],
                    "expected_result": "Operation completes successfully.",
                },
                {
                    "test_case_id": "TC-GEN-002",
                    "title": "Verify error handling on invalid parameter values",
                    "type": "Negative",
                    "priority": "Medium",
                    "preconditions": "System loaded",
                    "steps": ["Submit payload with malformed or missing required keys"],
                    "expected_result": "Helpful validation error returned without system crash.",
                },
            ]

        return {
            "feature": feature,
            "total_test_cases": len(scenarios),
            "generated_by": "MockAIProvider (Local / Zero-Cost)",
            "test_cases": scenarios,
        }

    def _synthesize_bug_analysis(self, prompt: str) -> Dict[str, Any]:
        """Analyze bug details and provide root cause diagnosis."""
        prompt_lower = prompt.lower()

        if "nullpointer" in prompt_lower or "null" in prompt_lower:
            category = "Backend Logic / Unhandled Null Reference"
            severity = "High"
            priority = "P1 - Urgent"
            root_cause = "Missing null/empty defensive check before dereferencing parameter."
            investigation = [
                "Inspect CouponValidator.java line 42 for missing null check on couponCode.",
                "Verify API gateway input sanitization filters for null vs empty string values.",
            ]
            suggested_tests = [
                "Unit test CouponValidator with null, empty string, and whitespace arguments.",
                "API regression test for checkout endpoint with omitted 'couponCode' key.",
            ]
        elif "timeout" in prompt_lower or "timeoutexception" in prompt_lower or "504" in prompt_lower:
            category = "Integration / Latency / Upstream Dependency"
            severity = "Critical"
            priority = "P1 - Urgent"
            root_cause = "Upstream bank partner processor failed to respond within 5000ms threshold."
            investigation = [
                "Check network latency and circuit breaker status on BankClient connector.",
                "Inspect downstream partner status page and timeout thresholds.",
            ]
            suggested_tests = [
                "Mock upstream latency to verify graceful fallback / circuit breaker activation.",
                "Retry policy test with exponential backoff.",
            ]
        elif "locator" in prompt_lower or "playwright" in prompt_lower or "button" in prompt_lower:
            category = "UI Automation / DOM Selector Drift"
            severity = "Low"
            priority = "P3 - Maintenance"
            root_cause = "Element ID/Class changed during frontend styling refactoring without updating test selector."
            investigation = [
                "Compare latest HTML DOM template with Page Object Model selector definitions.",
                "Leverage resilient data-testid attributes instead of dynamic IDs.",
            ]
            suggested_tests = [
                "Execute Self-Healing locator fallback chain.",
                "Validate UI flow with updated data-testid selector.",
            ]
        else:
            category = "General Defect"
            severity = "Medium"
            priority = "P2 - Standard"
            root_cause = "Unexpected behavior observed during automated validation."
            investigation = ["Review application log traces and network payloads."]
            suggested_tests = ["Add boundary and regression test cases."]

        return {
            "analysis_status": "Completed",
            "provider": "MockAIProvider",
            "probable_category": category,
            "suggested_severity": severity,
            "suggested_priority": priority,
            "probable_root_cause": root_cause,
            "investigation_steps": investigation,
            "recommended_additional_tests": suggested_tests,
            "disclaimer": "AI-assisted suggestion. Requires human QA confirmation.",
        }

    def _synthesize_log_analysis(self, prompt: str) -> Dict[str, Any]:
        """Analyze log text to extract error patterns, anomalies, and next debugging steps."""
        prompt_lower = prompt.lower()

        detected_errors = []
        if "paymentgatewaytimeoutexception" in prompt_lower or "timeout" in prompt_lower:
            detected_errors.append({
                "service": "PaymentGateway / OrderService",
                "level": "ERROR",
                "type": "PaymentGatewayTimeoutException",
                "frequency": "High",
                "impact": "Failed checkout transactions for end users",
            })
        if "connection pool exhausted" in prompt_lower or "databasepool" in prompt_lower:
            detected_errors.append({
                "service": "DatabasePool / UserService",
                "level": "ERROR",
                "type": "ConnectionPoolExhaustion",
                "frequency": "Critical",
                "impact": "Queries blocked waiting for available DB connections",
            })

        if not detected_errors:
            detected_errors.append({
                "service": "ApplicationCore",
                "level": "WARN/ERROR",
                "type": "GenericAnomaly",
                "frequency": "Low",
                "impact": "Unclassified log warnings detected",
            })

        return {
            "summary": f"Analyzed log snippet. Identified {len(detected_errors)} distinct critical failure patterns.",
            "total_anomalies_found": len(detected_errors),
            "critical_errors": detected_errors,
            "probable_root_cause": "Cascading failure: Upstream payment processor latency caused request queue buildup, exhausting database connection pool.",
            "affected_components": [e["service"] for e in detected_errors],
            "suggested_next_debugging_steps": [
                "Increase or tune DB connection pool maximum capacity and idle timeout.",
                "Introduce circuit breaker pattern with short timeout on external PaymentGateway client.",
                "Inspect database slow query logs for long-running unindexed queries holding connections.",
            ],
        }

    def _synthesize_test_data(self, prompt: str) -> Dict[str, Any]:
        """Synthesize synthetic test dataset with valid, boundary, and edge records."""
        return {
            "dataset_name": "Synthetic_User_Accounts",
            "total_records": 4,
            "records": [
                {
                    "type": "valid_standard",
                    "username": "qa_valid_sarah",
                    "email": "sarah.qa@example.com",
                    "age": 28,
                    "role": "STANDARD_USER",
                    "status": "ACTIVE",
                },
                {
                    "type": "valid_admin",
                    "username": "qa_admin_marcus",
                    "email": "marcus.admin@example.com",
                    "age": 42,
                    "role": "SYSTEM_ADMIN",
                    "status": "ACTIVE",
                },
                {
                    "type": "boundary_minimum_age",
                    "username": "qa_boundary_18",
                    "email": "teen.user18@example.com",
                    "age": 18,
                    "role": "STANDARD_USER",
                    "status": "ACTIVE",
                },
                {
                    "type": "invalid_format",
                    "username": "invalid@@user##",
                    "email": "not-an-email-format",
                    "age": -5,
                    "role": "UNKNOWN",
                    "status": "INVALID_REJECT",
                },
            ],
        }

    def _synthesize_locator_healing(self, prompt: str) -> Dict[str, Any]:
        """Suggest alternative resilient locators given a failed primary selector."""
        return {
            "healing_strategy": "Multi-Strategy Fallback & Semantic Matching",
            "confidence_score": 0.94,
            "suggested_locators": [
                {"strategy": "DataTestId", "locator": "[data-testid='login-submit-btn']", "rank": 1},
                {"strategy": "AriaRole", "locator": "button:has-text('Login')", "rank": 2},
                {"strategy": "FormSubmit", "locator": "form#login button[type='submit']", "rank": 3},
                {"strategy": "XPathText", "locator": "//button[contains(normalize-space(.), 'Login')]", "rank": 4},
            ],
            "explanation": "Primary CSS ID changed or dynamic. Fallback to accessibility roles and data-testid recommended.",
        }
