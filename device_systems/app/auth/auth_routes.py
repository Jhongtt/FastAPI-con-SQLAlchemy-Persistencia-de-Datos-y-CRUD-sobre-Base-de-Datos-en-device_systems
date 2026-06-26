from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.auth_schema import UserRegister, UserLogin, Token, UserAuthResponse
from app.auth import auth_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserAuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea un usuario con contrasena segura. El email debe ser unico.",
    responses={
        400: {"description": "Email duplicado o datos invalidos"},
        422: {"description": "Error de validacion"},
    },
)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data.model_dump())


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesion",
    description="Autentica al usuario y retorna un token JWT.",
    responses={
        401: {"description": "Credenciales invalidas"},
        403: {"description": "Usuario inactivo"},
    },
)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, data.email, data.password)


@router.get(
    "/me",
    response_model=UserAuthResponse,
    summary="Obtener usuario autenticado",
    description="Retorna los datos del usuario autenticado mediante token Bearer.",
    responses={
        401: {"description": "Token invalido o no proporcionado"},
    },
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
