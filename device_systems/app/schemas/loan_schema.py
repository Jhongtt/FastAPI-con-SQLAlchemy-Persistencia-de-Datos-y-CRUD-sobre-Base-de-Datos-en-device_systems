from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime

ESTADOS_VALIDOS = {"active", "returned", "overdue"}


class UserBasic(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class DeviceBasic(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = ConfigDict(from_attributes=True)


class LoanCreate(BaseModel):
    user_id: int = Field(..., gt=0, description="ID del usuario que solicita el prestamo")
    device_id: int = Field(..., gt=0, description="ID del dispositivo a prestar")


class LoanUpdate(BaseModel):
    status: str = Field(..., description="Estado: active, returned, overdue")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado invalido. Opciones: {sorted(ESTADOS_VALIDOS)}")
        return v


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(BaseModel):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str
    user: UserBasic
    device: DeviceBasic

    model_config = ConfigDict(from_attributes=True)
