from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

app = FastAPI(
    title="device_systems API",
    description="API REST para gestion de usuarios, dispositivos y prestamos",
    version="3.0.0",
    contact={"name": "device_systems Team"},
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/")
def home():
    return {"mensaje": "device_systems API funcionando"}
