from fastapi import HTTPException, status
from app.data.users_db import (
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    create_user,
    update_user,
    delete_user,
)


def list_users(skip: int = 0, limit: int = 10, role: str | None = None, is_active: bool | None = None) -> list[dict]:
    results = get_all_users()
    if role:
        results = [u for u in results if u["role"] == role.lower()]
    if is_active is not None:
        results = [u for u in results if u["is_active"] == is_active]
    return results[skip: skip + limit]


def get_user(user_id: int) -> dict:
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


def create_new_user(user_data: dict) -> dict:
    existing = get_user_by_email(user_data["email"])
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_data['email']}' already exists",
        )
    return create_user(user_data)


def update_existing_user(user_id: int, update_data: dict) -> dict:
    if "email" in update_data:
        existing = get_user_by_email(update_data["email"])
        if existing and existing["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{update_data['email']}' already exists",
            )
    updated = update_user(user_id, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return updated


def delete_existing_user(user_id: int) -> None:
    if not get_user_by_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    delete_user(user_id)
