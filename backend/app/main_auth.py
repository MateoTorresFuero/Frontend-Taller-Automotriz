import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
import app.models
from app.routers import auth, catalogos

app = FastAPI(
    title="API Taller Automotriz - Servicio de Autenticación",
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
    return {"message": "Servicio de Autenticación Activo"}

app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(catalogos.router, prefix="/api/catalogos", tags=["Catálogos"])
