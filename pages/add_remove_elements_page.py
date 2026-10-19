"""
Add/Remove Elements Page Object for The Internet HeroKuApp /add_remove_elements/.

Encapsulates locators, adding elements, deleting elements, and element count assertions.
"""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from utils.config import config
from utils.logger import get_logger

logger = get_logger("AddRemoveElementsPage")


class AddRemoveElementsPage(BasePage):
    """Page Object for the Add/Remove Elements page."""

    URL_PATH = "/add_remove_elements/"

    # Locators
    PAGE_HEADER = "h3.heading"
    ADD_ELEMENT_BUTTON = "button[onclick='addElement()']"
    DELETE_BUTTONS = "#elements button.added-manually"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> "AddRemoveElementsPage":
        """Navigate directly to the Add/Remove Elements page."""
        target_url = f"{config.base_url.rstrip('/')}{self.URL_PATH}"
        self.navigate(target_url)
        return self

    def get_header_text(self) -> str:
        """Get page heading text."""
        return self.get_text(self.PAGE_HEADER)

    def is_add_element_button_visible(self) -> bool:
        """Check if 'Add Element' button is visible."""
        return self.is_visible(self.ADD_ELEMENT_BUTTON)

    def click_add_element(self, count: int = 1) -> None:
        """
        Click the 'Add Element' button one or more times.

        :param count: Number of times to click the button (default 1)
        """
        for i in range(count):
            logger.info(f"Clicking Add Element button (iteration {i + 1}/{count})")
            self.click(self.ADD_ELEMENT_BUTTON)

    def get_delete_buttons_locator(self) -> Locator:
        """Get Locator for all Delete buttons created dynamically."""
        return self.find_element(self.DELETE_BUTTONS)

    def get_delete_button_count(self) -> int:
        """Return count of currently visible Delete buttons."""
        return self.get_delete_buttons_locator().count()

    def click_delete_button(self, index: int = 0) -> None:
        """
        Click the Delete button at the specified 0-based index.

        :param index: Index of the Delete button to click (default 0)
        """
        logger.info(f"Clicking Delete button at index {index}")
        self.get_delete_buttons_locator().nth(index).click()

    def delete_all_elements(self) -> None:
        """Repeatedly click Delete buttons until none remain."""
        logger.info("Deleting all elements on page.")
        while self.get_delete_button_count() > 0:
            self.click_delete_button(0)
