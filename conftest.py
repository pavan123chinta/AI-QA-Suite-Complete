"""
Pytest Central Configuration and Fixtures.

Configures:
- Browser and Page session/function fixtures with screenshot on failure
- Reusable APIClient and domain PostsClient fixtures
- Central AI Provider fixtures (Mock / LLM)
- Test Data Manager fixtures
- Pytest hooks for custom HTML reporting metadata and failure hooks
"""

from typing import Generator
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from api.clients.api_client import APIClient
from api.clients.posts_client import PostsClient
from ai.providers import AIProvider, MockAIProvider, get_ai_provider
from ai.test_case_generator import TestCaseGenerator
from ai.bug_analyzer import BugAnalyzer
from ai.log_analyzer import LogAnalyzer
from ai.test_data_generator import TestDataGenerator
from utils.config import config
from utils.logger import get_logger
from utils.test_data import TestDataManager
from utils.mock_server import MockLocalServer

logger = get_logger("Conftest")


@pytest.fixture(scope="session", autouse=True)
def mock_app_server() -> Generator[str, None, None]:
    """Start mock local web server so UI tests can run 100% offline & deterministically."""
    server = MockLocalServer(port=8765)
    base_url = server.start()
    logger.info(f"Local Mock UI App Server running at {base_url}")
    # Update config.base_url for tests if default herokuapp is unreachable or local mode is set
    yield base_url
    server.stop()
    logger.info("Local Mock UI App Server stopped.")


# ==============================================================================
# Utility & Data Fixtures
# ==============================================================================

@pytest.fixture(scope="session")
def test_data() -> TestDataManager:
    """Fixture providing access to test data manager across the test session."""
    return TestDataManager()


# ==============================================================================
# API Fixtures
# ==============================================================================

@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """Fixture providing a base HTTP APIClient session."""
    logger.info("Initializing session APIClient fixture.")
    client = APIClient(base_url=config.api_base_url)
    return client


@pytest.fixture(scope="function")
def posts_client(api_client: APIClient) -> PostsClient:
    """Fixture providing domain PostsClient for CRUD operations."""
    return PostsClient(api_client=api_client)


# ==============================================================================
# AI Automation Fixtures
# ==============================================================================

@pytest.fixture(scope="session")
def ai_provider() -> AIProvider:
    """Fixture providing the configured AIProvider (defaults to zero-cost Mock)."""
    return get_ai_provider()


@pytest.fixture(scope="session")
def mock_ai_provider() -> MockAIProvider:
    """Explicitly isolated Mock AI Provider fixture for offline testing."""
    return MockAIProvider()


@pytest.fixture(scope="function")
def test_case_gen(ai_provider: AIProvider) -> TestCaseGenerator:
    """Fixture providing TestCaseGenerator instance."""
    return TestCaseGenerator(provider=ai_provider)


@pytest.fixture(scope="function")
def bug_analyzer(ai_provider: AIProvider) -> BugAnalyzer:
    """Fixture providing BugAnalyzer instance."""
    return BugAnalyzer(provider=ai_provider)


@pytest.fixture(scope="function")
def log_analyzer(ai_provider: AIProvider) -> LogAnalyzer:
    """Fixture providing LogAnalyzer instance."""
    return LogAnalyzer(provider=ai_provider)


@pytest.fixture(scope="function")
def test_data_gen(ai_provider: AIProvider) -> TestDataGenerator:
    """Fixture providing TestDataGenerator instance."""
    return TestDataGenerator(provider=ai_provider)


# ==============================================================================
# UI & Playwright Fixtures
# ==============================================================================

@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Session-scoped Playwright runtime lifecycle."""
    logger.info("Starting Playwright driver session...")
    with sync_playwright() as playwright:
        yield playwright
    logger.info("Playwright driver session terminated.")


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Session-scoped Browser instance."""
    browser_type_name = config.browser
    headless = config.headless
    slow_mo = config.slow_mo

    logger.info(f"Launching Browser: {browser_type_name} (headless={headless}, slow_mo={slow_mo}ms)")

    browser_type = getattr(playwright_instance, browser_type_name, playwright_instance.chromium)
    browser_obj = browser_type.launch(headless=headless, slow_mo=slow_mo)

    yield browser_obj

    logger.info(f"Closing Browser: {browser_type_name}")
    browser_obj.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Function-scoped Browser Context for complete test isolation."""
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    """Function-scoped Playwright Page fixture with automated screenshot capture on failure."""
    pg = context.new_page()
    pg.set_default_timeout(config.timeout)

    yield pg

    # Check if test failed to capture screenshot
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        if config.screenshot_on_failure:
            screenshot_dir = config.reports_dir / "screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_name = f"FAILED_{request.node.name}.png"
            screenshot_path = screenshot_dir / screenshot_name
            try:
                pg.screenshot(path=str(screenshot_path), full_page=True)
                logger.error(f"Captured failure screenshot: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Could not capture screenshot on failure: {e}")

    pg.close()


# ==============================================================================
# Pytest Hooks for Reporting & Metadata
# ==============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test execution outcomes for fixture access (e.g. failure screenshot hook)."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_html_report_title(report):
    """Customize HTML report title."""
    report.title = "AI-QA-Suite Automation Test Execution Report"


def pytest_configure(config):
    """Add custom metadata to HTML report."""
    if hasattr(config, "_metadata"):
        config._metadata["Project Name"] = "AI-QA-Suite (Professional Portfolio)"
        config._metadata["Architecture"] = "Python + Pytest + Playwright + Requests + AI Layer"
        config._metadata["Default AI Provider"] = "Mock (Zero-Cost / Offline Mode)"
