"""
Self-Healing Locator Demonstration & Strategy Handler.

Demonstrates resilient UI automation:
1. Primary locator attempt.
2. Interception of failure.
3. Ordered fallback strategy execution (ID -> data-testid -> Text/Role -> XPath).
4. AI-assisted locator suggestions for healing logs.
5. Clear healing event logging & telemetry.

NOTE: This is a robust deterministic multi-strategy fallback mechanism
coupled with AI locator suggestion triage. It does NOT make false claims of
autonomous AI production healing without human oversight.
"""

from typing import Any, Dict, List, Optional
from playwright.sync_api import Locator, Page

from ai.providers import AIProvider, get_ai_provider
from ai.prompts import LOCATOR_HEALING_PROMPT
from utils.logger import get_logger

logger = get_logger("SelfHealingLocator")


class SelfHealingLocator:
    """
    Resilient Locator wrapper that recovers from DOM mutations via fallback chains and AI suggestions.
    """

    def __init__(
        self,
        page: Page,
        element_name: str,
        primary_locator: str,
        fallback_locators: Optional[List[str]] = None,
        ai_provider: Optional[AIProvider] = None,
    ):
        """
        Initialize SelfHealingLocator.

        :param page: Playwright Page instance
        :param element_name: Descriptive name of target UI element
        :param primary_locator: Primary CSS / XPath selector
        :param fallback_locators: Ordered list of alternate selectors
        :param ai_provider: Optional AI provider for locator suggestion triage
        """
        self.page = page
        self.element_name = element_name
        self.primary_locator = primary_locator
        self.fallback_locators = fallback_locators or []
        self.ai_provider = ai_provider or get_ai_provider()
        self.last_used_locator: Optional[str] = None
        self.healing_events: List[Dict[str, Any]] = []

    def find(self, timeout: int = 3000) -> Locator:
        """
        Locate element using primary locator, recovering via fallback chain if necessary.

        :param timeout: Per-attempt timeout in ms
        :return: Playwright Locator of matching element
        :raises TimeoutError: If both primary and all fallback locators fail
        """
        # 1. Attempt Primary Locator
        try:
            logger.debug(f"Attempting primary locator for '{self.element_name}': '{self.primary_locator}'")
            locator = self.page.locator(self.primary_locator)
            locator.wait_for(state="visible", timeout=timeout)
            self.last_used_locator = self.primary_locator
            logger.debug(f"Primary locator succeeded for '{self.element_name}'.")
            return locator
        except Exception as primary_err:
            logger.warning(
                f"Primary locator '{self.primary_locator}' failed for '{self.element_name}'. Initiating healing sequence..."
            )

        # 2. Iterate through Fallback Locators
        for index, fallback in enumerate(self.fallback_locators, start=1):
            try:
                logger.info(f"Trying fallback locator #{index} for '{self.element_name}': '{fallback}'")
                locator = self.page.locator(fallback)
                locator.wait_for(state="visible", timeout=timeout)

                # Record successful healing event
                healing_event = {
                    "element": self.element_name,
                    "failed_locator": self.primary_locator,
                    "healed_with": fallback,
                    "strategy_rank": index,
                    "status": "HEALED",
                }
                self.healing_events.append(healing_event)
                self.last_used_locator = fallback

                logger.info(
                    f"✓ SELF-HEALING SUCCESS: Element '{self.element_name}' located via fallback #{index} ('{fallback}')."
                )
                return locator
            except Exception:
                logger.debug(f"Fallback #{index} ('{fallback}') also failed.")

        # 3. If all locators fail, request AI suggestion for the failure log
        logger.error(f"All {len(self.fallback_locators) + 1} locators failed for element '{self.element_name}'.")
        ai_suggestion = self.request_ai_locator_suggestion()

        error_summary = (
            f"Failed to locate '{self.element_name}'. Primary: '{self.primary_locator}', "
            f"Fallbacks: {self.fallback_locators}. AI Recommendation: {ai_suggestion.get('suggested_locators', [])}"
        )
        raise TimeoutError(error_summary)

    def click(self, timeout: int = 3000) -> None:
        """Find element (with self-healing) and click."""
        locator = self.find(timeout=timeout)
        locator.click()

    def fill(self, text: str, timeout: int = 3000) -> None:
        """Find element (with self-healing) and fill text."""
        locator = self.find(timeout=timeout)
        locator.fill(text)

    def _extract_bounded_dom_context(self, max_chars: int = 1500) -> str:
        """
        Extract bounded, sanitized runtime DOM context from the active Playwright page.

        Prioritizes:
        1. Context around candidates matching keywords from element_name or locator.
        2. Relevant interactive containers (form, main, or body).
        3. Strips sensitive attributes (values, tokens, passwords, cookies).
        4. Bounded to max_chars to prevent prompt bloat.
        5. Returns a placeholder safely if page is closed, detached, or inaccessible.
        """
        try:
            if not self.page or self.page.is_closed():
                return f"<!-- Runtime DOM unavailable: page is closed for '{self.element_name}' -->"

            # Execute in-browser DOM query to extract relevant structural snippet safely
            # Note: We clone/sanitize without sensitive values (input values, passwords, tokens)
            js_script = """
            (keywords) => {
                const sanitize = (node) => {
                    const clone = node.cloneNode(true);
                    // Remove scripts, styles, and SVG paths for compact representation
                    const unneeded = clone.querySelectorAll('script, style, svg, noscript, iframe');
                    unneeded.forEach(el => el.remove());

                    // Sanitize form controls to remove sensitive user input values
                    const inputs = clone.querySelectorAll('input, textarea, select');
                    inputs.forEach(input => {
                        const type = (input.getAttribute('type') || '').toLowerCase();
                        if (type === 'password' || input.name.toLowerCase().includes('pass') || input.name.toLowerCase().includes('token')) {
                            input.setAttribute('value', '[REDACTED]');
                        } else if (input.value) {
                            input.setAttribute('value', '[SANITIZED]');
                        }
                    });
                    return clone;
                };

                // Search for potential element match or parent container
                let bestNode = null;
                for (const kw of keywords) {
                    if (!kw || kw.length < 2) continue;
                    // Try by attribute or text content
                    const candidate = Array.from(document.querySelectorAll('button, a, input, form, [role], [data-testid]'))
                        .find(el => {
                            const text = (el.innerText || el.textContent || '').toLowerCase();
                            const id = (el.id || '').toLowerCase();
                            const testId = (el.getAttribute('data-testid') || '').toLowerCase();
                            const aria = (el.getAttribute('aria-label') || '').toLowerCase();
                            return text.includes(kw) || id.includes(kw) || testId.includes(kw) || aria.includes(kw);
                        });
                    if (candidate) {
                        bestNode = candidate.closest('form, div, section, nav') || candidate;
                        break;
                    }
                }

                // Fallback to active form or main content if no keyword matched
                if (!bestNode) {
                    bestNode = document.querySelector('form') || document.querySelector('main') || document.body;
                }

                if (!bestNode) return '';
                const sanitized = sanitize(bestNode);
                return sanitized.outerHTML || sanitized.innerHTML || '';
            }
            """

            # Build search keywords from element_name and primary_locator
            raw_keywords = [
                part.lower() for part in (self.element_name + " " + self.primary_locator).replace("#", " ")
                .replace(".", " ")
                .replace("[", " ")
                .replace("]", " ")
                .replace("=", " ")
                .replace("'", " ")
                .replace('"', " ")
                .replace("-", " ")
                .replace("_", " ")
                .split()
                if len(part) >= 3 and part.lower() not in ("button", "submit", "login", "non", "existent", "the")
            ]
            # Always include core element name terms if available
            element_terms = [w.lower() for w in self.element_name.split() if len(w) >= 3]
            keywords = list(dict.fromkeys(element_terms + raw_keywords))

            raw_html = self.page.evaluate(js_script, keywords)
            if not raw_html or not str(raw_html).strip():
                return f"<!-- Runtime DOM unavailable: empty content for '{self.element_name}' -->"

            # Normalize whitespace
            normalized_html = " ".join(str(raw_html).split())

            # Bounded truncation
            if len(normalized_html) > max_chars:
                return normalized_html[:max_chars] + f" ... [truncated at {max_chars} chars]"
            return normalized_html

        except Exception as exc:
            logger.warning(
                f"Gracefully intercepted error during DOM context extraction for '{self.element_name}': {exc}"
            )
            return f"<!-- Runtime DOM extraction failed: {type(exc).__name__} for '{self.element_name}' -->"

    def request_ai_locator_suggestion(self) -> Dict[str, Any]:
        """
        Invoke AI provider to analyze failed element and suggest better locators.
        Uses runtime page DOM context when available.
        """
        html_snippet = self._extract_bounded_dom_context()
        prompt = LOCATOR_HEALING_PROMPT.format(
            failed_locator=self.primary_locator,
            element_description=self.element_name,
            html_snippet=html_snippet,
        )
        return self.ai_provider.generate_structured_json(prompt)
