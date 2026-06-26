from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router
from app.middlewares.request_middleware import RequestMiddleware

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestion de usuarios, dispositivos y prestamos",
    version="3.0.0",
    contact={"name": "device_systems Team"},
    license_info={"name": "MIT"},
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestMiddleware)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get(
    "/",
    tags=["Security"],
    summary="Health check",
    description="Endpoint publico para verificar que la API funciona.",
)
def home():
    return {"mensaje": "device_systems API funcionando", "version": "3.0.0"}
