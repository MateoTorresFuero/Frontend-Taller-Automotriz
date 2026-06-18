from sqlalchemy.schema import CreateTable
from app.core.database import engine, Base
import app.models

with open("../database/taller_db_schema.sql", "w") as f:
    for table in Base.metadata.sorted_tables:
        f.write(str(CreateTable(table).compile(engine)).strip() + ";\n\n")

print("Schema generated successfully.")
