from sqlalchemy.orm import Session
from app.models.user_model import User
from app.auth.security import get_password_hash


def get_all_users(db: Session, role: str = None, is_active: bool = None) -> list[User]:
    query = db.query(User)
    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, data: dict) -> User:
    password = data.pop("password", None)
    if password:
        data["hashed_password"] = get_password_hash(password)
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, data: dict) -> User | None:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    if "password" in data:
        data["hashed_password"] = get_password_hash(data.pop("password"))
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def patch_user(db: Session, user_id: int, data: dict) -> User | None:
    return update_user(db, user_id, data)


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
