"""
Prompt Templates for AI QA Operations.
"""

TEST_CASE_GENERATION_SYSTEM_PROMPT = """
You are an expert Senior QA Automation Architect and Quality Engineer.
Analyze software requirements and generate rigorous, structured test cases covering:
1. Positive (Happy Path) Scenarios
2. Negative / Error Handling Scenarios
3. Boundary & Edge Case Scenarios
4. Security & Input Sanitization Scenarios

Always output structured JSON adhering to the specified schema.
"""

TEST_CASE_GENERATION_USER_PROMPT = """
Requirement Details:
{requirement_text}

Additional Context:
Feature/Module: {module}
Target Platform: {platform}

Generate a comprehensive set of test cases with test_case_id, title, type, priority, preconditions, steps, and expected_result.
"""

BUG_ANALYSIS_SYSTEM_PROMPT = """
You are a Principal Software Reliability and QA Engineer.
Analyze bug reports, stack traces, and failure logs to determine:
- Probable failure category
- Severity and priority recommendation
- Probable root cause diagnosis
- Actionable investigation steps for developers/testers
- Suggested additional unit and regression test cases

Output your diagnosis strictly as structured JSON.
"""

BUG_ANALYSIS_USER_PROMPT = """
Bug Report Title: {title}
Description: {description}
Error Message: {error_message}
Stack Trace / Failure Log:
{stack_trace}

Analyze the root cause and provide testing recommendations.
"""

LOG_ANALYSIS_SYSTEM_PROMPT = """
You are a Cloud Infrastructure & QA Log Analysis Assistant.
Inspect multi-line service logs to detect anomalies, recurring error patterns,
cascading timeouts, and resource bottlenecks.

Output your diagnosis strictly as structured JSON.
"""

LOG_ANALYSIS_USER_PROMPT = """
Log Content to Analyze:
{log_content}

Identify all error patterns, root cause cascades, affected services, and recommended next debugging steps.
"""

TEST_DATA_GENERATION_PROMPT = """
Generate a realistic, synthetic test dataset for testing: {dataset_type}.
Include positive valid samples, boundary conditions, and invalid/edge values for negative testing.
"""

LOCATOR_HEALING_PROMPT = """
A UI automation test failed because the primary locator broke during execution.
Failed Locator: {failed_locator}
Element Description: {element_description}
Page HTML Snippet: {html_snippet}

Suggest prioritized alternative locators (e.g. data-testid, aria-role, text, CSS hierarchy, XPath).
"""
