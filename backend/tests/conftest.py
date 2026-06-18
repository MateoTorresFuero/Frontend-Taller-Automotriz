import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app
from app.models.catalogos import TipoDocumento, Sexo
from app.models.usuario import Rol, Usuario
from app.models.persona import Persona
from app.core.security import get_password_hash, create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Configura la DB en memoria vacía antes de cada test e inserta catálogos base."""
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        #  Catálogos Base
        db.add_all(
            [
                Sexo(codigo="M", descripcion="Masculino"),
                Sexo(codigo="F", descripcion="Femenino"),
                TipoDocumento(
                    codigo="DNI", descripcion="Documento Nacional de Identidad"
                ),
                Rol(codigo="ADMIN", descripcion="Administrador del Sistema"),
                Rol(codigo="RECEPCION", descripcion="Recepcionista"),
            ]
        )
        db.commit()

        # Usuario de Prueba (admin)
        persona_admin = Persona(
            tipo_documento_id=1,
            numero_documento="00000000",
            nombres="Admin",
            apellido_paterno="Test",
            apellido_materno="",
            sexo_id=1,
        )
        db.add(persona_admin)
        db.commit()
        db.refresh(persona_admin)

        usuario_admin = Usuario(
            email="test@taller.com",
            password_hash=get_password_hash("testpassword"),
            persona_id=persona_admin.id,
            rol_id=1,
        )
        db.add(usuario_admin)
        db.commit()
    finally:
        db.close()

    yield  # Aquí se ejecuta el test

    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """Cliente HTTP sin autenticar"""
    return TestClient(app)


@pytest.fixture
def db():
    """Sesión de Base de Datos temporal"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user_data():
    """Credenciales del usuario generado en la base de datos temporal"""
    return {"email": "test@taller.com", "password": "testpassword"}


@pytest.fixture
def authorized_client(client, test_user_data):
    """Cliente HTTP ya autenticado (contiene el token JWT en las cabeceras)"""
    token = create_access_token(subject=test_user_data["email"])
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
