"""
Pydantic Models for API Resources & Payloads.
Provides type safety and schema validation.
"""

from typing import Optional
from pydantic import BaseModel, Field


class PostModel(BaseModel):
    """Data model representing a Post resource."""
    id: Optional[int] = None
    title: str = Field(..., min_length=1, description="Post title")
    body: str = Field(..., min_length=1, description="Post body content")
    userId: int = Field(..., gt=0, description="User ID owner")


class UserModel(BaseModel):
    """Data model representing a User resource."""
    id: Optional[int] = None
    name: str
    username: str
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None


class CommentModel(BaseModel):
    """Data model representing a Comment resource."""
    id: Optional[int] = None
    postId: int
    name: str
    email: str
    body: str
