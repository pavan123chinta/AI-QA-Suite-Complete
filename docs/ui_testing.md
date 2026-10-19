# UI Automation & Page Object Model Guide

## Overview
The UI automation layer uses **Playwright for Python** structured through the **Page Object Model (POM)** design pattern.

## Page Classes
- **`BasePage` (`pages/base_page.py`)**: Provides common browser actions:
  - `navigate(url)`
  - `find_element(selector)`
  - `click(selector)`
  - `fill(selector, text)` (with password masking in logs)
  - `wait_for_selector(selector, state)`
  - `take_screenshot(filename)`
- **`LoginPage` (`pages/login_page.py`)**: Encapsulates login forms, credential submission, banner message extraction, and logout.
- **`HomePage` (`pages/home_page.py`)**: Manages navigation on application entry points.

## Resilient Execution & Failure Capture
1. **Context Isolation**: Each test runs in an independent `BrowserContext`, preventing state leaks across tests.
2. **Automatic Screenshot on Failure**: Configured via Pytest hooks in `conftest.py`—when any UI assertion fails, a full-page PNG screenshot is automatically saved to `reports/screenshots/`.
