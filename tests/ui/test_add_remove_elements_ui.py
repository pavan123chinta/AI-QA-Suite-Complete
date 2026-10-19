"""
UI Automation Tests for Add/Remove Elements Page using Playwright and Page Object Model (POM).

Tests:
- Add/Remove Elements page loads correctly with header & Add button
- Add Element creates an element dynamically
- Multiple elements can be added
- Delete button removes an element
- Verify element count and state transitions
"""

import pytest
from playwright.sync_api import Page
from pages.add_remove_elements_page import AddRemoveElementsPage


@pytest.mark.ui
@pytest.mark.regression
class TestAddRemoveElementsUI:
    """Test suite for /add_remove_elements/ functionality."""

    def test_page_load_and_elements(self, page: Page):
        """Verify the page loads correctly with heading, Add button, and zero initial elements."""
        add_remove_page = AddRemoveElementsPage(page).load()

        assert "Add/Remove Elements" in add_remove_page.get_title()
        assert "Add/Remove Elements" in add_remove_page.get_header_text()
        assert add_remove_page.is_add_element_button_visible(), "'Add Element' button should be visible"
        assert add_remove_page.get_delete_button_count() == 0, "Initial delete button count should be 0"

    def test_add_single_element(self, page: Page):
        """Verify that clicking 'Add Element' creates exactly one Delete button."""
        add_remove_page = AddRemoveElementsPage(page).load()

        assert add_remove_page.get_delete_button_count() == 0
        add_remove_page.click_add_element(count=1)
        assert add_remove_page.get_delete_button_count() == 1, "Exactly one Delete button should be visible"

    def test_add_multiple_elements(self, page: Page):
        """Verify adding multiple elements creates the corresponding number of Delete buttons."""
        add_remove_page = AddRemoveElementsPage(page).load()

        target_count = 5
        add_remove_page.click_add_element(count=target_count)
        assert add_remove_page.get_delete_button_count() == target_count, f"Expected {target_count} Delete buttons"

    def test_delete_element_removes_it(self, page: Page):
        """Verify clicking a Delete button removes that element from the DOM."""
        add_remove_page = AddRemoveElementsPage(page).load()

        # Add 3 elements
        add_remove_page.click_add_element(count=3)
        assert add_remove_page.get_delete_button_count() == 3

        # Delete one element
        add_remove_page.click_delete_button(0)
        assert add_remove_page.get_delete_button_count() == 2, "Expected 2 remaining Delete buttons"

        # Delete another element
        add_remove_page.click_delete_button(0)
        assert add_remove_page.get_delete_button_count() == 1, "Expected 1 remaining Delete button"

    def test_delete_all_elements(self, page: Page):
        """Verify adding multiple elements and deleting all of them leaves zero elements."""
        add_remove_page = AddRemoveElementsPage(page).load()

        add_remove_page.click_add_element(count=4)
        assert add_remove_page.get_delete_button_count() == 4

        add_remove_page.delete_all_elements()
        assert add_remove_page.get_delete_button_count() == 0, "All Delete buttons should have been removed"
