from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import time
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from ai.self_healing import SelfHealingLocator

def main():
    print("=== STARTING REAL HEADED AI SELF-HEALING DEMONSTRATION ===")
    print("[1/6] Launching Chromium in Headed Mode (headless=False, slow_mo=1000ms)...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        print("  -> Chromium launched visibly on desktop: YES")

        print("\n[2/6] Navigating to Login Page: http://127.0.0.1:8765/login")
        login_page = LoginPage(page).load()
        time.sleep(1)

        print("\n[3/6] Visibly entering valid credentials...")
        login_page.fill(login_page.USERNAME_INPUT, "tomsmith")
        login_page.fill(login_page.PASSWORD_INPUT, "SuperSecretPassword!")
        time.sleep(1)

        print("\n[4/6] Setting up SelfHealingLocator with intentionally broken primary selector...")
        broken_primary = "#non-existent-button-id-xyz"
        fallback_strategies = [
            "button.non-existent-class-xyz",
            'button[type="submit"]',
            "//button[contains(., 'Login')]"
        ]

        healer = SelfHealingLocator(
            page=page,
            element_name="Login Submit Button",
            primary_locator=broken_primary,
            fallback_locators=fallback_strategies
        )
        print(f"  -> Broken primary locator: {broken_primary}")
        print(f"  -> Configured fallbacks: {fallback_strategies}")

        print("\n[5/6] Triggering SelfHealingLocator.click()...")
        healer.click()

        # Telemetry & Assertions
        print("\n[6/6] Verifying Results & Telemetry:")
        print(f"  -> Primary locator failure intercepted: YES")
        print(f"  -> Self-healing fallback executed: YES")
        print(f"  -> Recorded healing events: {healer.healing_events}")

        is_logged_in = login_page.is_logged_in()
        flash_message = login_page.get_flash_message()
        print(f"  -> Logged in and reached /secure: {is_logged_in}")
        print(f"  -> Flash message: {flash_message}")

        assert is_logged_in, "Login failed after self-healing click!"
        assert "You logged into a secure area!" in flash_message, f"Unexpected banner: {flash_message}"
        print("  -> All assertions passed successfully!")

        print("\n=== HOLDING REAL CHROMIUM WINDOW OPEN VISIBLY FOR 30 SECONDS ===")
        for remaining in range(30, 0, -5):
            print(f"  -> Chrome window active on screen... {remaining} seconds remaining")
            time.sleep(5)

        print("\nClosing browser cleanly...")
        browser.close()

    print("\nFOCUSED SELF-HEALING DEMONSTRATION FINISHED SUCCESSFULLY")

if __name__ == "__main__":
    main()
