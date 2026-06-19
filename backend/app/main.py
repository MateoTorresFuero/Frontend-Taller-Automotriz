import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
import app.models
from app.routers import clientes, catalogos, auth, ost, bitacora

app = FastAPI(
    title="API Taller Automotriz",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
]
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Taller Automotriz"}

app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(catalogos.router, prefix="/api/catalogos", tags=["Catálogos"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(ost.router, prefix="/api/ost", tags=["Órdenes de Trabajo"])
app.include_router(bitacora.router, prefix="/api/bitacora", tags=["Bitácora"])
