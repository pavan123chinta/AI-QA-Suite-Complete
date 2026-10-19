"""
UI Automation Tests using Playwright and Page Object Model (POM).

Tests:
- Home page navigation & header verification
- Successful login flow with positive banner assertion
- Negative login scenarios (invalid username, invalid password, empty credentials)
- Dynamic logout workflow
"""

import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.test_data import TestDataManager


@pytest.mark.ui
@pytest.mark.smoke
class TestNavigationUI:
    """Tests validating basic application navigation and DOM assertions."""

    def test_home_page_load_and_elements(self, page: Page):
        """Verify the landing page loads with correct title and main heading."""
        home_page = HomePage(page).load()

        assert "The Internet" in home_page.get_title()
        assert "Welcome to the-internet" in home_page.get_main_heading()


@pytest.mark.ui
@pytest.mark.regression
class TestAuthenticationUI:
    """Test suite covering authentication flows using Page Object Model."""

    def test_successful_login(self, page: Page, test_data: TestDataManager):
        """Verify user can log in with valid credentials and receive success notification."""
        ui_data = test_data.load_json("ui_data.json")
        creds = ui_data["login"]["valid_user"]

        login_page = LoginPage(page).load()
        login_page.login(creds["username"], creds["password"])

        # Validate success
        assert login_page.is_logged_in(), "Logout button should be visible upon login"
        flash_msg = login_page.get_flash_message()
        assert "You logged into a secure area!" in flash_msg

        # Teardown logout
        login_page.logout()
        assert not login_page.is_logged_in()

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "scenario_key",
        ["invalid_username", "invalid_password", "empty_credentials"],
    )
    def test_negative_login_scenarios(self, page: Page, test_data: TestDataManager, scenario_key: str):
        """Verify login rejection and error messaging for invalid and empty credentials."""
        ui_data = test_data.load_json("ui_data.json")
        creds = ui_data["login"][scenario_key]

        login_page = LoginPage(page).load()
        login_page.login(creds["username"], creds["password"])

        # Verify not logged in
        assert not login_page.is_logged_in(), "User should NOT be logged in with invalid credentials"

        # Verify error flash banner
        flash_msg = login_page.get_flash_message()
        assert (
            "Your username is invalid!" in flash_msg or "Your password is invalid!" in flash_msg
        )
