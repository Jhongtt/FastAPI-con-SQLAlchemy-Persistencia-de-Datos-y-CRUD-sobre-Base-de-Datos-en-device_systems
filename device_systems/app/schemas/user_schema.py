from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., max_length=100)
    role: str = Field(default="user", max_length=20)
    is_active: bool = Field(default=True)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v.lower().strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        allowed = {"admin", "support", "user"}
        if v.lower() not in allowed:
            raise ValueError(f"Role must be one of: {', '.join(sorted(allowed))}")
        return v.lower()


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if "@" not in v or "." not in v.split("@")[-1]:
                raise ValueError("Invalid email format")
            return v.lower().strip()
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            allowed = {"admin", "support", "user"}
            if v.lower() not in allowed:
                raise ValueError(f"Role must be one of: {', '.join(sorted(allowed))}")
            return v.lower()
        return v


class UserUpdateFull(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., max_length=100)
    role: str = Field(..., max_length=20)
    is_active: bool = Field(...)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v.lower().strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        allowed = {"admin", "support", "user"}
        if v.lower() not in allowed:
            raise ValueError(f"Role must be one of: {', '.join(sorted(allowed))}")
        return v.lower()


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
