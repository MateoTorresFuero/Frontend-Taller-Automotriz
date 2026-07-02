from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.bitacora import BitacoraCreate, BitacoraOut
from app.services import bitacora_service

router = APIRouter()


@router.post("/", response_model=BitacoraOut, status_code=status.HTTP_201_CREATED)
def registrar_bitacora(bitacora_in: BitacoraCreate, db: Session = Depends(get_db)):
    return bitacora_service.crear_bitacora(db=db, bitacora_data=bitacora_in)


@router.get("/", response_model=List[BitacoraOut])
def listar_bitacoras(
    busqueda: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return bitacora_service.obtener_bitacoras(
        db=db,
        busqueda=busqueda,
        skip=skip,
        limit=limit
    )


@router.get("/{bitacora_id}", response_model=BitacoraOut)
def ver_bitacora(bitacora_id: str, db: Session = Depends(get_db)):
    return bitacora_service.obtener_bitacora_por_id(db=db, bitacora_id=bitacora_id)
