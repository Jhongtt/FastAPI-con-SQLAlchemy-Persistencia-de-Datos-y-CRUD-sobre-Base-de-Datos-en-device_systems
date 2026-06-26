from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional

ROLES_PERMITIDOS = ["admin", "support", "user"]


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del usuario")
    email: EmailStr
    password: str = Field(..., min_length=8, description="Contrasena del usuario")
    role: str = Field(default="user", description="Roles: admin, support, user")
    is_active: bool = True

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ROLES_PERMITIDOS:
            raise ValueError(f"Rol invalido. Opciones: {ROLES_PERMITIDOS}")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contrasena no debe contener espacios")
        import re
        if not re.search(r"[A-Z]", v):
            raise ValueError("Debe contener al menos una mayuscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("Debe contener al menos una minuscula")
        if not re.search(r"\d", v):
            raise ValueError("Debe contener al menos un numero")
        return v


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: str
    is_active: bool


class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
