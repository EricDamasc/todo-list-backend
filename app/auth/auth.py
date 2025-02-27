from fastapi import APIRouter, HTTPException, Depends
from app.database.database import get_user_table
from app.schemas.auth import UserRegister, UserLogin, Token
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Expira em 60 minutos

router = APIRouter()

# Função para criar hash da senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 Rota de registro de usuário (sem hash de senha e com username)
@router.post("/register", response_model=Token)
def register(user: UserRegister, db = Depends(get_user_table)):
    # Verifica se o username já está cadastrado no DynamoDB
    response = db.get_item(Key={"email": user.email})
    if "Item" in response:
        raise HTTPException(status_code=400, detail="Username já cadastrado")

    # Criar novo usuário no DynamoDB
    new_user = {
        "email": user.email,
        "password": user.password
    }
    db.put_item(Item=new_user)

    # Gerar token JWT para login automático após registro
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# Rota de login de usuário
@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db = Depends(get_user_table)):
    response = db.get_item(Key={"email": user_data.email})
    user = response.get("Item")

    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}
