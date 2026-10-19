"""
UI Automation Tests for Checkboxes Page using Playwright and Page Object Model (POM).

Tests:
- Checkboxes page loads correctly with title & heading
- Correct number of checkboxes exists
- Initial checkbox states (first unchecked, second checked)
- Check an unchecked checkbox
- Uncheck a checked checkbox
- Verify toggling behavior and final states
"""

import pytest
from playwright.sync_api import Page
from pages.checkboxes_page import CheckboxesPage


@pytest.mark.ui
@pytest.mark.regression
class TestCheckboxesUI:
    """Test suite for /checkboxes functionality."""

    def test_checkboxes_page_load(self, page: Page):
        """Verify checkboxes page loads properly with header and title."""
        checkboxes_page = CheckboxesPage(page).load()

        assert "Checkboxes" in checkboxes_page.get_title()
        assert "Checkboxes" in checkboxes_page.get_header_text()
        assert checkboxes_page.get_checkbox_count() == 2

    def test_initial_checkbox_states(self, page: Page):
        """Verify default checkbox states upon page load."""
        checkboxes_page = CheckboxesPage(page).load()

        # Checkbox 1 is unchecked by default; Checkbox 2 is checked by default
        assert not checkboxes_page.is_checkbox_checked(0), "Checkbox 1 should initially be unchecked"
        assert checkboxes_page.is_checkbox_checked(1), "Checkbox 2 should initially be checked"

    def test_check_unchecked_checkbox(self, page: Page):
        """Verify that checking an unchecked checkbox changes its state to checked."""
        checkboxes_page = CheckboxesPage(page).load()

        assert not checkboxes_page.is_checkbox_checked(0)
        checkboxes_page.check_checkbox(0)
        assert checkboxes_page.is_checkbox_checked(0), "Checkbox 1 should be checked after check_checkbox"

    def test_uncheck_checked_checkbox(self, page: Page):
        """Verify that unchecking a checked checkbox changes its state to unchecked."""
        checkboxes_page = CheckboxesPage(page).load()

        assert checkboxes_page.is_checkbox_checked(1)
        checkboxes_page.uncheck_checkbox(1)
        assert not checkboxes_page.is_checkbox_checked(1), "Checkbox 2 should be unchecked after uncheck_checkbox"

    def test_toggle_checkboxes_state_flow(self, page: Page):
        """Verify full interaction flow checking one and unchecking the other."""
        checkboxes_page = CheckboxesPage(page).load()

        # Initial states
        assert not checkboxes_page.is_checkbox_checked(0)
        assert checkboxes_page.is_checkbox_checked(1)

        # Toggle both checkboxes
        checkboxes_page.toggle_checkbox(0)
        checkboxes_page.toggle_checkbox(1)

        # Inverted states
        assert checkboxes_page.is_checkbox_checked(0)
        assert not checkboxes_page.is_checkbox_checked(1)

        # Toggle back to original
        checkboxes_page.toggle_checkbox(0)
        checkboxes_page.toggle_checkbox(1)

        assert not checkboxes_page.is_checkbox_checked(0)
        assert checkboxes_page.is_checkbox_checked(1)
