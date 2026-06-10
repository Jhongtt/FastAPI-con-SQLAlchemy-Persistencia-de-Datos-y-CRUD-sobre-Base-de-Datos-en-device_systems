from fastapi import HTTPException, status

ALLOWED_ROLES = {"admin", "support", "user"}


def validate_role_allowed(role: str) -> str:
    role_lower = role.lower()
    if role_lower not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role must be one of: {', '.join(sorted(ALLOWED_ROLES))}",
        )
    return role_lower


def get_api_config() -> dict:
    return {
        "app_name": "device_systems",
        "version": "2.0.0",
        "description": "API REST para la gestión de usuarios del sistema device_systems",
    }
