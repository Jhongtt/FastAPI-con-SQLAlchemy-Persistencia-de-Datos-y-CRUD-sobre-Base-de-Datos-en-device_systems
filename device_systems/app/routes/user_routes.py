from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.schemas.response_schema import StandardResponse
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserUpdateFull
from app.services.user_service import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
)
from app.dependencies.user_dependencies import validate_role_allowed

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=StandardResponse,
    summary="List all users",
    description="Retrieves a paginated list of users with optional filtering by role, active status, and sorting.",
    response_description="List of users retrieved successfully",
)
def list_users_route(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    role: Optional[str] = Query(None, description="Filter by role (admin, support, user)"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: Optional[str] = Query(None, description="Sort by field (name, created_at)"),
    sort_order: str = Query("asc", description="Sort order (asc, desc)"),
    db: Session = Depends(get_db),
):
    results = get_users(
        db=db,
        skip=skip,
        limit=limit,
        role=role,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return {
        "data": [UserResponse.model_validate(u).model_dump() for u in results],
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
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user(db=db, user_id=user_id)
    return {
        "data": UserResponse.model_validate(user).model_dump(),
        "message": "User retrieved successfully",
        "status_code": status.HTTP_200_OK,
    }


@router.post(
    "",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Creates a new user with the provided data. Validates email uniqueness and role permissions.",
    response_description="User created successfully",
)
def create_user_route(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    validate_role_allowed(user_data.role)
    new_user = create_user(db=db, user_data=user_data.model_dump())
    return {
        "data": UserResponse.model_validate(new_user).model_dump(),
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
    db: Session = Depends(get_db),
):
    validate_role_allowed(user_data.role)
    updated = update_user(db=db, user_id=user_id, update_data=user_data.model_dump())
    return {
        "data": UserResponse.model_validate(updated).model_dump(),
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
    db: Session = Depends(get_db),
):
    update_fields = user_data.model_dump(exclude_unset=True)
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )
    if "role" in update_fields:
        validate_role_allowed(update_fields["role"])
    updated = update_user(db=db, user_id=user_id, update_data=update_fields)
    return {
        "data": UserResponse.model_validate(updated).model_dump(),
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
    db: Session = Depends(get_db),
):
    delete_user(db=db, user_id=user_id)
    return None
