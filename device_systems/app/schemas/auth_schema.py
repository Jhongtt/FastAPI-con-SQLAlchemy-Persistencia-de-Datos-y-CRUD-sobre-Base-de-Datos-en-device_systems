from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
import re


class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nombre completo del usuario")
    email: str = Field(..., description="Correo electronico valido")
    password: str = Field(..., min_length=8, description="Contrasena segura")
    role: str = Field(default="user", description="Rol del usuario: admin, support, user")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Formato de email invalido")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contrasena no debe contener espacios en blanco")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contrasena debe contener al menos una mayuscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contrasena debe contener al menos una minuscula")
        if not re.search(r"\d", v):
            raise ValueError("La contrasena debe contener al menos un numero")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        valid_roles = {"admin", "support", "user"}
        if v not in valid_roles:
            raise ValueError(f"Rol invalido. Opciones: {', '.join(sorted(valid_roles))}")
        return v

    @model_validator(mode="after")
    def check_password_not_name(self):
        if self.name.lower() in self.password.lower():
            raise ValueError("La contrasena no debe contener el nombre del usuario")
        return self


class UserLogin(BaseModel):
    email: str = Field(..., description="Correo electronico")
    password: str = Field(..., description="Contrasena")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Formato de email invalido")
        return v.lower()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None


class UserAuthResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
