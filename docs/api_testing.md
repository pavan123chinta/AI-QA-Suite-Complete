# API Testing Architecture & Guidelines

## Overview
The API automation layer in **AI-QA-Suite** is built using Python `requests`, providing a structured, maintainable, and type-safe approach to RESTful service testing.

## Layered Design
```
API Tests (tests/api/test_posts_api.py)
   ↓
Domain Service Client (api/clients/posts_client.py)
   ↓
Core Reusable HTTP Client (api/clients/api_client.py)
   ↓
Python Requests Session
   ↓
RESTful Service Endpoints
```

## Supported Operations & Validations
- **HTTP Methods**: Full verification of `GET`, `POST`, `PUT`, `PATCH`, and `DELETE`.
- **Query & Path Parameters**: Filtering collections by `userId`, targeting specific resources by `id`.
- **Schema Validation**: Uses `Pydantic` models (`PostModel`, `UserModel`) for strong data contract validation.
- **Negative Testing**: Verification of HTTP 404 for nonexistent resources and unmapped endpoints.
- **Security & Headers**: Token lifecycle management (`set_auth_token`, `clear_auth_token`) and automatic credential masking in test logs.
