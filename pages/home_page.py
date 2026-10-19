"""
Home Page Object for The Internet HeroKuApp Root.

Provides entry points to demo sub-pages (Login, Checkboxes, Add/Remove Elements, etc.).
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config import config
from utils.logger import get_logger

logger = get_logger("HomePage")


class HomePage(BasePage):
    """Page Object for Application Main Landing Page."""

    HEADING = "h1.heading"
    SUBHEADING = "h2"
    FORM_AUTH_LINK = "a[href='/login']"
    CHECKBOXES_LINK = "a[href='/checkboxes']"
    ADD_REMOVE_LINK = "a[href='/add_remove_elements/']"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> "HomePage":
        """Navigate to application root URL."""
        self.navigate(config.base_url)
        return self

    def get_main_heading(self) -> str:
        """Get main h1 title."""
        return self.get_text(self.HEADING)

    def click_form_authentication(self) -> None:
        """Click Form Authentication link."""
        logger.info("Navigating from Home to Form Authentication page.")
        self.click(self.FORM_AUTH_LINK)
