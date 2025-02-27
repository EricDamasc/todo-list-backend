import os
from dotenv import load_dotenv

load_dotenv()

# Configurações de Segurança
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
