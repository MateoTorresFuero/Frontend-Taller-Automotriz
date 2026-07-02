from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.schemas.ost import OSTCreate, OSTOut
from app.services import ost_service

router = APIRouter()


@router.post("/", response_model=OSTOut, status_code=status.HTTP_201_CREATED)
def registrar_ost(ost_in: OSTCreate, db: Session = Depends(get_db)):
    return ost_service.crear_ost(db=db, ost_data=ost_in)


@router.get("/", response_model=List[OSTOut])
def listar_osts(
    estado: Optional[str] = None,
    placa: Optional[str] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return ost_service.obtener_osts(
        db=db,
        estado=estado,
        placa=placa,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        skip=skip,
        limit=limit
    )


@router.get("/dashboard/stats")
def obtener_stats(db: Session = Depends(get_db)):
    return ost_service.obtener_estadisticas_dashboard(db=db)


@router.get("/{ost_id}", response_model=OSTOut)
def ver_ost(ost_id: int, db: Session = Depends(get_db)):
    return ost_service.obtener_ost_por_id(db=db, ost_id=ost_id)


@router.get("/codigo/{codigo}", response_model=OSTOut)
def ver_ost_por_codigo(codigo: str, db: Session = Depends(get_db)):
    return ost_service.obtener_ost_por_codigo(db=db, codigo=codigo)
