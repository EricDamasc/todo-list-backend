import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do Banco de Dados (RDS PostgreSQL)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://AdminEricDamasc@todo-list-db.cpq2caosujiy.us-east-1.rds.amazonaws.com:5432/todo"
)

# Configurações de Segurança
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
