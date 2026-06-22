from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.loan_schema import LoanCreate, LoanUpdate, LoanResponse, LoanDetailResponse
from app.services import loan_service
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get(
    "/",
    response_model=list[LoanResponse],
    summary="Listar prestamos",
    description="Lista todos los prestamos con filtros opcionales por estado, email de usuario o tipo de dispositivo.",
    response_description="Lista de prestamos",
)
def list_loans(
    status: str = Query(None, description="Filtrar por estado: active, returned, overdue"),
    user_email: str = Query(None, description="Filtrar por email del usuario"),
    device_type: str = Query(None, description="Filtrar por tipo de dispositivo"),
    db: Session = Depends(get_db),
):
    return loan_service.get_all_loans(db, status=status, user_email=user_email, device_type=device_type)


@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Listar prestamos con detalles",
    description="Retorna prestamos con informacion completa del usuario y dispositivo. Incluye filtros.",
    response_description="Prestamos con detalles de usuario y dispositivo",
)
def list_loan_details(
    status: str = Query(None, description="Filtrar por estado"),
    user_email: str = Query(None, description="Filtrar por email del usuario"),
    device_type: str = Query(None, description="Filtrar por tipo de dispositivo"),
    db: Session = Depends(get_db),
):
    return loan_service.get_loans_with_details(db, status=status, user_email=user_email, device_type=device_type)


@router.get(
    "/{loan_id}",
    response_model=LoanDetailResponse,
    summary="Obtener prestamo por ID",
    description="Retorna un prestamo especifico con datos del usuario y dispositivo.",
    response_description="Detalle del prestamo",
)
def get_one_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = loan_service.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return loan


@router.post(
    "/",
    response_model=LoanDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear prestamo",
    description="Crea un nuevo prestamo. Valida que el usuario y dispositivo existan y que el dispositivo este disponible.",
    response_description="Prestamo creado",
)
def create(data: LoanCreate, db: Session = Depends(get_db)):
    try:
        loan = loan_service.create_loan(db, data.model_dump())
        return loan
    except ValueError as e:
        if "no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        if "no disponible" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{loan_id}/return",
    response_model=LoanDetailResponse,
    summary="Devolver dispositivo",
    description="Marca un prestamo como devuelto. Actualiza la fecha de devolucion y marca el dispositivo como disponible.",
    response_description="Prestamo actualizado",
)
def return_device(loan_id: int, db: Session = Depends(get_db)):
    try:
        loan = loan_service.return_loan(db, loan_id)
        return loan
    except ValueError as e:
        if "no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=409, detail=str(e))
