from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services import user_service, loan_service
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/users", tags=["Users"])

ROLES_VALIDOS = ["admin", "support", "user"]


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Filtros opcionales por rol o estado activo.",
    response_description="Lista de usuarios",
)
def list_users(role: str = None, is_active: bool = None, db: Session = Depends(get_db)):
    return user_service.get_all_users(db, role=role, is_active=is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Retorna un usuario especifico por su ID.",
    response_description="Datos del usuario",
)
def get_one_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario. El email debe ser unico. Roles: admin, support, user.",
    response_description="Usuario creado",
)
def create(data: UserCreate, db: Session = Depends(get_db)):
    if data.role not in ROLES_VALIDOS:
        raise HTTPException(
            status_code=400, detail=f"Rol no valido. Opciones: {ROLES_VALIDOS}"
        )
    existente = user_service.get_user_by_email(db, data.email)
    if existente:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
    return user_service.create_user(db, data.model_dump())


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza toda la informacion de un usuario.",
    response_description="Usuario actualizado",
)
def update(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if data.role not in ROLES_VALIDOS:
        raise HTTPException(
            status_code=400, detail=f"Rol no valido. Opciones: {ROLES_VALIDOS}"
        )
    if data.email != user.email:
        existente = user_service.get_user_by_email(db, data.email)
        if existente:
            raise HTTPException(status_code=400, detail="El email ya esta registrado")
    updated = user_service.update_user(db, user_id, data.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Modifica solo los campos enviados en el cuerpo.",
    response_description="Usuario actualizado parcialmente",
)
def patch(user_id: int, data: UserPatch, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    campos = data.model_dump(exclude_unset=True)
    if not campos:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")
    if "role" in campos and campos["role"] not in ROLES_VALIDOS:
        raise HTTPException(
            status_code=400, detail=f"Rol no valido. Opciones: {ROLES_VALIDOS}"
        )
    if "email" in campos and campos["email"] != user.email:
        existente = user_service.get_user_by_email(db, campos["email"])
        if existente:
            raise HTTPException(status_code=400, detail="El email ya esta registrado")
    updated = user_service.patch_user(db, user_id, campos)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente por su ID.",
)
def delete(user_id: int, db: Session = Depends(get_db)):
    deleted = user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.get(
    "/{user_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Prestamos de un usuario",
    description="Retorna todos los prestamos asociados a un usuario especifico.",
    response_description="Lista de prestamos del usuario",
)
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return loan_service.get_user_loans(db, user_id)
