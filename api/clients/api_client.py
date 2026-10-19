"""
Reusable HTTP API Client Wrapper around Requests.

Provides centralized logging, error handling, session management,
header sanitation, timing metrics, and convenient REST helpers (GET, POST, PUT, PATCH, DELETE).
"""

import time
from typing import Any, Dict, Optional, Union
import requests
from requests import Response, Session

from utils.config import config
from utils.logger import get_logger
from utils.helpers import sanitize_headers

logger = get_logger("APIClient")


class APIClient:
    """
    Robust HTTP API Client for QA Automation.
    Encapsulates base URL, headers, session lifecycle, and detailed execution logging.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: int = 15,
        auth_token: Optional[str] = None,
    ):
        """
        Initialize APIClient.

        :param base_url: Base URL for endpoints (defaults to config.api_base_url)
        :param default_headers: Optional default headers dictionary
        :param timeout: Request timeout in seconds
        :param auth_token: Optional Bearer token for authentication
        """
        self.base_url = (base_url or config.api_base_url).rstrip("/")
        self.timeout = timeout
        self.session = Session()

        # Set default headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "AI-QA-Suite-Automation-Client/1.0",
        }
        if default_headers:
            headers.update(default_headers)

        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        self.session.headers.update(headers)
        logger.debug(f"APIClient initialized with base_url={self.base_url}")

    def set_auth_token(self, token: str) -> None:
        """Dynamically update Bearer authentication token."""
        self.session.headers["Authorization"] = f"Bearer {token}"
        logger.debug("Authentication Bearer token updated.")

    def clear_auth_token(self) -> None:
        """Remove authentication token for negative auth testing."""
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
            logger.debug("Authentication token cleared.")

    def _build_url(self, endpoint: str) -> str:
        """Construct full URL from endpoint."""
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json_data: Optional[Union[Dict[str, Any], list]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> Response:
        """
        Execute raw HTTP request with logging and performance metrics.

        :param method: HTTP Verb ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
        :param endpoint: Resource route or full URL
        :param params: URL query parameters
        :param data: Form data or string payload
        :param json_data: JSON serializable object
        :param headers: Custom request headers
        :param timeout: Request timeout in seconds
        :return: requests.Response object
        """
        url = self._build_url(endpoint)
        request_timeout = timeout or self.timeout
        effective_headers = sanitize_headers(headers or dict(self.session.headers))

        logger.info(f"==> HTTP {method.upper()} {url}")
        if params:
            logger.info(f"    Params: {params}")
        if json_data:
            logger.info(f"    Payload: {json_data}")
        logger.debug(f"    Headers: {effective_headers}")

        start_time = time.time()
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                timeout=request_timeout,
                **kwargs,
            )
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            logger.info(f"<== HTTP {response.status_code} ({elapsed_ms}ms) from {url}")

            # Try logging snippet of response body if JSON or text
            try:
                body_snippet = response.json()
                logger.debug(f"    Response JSON: {body_snippet}")
            except Exception:
                if response.text:
                    logger.debug(f"    Response Text (first 200 chars): {response.text[:200]}")

            return response
        except requests.exceptions.RequestException as exc:
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(f"<== HTTP Request FAILED after {elapsed_ms}ms: {exc}")
            raise

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Response:
        """Execute HTTP GET."""
        return self.request("GET", endpoint, params=params, headers=headers, **kwargs)

    def post(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], list]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Response:
        """Execute HTTP POST."""
        return self.request("POST", endpoint, params=params, json_data=json_data, headers=headers, **kwargs)

    def put(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], list]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Response:
        """Execute HTTP PUT."""
        return self.request("PUT", endpoint, params=params, json_data=json_data, headers=headers, **kwargs)

    def patch(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], list]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Response:
        """Execute HTTP PATCH."""
        return self.request("PATCH", endpoint, params=params, json_data=json_data, headers=headers, **kwargs)

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Response:
        """Execute HTTP DELETE."""
        return self.request("DELETE", endpoint, params=params, headers=headers, **kwargs)
