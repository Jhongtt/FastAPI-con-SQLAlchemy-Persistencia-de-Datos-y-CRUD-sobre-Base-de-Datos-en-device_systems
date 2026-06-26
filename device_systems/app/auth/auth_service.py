from sqlalchemy.orm import Session
from app.models.user_model import User
from app.auth.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status


def register_user(db: Session, data: dict) -> User:
    existing = db.query(User).filter(User.email == data["email"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")

    hashed = get_password_hash(data["password"])
    user = User(
        name=data["name"],
        email=data["email"],
        hashed_password=hashed,
        role=data.get("role", "user"),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")

    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
