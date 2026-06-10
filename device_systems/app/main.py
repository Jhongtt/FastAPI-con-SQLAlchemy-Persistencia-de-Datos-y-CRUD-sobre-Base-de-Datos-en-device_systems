from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.database.connection import engine, Base
from app.models.user_model import User  # noqa: F401
from app.routes.user_routes import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems. "
    "Implementa CRUD completo con persistencia en base de datos SQLite mediante SQLAlchemy, "
    "validaciones Pydantic, manejo de errores y documentación automática Swagger/OpenAPI.",
    version="3.0.0",
    contact={
        "name": "Jhonatan David",
        "url": "https://github.com/Jhongtt",
    },
    lifespan=lifespan,
)


@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "3.0"
    return response


app.include_router(user_router)
