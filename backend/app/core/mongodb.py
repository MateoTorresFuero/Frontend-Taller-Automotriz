from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_URL)
# Extrae el nombre de la base de datos de la URL o usa 'taller_db' como fallback
db_name = settings.MONGO_URL.split("/")[-1].split("?")[0] or "taller_db"
mongo_db = client[db_name]
