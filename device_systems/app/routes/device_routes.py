from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services import device_service, loan_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin, require_admin_or_support
from app.models.user_model import User

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get(
    "/",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Lista todos los dispositivos con filtros opcionales.",
    responses={401: {"description": "No autenticado"}},
)
def list_devices(
    device_type: str = Query(None, description="Filtrar por tipo: laptop, tablet, proyector, etc."),
    is_available: bool = Query(None, description="Filtrar por disponibilidad"),
    brand: str = Query(None, description="Filtrar por marca"),
    search: str = Query(None, description="Buscar por nombre, serial o marca"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return device_service.get_all_devices(
        db, device_type=device_type, is_available=is_available, brand=brand, search=search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener dispositivo por ID",
    description="Retorna un dispositivo especifico por su ID.",
    responses={401: {"description": "No autenticado"}, 404: {"description": "Dispositivo no encontrado"}},
)
def get_one_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo. Requiere rol admin o support.",
    responses={400: {"description": "Serial duplicado"}, 401: {"description": "No autenticado"}, 403: {"description": "No autorizado"}},
)
def create(
    data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    existente = device_service.get_device_by_serial(db, data.serial_number)
    if existente:
        raise HTTPException(status_code=400, detail="El numero de serie ya existe")
    return device_service.create_device(db, data.model_dump())


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo completo",
    description="Reemplaza toda la informacion de un dispositivo. Requiere admin o support.",
    responses={401: {"description": "No autenticado"}, 403: {"description": "No autorizado"}, 404: {"description": "Dispositivo no encontrado"}},
)
def update(
    device_id: int,
    data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if data.serial_number != device.serial_number:
        existente = device_service.get_device_by_serial(db, data.serial_number)
        if existente:
            raise HTTPException(status_code=400, detail="El numero de serie ya existe")
    updated = device_service.update_device(db, device_id, data.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return updated


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcialmente",
    description="Modifica solo los campos enviados.",
    responses={401: {"description": "No autenticado"}, 403: {"description": "No autorizado"}},
)
def patch(
    device_id: int,
    data: DevicePatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    campos = data.model_dump(exclude_unset=True)
    if not campos:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")
    if "serial_number" in campos and campos["serial_number"] != device.serial_number:
        existente = device_service.get_device_by_serial(db, campos["serial_number"])
        if existente:
            raise HTTPException(status_code=400, detail="El numero de serie ya existe")
    updated = device_service.patch_device(db, device_id, campos)
    if not updated:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return updated


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo existente por su ID. Solo admin.",
    responses={401: {"description": "No autenticado"}, 403: {"description": "Requiere rol admin"}, 404: {"description": "Dispositivo no encontrado"}},
)
def delete(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    deleted = device_service.delete_device(db, device_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")


@router.get(
    "/{device_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Historial de prestamos de un dispositivo",
    description="Retorna el historial completo de prestamos de un dispositivo.",
    responses={401: {"description": "No autenticado"}, 404: {"description": "Dispositivo no encontrado"}},
)
def get_device_loans(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return loan_service.get_device_loans(db, device_id)
