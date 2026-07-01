from pydantic import BaseModel
from datetime import datetime


class BitacoraCreate(BaseModel):
    problema: str
    solucion: str


class BitacoraOut(BaseModel):
    id: str
    problema: str
    solucion: str
    created_at: datetime

    class Config:
        from_attributes = True
