import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Verifica se a URL do banco foi carregada corretamente
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Erro: A variável de ambiente DATABASE_URL não foi encontrada!")

# Criar engine do banco PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Evita falha em conexões inativas
    pool_size=5,         # Número máximo de conexões (ajuste conforme necessário)
    max_overflow=10,     # Conexões extras se necessário
)

# Criar sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar base para os modelos
Base = declarative_base()

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
