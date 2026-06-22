from pydantic import BaseModel, EmailStr, Field
from typing import Optional

ROLES_PERMITIDOS = ["admin", "support", "user"]


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: str = Field(..., description="Roles validos: admin, support, user")
    is_active: bool = True


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

    model_config = {"from_attributes": True}
