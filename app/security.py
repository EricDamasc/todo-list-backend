from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from pytest import Session

from app.database.database import get_db
from app.models.user import User

# Carregar variáveis do .env
load_dotenv()

# Configuração do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta")  # Troque por uma chave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token válido por 60 minutos

# Configuração de hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar um token JWT
def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Função para verificar token JWT
def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Função para hash de senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Função para obter o usuário autenticado
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_jwt_token(token)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    user = db.query(User).filter(User.email == payload["sub"]).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user