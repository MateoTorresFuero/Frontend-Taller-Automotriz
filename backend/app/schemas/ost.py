from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.cliente import ClienteOut


class OSTCreate(BaseModel):
    cliente_id: int
    placa: str = Field(
        ...,
        pattern=r"^[a-zA-Z][a-zA-Z0-9]{2}-[0-9]{3}$",
        description="Placa vehicular peruana en formato ABC-123",
    )
    marca: str
    modelo: str
    falla_reportada: str


class OSTOut(BaseModel):
    id: int
    codigo: str
    estado: str
    cliente_id: int
    placa: str
    marca: str
    modelo: str
    falla_reportada: str
    fecha_ingreso: datetime
    fecha_cierre: Optional[datetime] = None
    cliente: ClienteOut
    tecnicos_asignados: list = []

    class Config:
        from_attributes = True
