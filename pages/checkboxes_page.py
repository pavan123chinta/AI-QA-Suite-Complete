"""
Checkboxes Page Object for The Internet HeroKuApp /checkboxes.

Encapsulates locators, navigation, checking/unchecking, and state verifications.
"""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from utils.config import config
from utils.logger import get_logger

logger = get_logger("CheckboxesPage")


class CheckboxesPage(BasePage):
    """Page Object for the Checkboxes page."""

    URL_PATH = "/checkboxes"

    # Locators
    PAGE_HEADER = "h3.heading"
    CHECKBOXES_FORM = "#checkboxes"
    CHECKBOXES = "#checkboxes input[type='checkbox']"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> "CheckboxesPage":
        """Navigate directly to the Checkboxes page."""
        target_url = f"{config.base_url.rstrip('/')}{self.URL_PATH}"
        self.navigate(target_url)
        return self

    def get_header_text(self) -> str:
        """Get the page heading text."""
        return self.get_text(self.PAGE_HEADER)

    def get_checkboxes_locator(self) -> Locator:
        """Get Locator for all checkbox inputs."""
        return self.find_element(self.CHECKBOXES)

    def get_checkbox_count(self) -> int:
        """Return total number of checkboxes found on the page."""
        return self.get_checkboxes_locator().count()

    def is_checkbox_checked(self, index: int) -> bool:
        """
        Check if the checkbox at 0-based index is checked.

        :param index: 0-based index of the checkbox
        :return: True if checked, False otherwise
        """
        return self.get_checkboxes_locator().nth(index).is_checked()

    def check_checkbox(self, index: int) -> None:
        """
        Ensure the checkbox at 0-based index is checked.

        :param index: 0-based index of the checkbox
        """
        logger.info(f"Checking checkbox at index {index}")
        self.get_checkboxes_locator().nth(index).check()

    def uncheck_checkbox(self, index: int) -> None:
        """
        Ensure the checkbox at 0-based index is unchecked.

        :param index: 0-based index of the checkbox
        """
        logger.info(f"Unchecking checkbox at index {index}")
        self.get_checkboxes_locator().nth(index).uncheck()

    def toggle_checkbox(self, index: int) -> None:
        """
        Toggle the checkbox at 0-based index by clicking it.

        :param index: 0-based index of the checkbox
        """
        logger.info(f"Clicking checkbox at index {index}")
        self.get_checkboxes_locator().nth(index).click()
