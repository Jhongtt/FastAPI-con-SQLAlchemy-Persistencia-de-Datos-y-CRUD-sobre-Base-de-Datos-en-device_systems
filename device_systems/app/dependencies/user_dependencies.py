from fastapi import HTTPException, status
from app.data.users_db import get_user_by_id, get_user_by_email


def get_user_or_404(user_id: int) -> dict:
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


def validate_email_not_duplicate(email: str, exclude_user_id: int | None = None) -> None:
    existing = get_user_by_email(email)
    if existing and existing["id"] != exclude_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{email}' already exists",
        )


ALLOWED_ROLES = {"admin", "support", "user"}


def validate_role_allowed(role: str) -> str:
    role_lower = role.lower()
    if role_lower not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role must be one of: {', '.join(sorted(ALLOWED_ROLES))}",
        )
    return role_lower


def get_api_config() -> dict:
    return {
        "app_name": "device_systems",
        "version": "2.0.0",
        "description": "API REST para la gestión de usuarios del sistema device_systems",
    }
