from typing import Optional
from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from app.schemas.response_schema import StandardResponse
from app.schemas.user_schema import UserCreate, UserUpdate, UserUpdateFull
from app.services.user_service import (
    list_users,
    get_user,
    create_new_user,
    update_existing_user,
    delete_existing_user,
)
from app.dependencies.user_dependencies import (
    get_user_or_404,
    validate_email_not_duplicate,
    validate_role_allowed,
    get_api_config,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=StandardResponse,
    summary="List all users",
    description="Retrieves a paginated list of users with optional filtering by role and active status.",
    response_description="List of users retrieved successfully",
)
def list_users_route(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    role: Optional[str] = Query(None, description="Filter by role (admin, support, user)"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    config: dict = Depends(get_api_config),
):
    results = list_users(skip=skip, limit=limit, role=role, is_active=is_active)
    return {
        "data": results,
        "message": "Users retrieved successfully",
        "status_code": status.HTTP_200_OK,
    }


@router.get(
    "/{user_id}",
    response_model=StandardResponse,
    summary="Get user by ID",
    description="Retrieves a single user by their unique identifier.",
    response_description="User retrieved successfully",
)
def get_user_route(
    user: dict = Depends(get_user_or_404),
):
    return {
        "data": user,
        "message": "User retrieved successfully",
        "status_code": status.HTTP_200_OK,
    }


@router.post(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Creates a new user with the provided data. Validates email uniqueness and role permissions.",
    response_description="User created successfully",
)
def create_user_route(
    user_data: UserCreate,
    config: dict = Depends(get_api_config),
):
    validate_email_not_duplicate(user_data.email)
    validate_role_allowed(user_data.role)
    new_user = create_new_user(user_data.model_dump())
    return {
        "data": new_user,
        "message": "User created successfully",
        "status_code": status.HTTP_201_CREATED,
    }


@router.put(
    "/{user_id}",
    response_model=StandardResponse,
    summary="Update user completely",
    description="Replaces all fields of an existing user. All fields are required.",
    response_description="User updated successfully",
)
def update_user_full_route(
    user_id: int,
    user_data: UserUpdateFull,
    _: dict = Depends(get_user_or_404),
):
    validate_email_not_duplicate(user_data.email, exclude_user_id=user_id)
    validate_role_allowed(user_data.role)
    updated = update_existing_user(user_id, user_data.model_dump())
    return {
        "data": updated,
        "message": "User updated successfully",
        "status_code": status.HTTP_200_OK,
    }


@router.patch(
    "/{user_id}",
    response_model=StandardResponse,
    summary="Update user partially",
    description="Updates only the provided fields of an existing user. Returns 400 if no fields are sent.",
    response_description="User updated partially",
)
def update_user_partial_route(
    user_id: int,
    user_data: UserUpdate,
    _: dict = Depends(get_user_or_404),
):
    update_fields = user_data.model_dump(exclude_unset=True)
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )
    if "email" in update_fields:
        validate_email_not_duplicate(update_fields["email"], exclude_user_id=user_id)
    if "role" in update_fields:
        validate_role_allowed(update_fields["role"])
    updated = update_existing_user(user_id, update_fields)
    return {
        "data": updated,
        "message": "User updated partially",
        "status_code": status.HTTP_200_OK,
    }


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Deletes an existing user by their ID. Returns 204 with no content on success.",
    response_description="User deleted successfully (no content)",
)
def delete_user_route(
    user_id: int,
    _: dict = Depends(get_user_or_404),
):
    delete_existing_user(user_id)
    return None
