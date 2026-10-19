"""
Posts Service API Client.

High-level domain client encapsulating all CRUD operations for the /posts resource.
"""

from typing import Any, Dict, Optional, Union
from requests import Response

from api.clients.api_client import APIClient
from api.endpoints.routes import Endpoints
from api.models.post_model import PostModel


class PostsClient:
    """Service wrapper for /posts REST endpoints."""

    def __init__(self, api_client: Optional[APIClient] = None):
        """Initialize with existing or fresh APIClient."""
        self.client = api_client or APIClient()

    def get_all_posts(self, user_id: Optional[int] = None) -> Response:
        """Fetch all posts, optionally filtered by user ID."""
        params = {"userId": user_id} if user_id else None
        return self.client.get(Endpoints.POSTS, params=params)

    def get_post_by_id(self, post_id: Union[int, str]) -> Response:
        """Fetch a specific post by ID."""
        endpoint = Endpoints.POST_BY_ID.format(id=post_id)
        return self.client.get(endpoint)

    def create_post(self, payload: Union[Dict[str, Any], PostModel]) -> Response:
        """Create a new post."""
        json_body = payload.model_dump() if isinstance(payload, PostModel) else payload
        return self.client.post(Endpoints.POSTS, json_data=json_body)

    def update_post(self, post_id: Union[int, str], payload: Union[Dict[str, Any], PostModel]) -> Response:
        """Fully update a post (PUT)."""
        endpoint = Endpoints.POST_BY_ID.format(id=post_id)
        json_body = payload.model_dump() if isinstance(payload, PostModel) else payload
        return self.client.put(endpoint, json_data=json_body)

    def patch_post(self, post_id: Union[int, str], partial_payload: Dict[str, Any]) -> Response:
        """Partially update a post (PATCH)."""
        endpoint = Endpoints.POST_BY_ID.format(id=post_id)
        return self.client.patch(endpoint, json_data=partial_payload)

    def delete_post(self, post_id: Union[int, str]) -> Response:
        """Delete a post by ID."""
        endpoint = Endpoints.POST_BY_ID.format(id=post_id)
        return self.client.delete(endpoint)
