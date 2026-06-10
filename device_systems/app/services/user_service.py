from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.user_model import User


def create_user(db: Session, user_data: dict) -> User:
    existing = db.query(User).filter(User.email == user_data["email"]).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_data['email']}' already exists",
        )
    user_data.pop("password", None)
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    role: str | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    sort_order: str = "asc",
) -> list[User]:
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if sort_by in ("name", "created_at"):
        order_func = asc if sort_order == "asc" else desc
        query = query.order_by(order_func(getattr(User, sort_by)))
    return query.offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


def update_user(db: Session, user_id: int, update_data: dict) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    if "email" in update_data:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{update_data['email']}' already exists",
            )
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    db.delete(db_user)
    db.commit()
