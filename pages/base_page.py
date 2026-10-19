"""
Base Page Object for Playwright UI Automation.

Encapsulates common page interactions, explicit waits, screenshots, and navigation helpers.
"""

from typing import Optional
from pathlib import Path
from playwright.sync_api import Page, Locator

from utils.config import config
from utils.logger import get_logger

logger = get_logger("BasePage")


class BasePage:
    """Foundational Page Object with resilient UI interaction methods."""

    def __init__(self, page: Page):
        """
        Initialize BasePage with Playwright page fixture.

        :param page: Playwright Page instance
        """
        self.page = page
        self.timeout = config.timeout

    def navigate(self, url: str) -> None:
        """Navigate to specified URL."""
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")

    def get_title(self) -> str:
        """Get active page title."""
        title = self.page.title()
        logger.debug(f"Page title retrieved: '{title}'")
        return title

    def get_url(self) -> str:
        """Get current URL."""
        return self.page.url

    def find_element(self, selector: str) -> Locator:
        """Return a Playwright Locator for given selector."""
        return self.page.locator(selector)

    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Wait for element and click."""
        t = timeout or self.timeout
        logger.debug(f"Clicking on selector: {selector}")
        self.page.locator(selector).click(timeout=t)

    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """Wait for input and fill text."""
        t = timeout or self.timeout
        # Mask text if field is a password
        logged_val = "********" if "password" in selector.lower() else text
        logger.debug(f"Filling selector '{selector}' with: '{logged_val}'")
        self.page.locator(selector).fill(text, timeout=t)

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Get inner text of element."""
        t = timeout or self.timeout
        text = self.page.locator(selector).inner_text(timeout=t)
        logger.debug(f"Selector '{selector}' inner text: '{text}'")
        return text

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Check if element is visible on page."""
        t = timeout or 3000
        try:
            return self.page.locator(selector).is_visible(timeout=t)
        except Exception:
            return False

    def wait_for_selector(self, selector: str, state: str = "visible", timeout: Optional[int] = None) -> Locator:
        """Explicitly wait for element state ('attached', 'detached', 'visible', 'hidden')."""
        t = timeout or self.timeout
        logger.debug(f"Waiting for selector '{selector}' to be {state}")
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=t)
        return locator

    def take_screenshot(self, file_name: str) -> Path:
        """
        Capture page screenshot and save under reports/screenshots.

        :param file_name: Screenshot image file name
        :return: Path to saved screenshot
        """
        screenshot_dir = config.reports_dir / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        target_path = screenshot_dir / file_name
        self.page.screenshot(path=str(target_path), full_page=True)
        logger.info(f"Screenshot saved to: {target_path}")
        return target_path
