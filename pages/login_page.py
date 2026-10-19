"""
Login Page Object for The Internet HeroKuApp /login.

Encapsulates locators, authentication flows, error verifications, and success banners.
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config import config
from utils.logger import get_logger

logger = get_logger("LoginPage")


class LoginPage(BasePage):
    """Page Object for the Form Authentication login page."""

    URL_PATH = "/login"

    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    FLASH_MESSAGE = "#flash"
    LOGOUT_BUTTON = "a[href='/logout']"
    PAGE_HEADER = "h2"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> "LoginPage":
        """Navigate directly to the Login page."""
        target_url = f"{config.base_url.rstrip('/')}{self.URL_PATH}"
        self.navigate(target_url)
        return self

    def login(self, username: str, password: str) -> None:
        """
        Perform standard login actions.

        :param username: Username text
        :param password: Password text
        """
        logger.info(f"Submitting credentials for user: '{username}'")
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_flash_message(self) -> str:
        """Retrieve flash notification banner message."""
        self.wait_for_selector(self.FLASH_MESSAGE, state="visible")
        message = self.get_text(self.FLASH_MESSAGE)
        # Strip trailing '×' close button icon text
        return message.replace("×", "").strip()

    def is_logged_in(self) -> bool:
        """Check if Logout button is visible, indicating authenticated state."""
        return self.is_visible(self.LOGOUT_BUTTON)

    def logout(self) -> None:
        """Perform logout action if authenticated."""
        if self.is_logged_in():
            logger.info("Clicking logout button.")
            self.click(self.LOGOUT_BUTTON)
