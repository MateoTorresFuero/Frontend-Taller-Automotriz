from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status
from app.models.ost import OST
from app.models.cliente import Cliente
from app.schemas.ost import OSTCreate


def generar_codigo_ost(db: Session) -> str:
    """Genera un código correlativo secuencial para la OST."""
    count = db.query(OST).count()
    return f"OST-{count + 1:06d}"


def crear_ost(db: Session, ost_data: OSTCreate) -> OST:
    cliente = db.query(Cliente).filter(Cliente.id == ost_data.cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente especificado no existe"
        )

    nueva_ost = OST(
        codigo=generar_codigo_ost(db),
        cliente_id=ost_data.cliente_id,
        placa=ost_data.placa.upper(),
        marca=ost_data.marca,
        modelo=ost_data.modelo,
        falla_reportada=ost_data.falla_reportada,
        estado="PENDIENTE"
    )

    db.add(nueva_ost)
    db.commit()
    db.refresh(nueva_ost)
    return nueva_ost


def obtener_osts(
    db: Session,
    estado: Optional[str] = None,
    placa: Optional[str] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 20
):
    query = db.query(OST)

    if estado:
        query = query.filter(OST.estado == estado.upper())

    if placa:
        query = query.filter(OST.placa.contains(placa.upper()))

    if fecha_desde:
        query = query.filter(OST.fecha_ingreso >= fecha_desde)

    if fecha_hasta:
        query = query.filter(OST.fecha_ingreso <= fecha_hasta)

    return query.order_by(OST.fecha_ingreso.desc()).offset(skip).limit(limit).all()


def obtener_ost_por_id(db: Session, ost_id: int) -> OST:
    ost = db.query(OST).filter(OST.id == ost_id).first()
    if not ost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La orden de servicio técnico no existe"
        )
    return ost


def obtener_ost_por_codigo(db: Session, codigo: str) -> OST:
    ost = db.query(OST).filter(OST.codigo == codigo.upper()).first()
    if not ost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La orden de servicio técnico no existe"
        )
    return ost


def obtener_estadisticas_dashboard(db: Session):
    total_osts = db.query(OST).count()
    total_clientes = db.query(Cliente).count()
    
    # Agregación de OSTs por Estado
    stats_estado = (
        db.query(OST.estado, func.count(OST.id).label("cantidad"))
        .group_by(OST.estado)
        .all()
    )
    osts_por_estado = [{"estado": row.estado, "cantidad": row.cantidad} for row in stats_estado]
    
    # Agregación de OSTs por Marca (Top 5)
    stats_marca = (
        db.query(OST.marca, func.count(OST.id).label("cantidad"))
        .group_by(OST.marca)
        .order_by(func.count(OST.id).desc())
        .limit(5)
        .all()
    )
    osts_por_marca = [{"marca": row.marca, "cantidad": row.cantidad} for row in stats_marca]
    
    return {
        "resumen": {
            "total_clientes": total_clientes,
            "total_osts": total_osts
        },
        "osts_por_estado": osts_por_estado,
        "osts_por_marca": osts_por_marca
    }
