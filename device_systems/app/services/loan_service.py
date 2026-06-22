from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from datetime import datetime, timezone
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device


def get_all_loans(
    db: Session,
    status: str = None,
    user_email: str = None,
    device_type: str = None,
) -> list[Loan]:
    query = db.query(Loan).options(joinedload(Loan.user), joinedload(Loan.device))
    if status is not None:
        query = query.filter(Loan.status == status)
    if user_email is not None:
        query = query.join(Loan.user).filter(User.email.ilike(f"%{user_email}%"))
    if device_type is not None:
        query = query.join(Loan.device).filter(Device.device_type == device_type)
    return query.all()


def get_loan_by_id(db: Session, loan_id: int) -> Loan | None:
    return (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.id == loan_id)
        .first()
    )


def get_loans_with_details(
    db: Session,
    status: str = None,
    user_email: str = None,
    device_type: str = None,
) -> list[Loan]:
    return get_all_loans(db, status, user_email, device_type)


def create_loan(db: Session, data: dict) -> Loan:
    user = db.query(User).filter(User.id == data["user_id"]).first()
    if not user:
        raise ValueError("Usuario no encontrado")

    device = db.query(Device).filter(Device.id == data["device_id"]).first()
    if not device:
        raise ValueError("Dispositivo no encontrado")

    if not device.is_available:
        raise ValueError("Dispositivo no disponible")

    loan = Loan(
        user_id=data["user_id"],
        device_id=data["device_id"],
        status="active",
        loan_date=datetime.now(timezone.utc),
    )
    device.is_available = False

    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan_id: int) -> Loan | None:
    loan = (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.id == loan_id)
        .first()
    )
    if not loan:
        raise ValueError("Prestamo no encontrado")

    if loan.status == "returned":
        raise ValueError("El prestamo ya fue devuelto")

    loan.status = "returned"
    loan.return_date = datetime.now(timezone.utc)

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)
    return loan


def get_user_loans(db: Session, user_id: int) -> list[Loan]:
    return (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.user_id == user_id)
        .all()
    )


def get_device_loans(db: Session, device_id: int) -> list[Loan]:
    return (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.device_id == device_id)
        .all()
    )
