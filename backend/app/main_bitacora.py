import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import bitacora

app = FastAPI(
    title="API Taller Automotriz - Servicio de Bitácora",
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
    return {"message": "Servicio de Bitácora Activo"}

app.include_router(bitacora.router, prefix="/api/bitacora", tags=["Bitácora"])
