"""
API Automation Tests.

Validates:
- GET (collection, by ID, with query params)
- POST (resource creation, payload assertions)
- PUT (full resource update)
- PATCH (partial modification)
- DELETE (resource deletion)
- Status code validation
- Headers & response structure verification
- Negative testing & error responses
- Authentication simulation
"""

import pytest
from requests import Response
from api.clients.api_client import APIClient
from api.clients.posts_client import PostsClient
from api.models.post_model import PostModel
from utils.test_data import TestDataManager


@pytest.mark.api
@pytest.mark.smoke
class TestPostsAPI:
    """Test suite for /posts CRUD REST API endpoints."""

    def test_get_all_posts(self, posts_client: PostsClient):
        """Verify fetching collection of posts returns 200 and non-empty list."""
        response: Response = posts_client.get_all_posts()

        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        assert response.headers.get("Content-Type", "").startswith("application/json")

        data = response.json()
        assert isinstance(data, list), "Response body should be a JSON array"
        assert len(data) > 0, "Posts collection should not be empty"

        # Validate structure of first item
        first_post = data[0]
        assert "id" in first_post
        assert "title" in first_post
        assert "body" in first_post
        assert "userId" in first_post

    def test_get_post_by_id(self, posts_client: PostsClient):
        """Verify fetching single post by ID returns expected fields."""
        post_id = 1
        response: Response = posts_client.get_post_by_id(post_id)

        assert response.status_code == 200
        post = response.json()
        assert post["id"] == post_id
        assert isinstance(post["title"], str) and len(post["title"]) > 0
        assert isinstance(post["userId"], int)

    def test_get_posts_with_query_params(self, posts_client: PostsClient):
        """Verify filtering posts by query parameter (userId=1)."""
        target_user_id = 1
        response: Response = posts_client.get_all_posts(user_id=target_user_id)

        assert response.status_code == 200
        posts = response.json()
        assert len(posts) > 0

        # Assert every returned post belongs to userId=1
        for p in posts:
            assert p["userId"] == target_user_id

    def test_create_post_success(self, posts_client: PostsClient, test_data: TestDataManager):
        """Verify creating a new post with valid JSON payload returns 201 Created."""
        api_data = test_data.load_json("api_data.json")
        payload = api_data["posts"]["valid_post"]

        response: Response = posts_client.create_post(payload)

        assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
        created = response.json()

        assert "id" in created
        assert created["title"] == payload["title"]
        assert created["body"] == payload["body"]
        assert created["userId"] == payload["userId"]

    def test_create_post_using_pydantic_model(self, posts_client: PostsClient):
        """Verify post creation using strongly-typed Pydantic model."""
        post_model = PostModel(
            title="Pydantic Validated AI Test Post",
            body="Ensuring schema validation in automated test pipeline.",
            userId=2,
        )

        response: Response = posts_client.create_post(post_model)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == post_model.title
        assert data["userId"] == post_model.userId

    def test_update_post_put(self, posts_client: PostsClient, test_data: TestDataManager):
        """Verify full replacement of a post via PUT request."""
        api_data = test_data.load_json("api_data.json")
        payload = api_data["posts"]["updated_post"]
        post_id = 1

        response: Response = posts_client.update_post(post_id, payload)
        assert response.status_code == 200

        updated = response.json()
        assert updated["id"] == post_id
        assert updated["title"] == payload["title"]
        assert updated["body"] == payload["body"]

    def test_patch_post_partial_update(self, posts_client: PostsClient, test_data: TestDataManager):
        """Verify partial update of post title via PATCH request."""
        api_data = test_data.load_json("api_data.json")
        patch_payload = api_data["posts"]["patch_post"]
        post_id = 1

        response: Response = posts_client.patch_post(post_id, patch_payload)
        assert response.status_code == 200

        patched = response.json()
        assert patched["id"] == post_id
        assert patched["title"] == patch_payload["title"]

    def test_delete_post(self, posts_client: PostsClient):
        """Verify deleting a post returns 200 OK."""
        post_id = 1
        response: Response = posts_client.delete_post(post_id)
        assert response.status_code in (200, 204)


@pytest.mark.api
@pytest.mark.negative
class TestAPINegativeScenarios:
    """Negative test suite testing error handling, invalid parameters, and 404s."""

    @pytest.mark.parametrize(
        "invalid_id, expected_status",
        [
            (999999, 404),
            ("invalid_route_slug", 404),
        ],
    )
    def test_get_nonexistent_post_returns_404(
        self, posts_client: PostsClient, invalid_id, expected_status
    ):
        """Verify requesting non-existent post IDs returns HTTP 404."""
        response = posts_client.get_post_by_id(invalid_id)
        assert response.status_code == expected_status

    def test_invalid_endpoint_route(self, api_client: APIClient):
        """Verify hitting an unmapped endpoint route returns 404."""
        response = api_client.get("/non_existent_unmapped_endpoint_route")
        assert response.status_code == 404

    def test_authentication_header_handling(self, api_client: APIClient):
        """Verify custom auth headers and token updates work seamlessly."""
        # Set simulated token
        api_client.set_auth_token("simulated_jwt_token_xyz_123")
        response = api_client.get("/posts/1")
        assert response.status_code == 200

        # Clear token
        api_client.clear_auth_token()
        assert "Authorization" not in api_client.session.headers
