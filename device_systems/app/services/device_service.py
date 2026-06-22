from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.device_model import Device


def get_all_devices(
    db: Session,
    device_type: str = None,
    is_available: bool = None,
    brand: str = None,
    search: str = None,
) -> list[Device]:
    query = db.query(Device)
    if device_type is not None:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand is not None:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search is not None:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%"),
            )
        )
    return query.all()


def get_device_by_id(db: Session, device_id: int) -> Device | None:
    return db.query(Device).filter(Device.id == device_id).first()


def get_device_by_serial(db: Session, serial: str) -> Device | None:
    return db.query(Device).filter(Device.serial_number == serial).first()


def create_device(db: Session, data: dict) -> Device:
    device = Device(**data)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update_device(db: Session, device_id: int, data: dict) -> Device | None:
    device = get_device_by_id(db, device_id)
    if not device:
        return None
    for key, value in data.items():
        setattr(device, key, value)
    db.commit()
    db.refresh(device)
    return device


def patch_device(db: Session, device_id: int, data: dict) -> Device | None:
    return update_device(db, device_id, data)


def delete_device(db: Session, device_id: int) -> bool:
    device = get_device_by_id(db, device_id)
    if not device:
        return False
    db.delete(device)
    db.commit()
    return True
