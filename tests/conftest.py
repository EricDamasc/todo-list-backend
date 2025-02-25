import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Definir um valor padrão para a variável de ambiente DATABASE_URL
DATABASE_URL = "sqlite:///:memory:"

from app.database.database import get_db, Base
from app.main import app

# Criar um banco de dados de testes (SQLite em memória)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar uma fixture para o banco de testes
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)  # Criar as tabelas no banco de testes
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Apagar as tabelas após o teste

# Criar uma fixture para o cliente de teste do FastAPI
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c