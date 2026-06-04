from fastapi import FastAPI, Request
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems. "
    "Implementa CRUD completo con validaciones, manejo de errores, "
    "documentación automática Swagger/OpenAPI y Dependency Injection.",
    version="2.0.0",
    contact={
        "name": "Jhonatan David",
        "url": "https://github.com/Jhongtt",
    },
)


@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return response


app.include_router(user_router)
