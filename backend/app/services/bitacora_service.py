from typing import Optional
from app.core.mongodb import mongo_db
from app.schemas.bitacora import BitacoraCreate
from bson import ObjectId
import datetime
from fastapi import HTTPException, status

def crear_bitacora(db, bitacora_data: BitacoraCreate):
    doc = {
        "problema": bitacora_data.problema,
        "solucion": bitacora_data.solucion,
        "created_at": datetime.datetime.now(datetime.UTC)
    }
    result = mongo_db.bitacora.insert_one(doc)
    return {
        "id": str(result.inserted_id),
        "problema": doc["problema"],
        "solucion": doc["solucion"],
        "created_at": doc["created_at"]
    }

def obtener_bitacoras(
    db,
    busqueda: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
):
    query = {}
    if busqueda:
        query = {
            "$or": [
                {"problema": {"$regex": busqueda, "$options": "i"}},
                {"solucion": {"$regex": busqueda, "$options": "i"}}
            ]
        }
    cursor = mongo_db.bitacora.find(query).sort("created_at", -1).skip(skip).limit(limit)
    results = []
    for doc in cursor:
        results.append({
            "id": str(doc["_id"]),
            "problema": doc["problema"],
            "solucion": doc["solucion"],
            "created_at": doc.get("created_at")
        })
    return results

def obtener_bitacora_por_id(db, bitacora_id: str):
    try:
        doc = mongo_db.bitacora.find_one({"_id": ObjectId(bitacora_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de bitácora no válido"
        )
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de bitácora no encontrado"
        )
    return {
        "id": str(doc["_id"]),
        "problema": doc["problema"],
        "solucion": doc["solucion"],
        "created_at": doc.get("created_at")
    }
