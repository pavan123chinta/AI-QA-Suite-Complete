"""
API Endpoint Path Constants.
"""


class Endpoints:
    """Central registry of API resource endpoint paths."""
    POSTS = "/posts"
    POST_BY_ID = "/posts/{id}"
    USERS = "/users"
    USER_BY_ID = "/users/{id}"
    COMMENTS = "/comments"
    POST_COMMENTS = "/posts/{id}/comments"
    INVALID_ROUTE = "/non_existent_route_404"
