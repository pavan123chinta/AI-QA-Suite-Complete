"""
General helper functions for AI-QA-Suite.

Includes payload sanitizers, random data generators, and timestamp helpers.
"""

import uuid
import random
import string
from typing import Dict, Any


def generate_unique_id(prefix: str = "id") -> str:
    """Generate a unique string identifier."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def generate_random_email(domain: str = "example.com") -> str:
    """Generate a random test email address."""
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"qa_user_{random_str}@{domain}"


def generate_random_string(length: int = 10) -> str:
    """Generate a random alphanumeric string."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def sanitize_headers(headers: Dict[str, Any]) -> Dict[str, Any]:
    """Mask sensitive tokens/keys in headers for safe logging."""
    sanitized = dict(headers)
    for sensitive_key in ["Authorization", "api-key", "token", "x-api-key", "password"]:
        for key in list(sanitized.keys()):
            if sensitive_key.lower() in key.lower():
                sanitized[key] = "********"
    return sanitized
