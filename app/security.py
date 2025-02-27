import os
import boto3
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Configuração do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token válido por 60 minutos

# Configuração de hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do DynamoDB
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
users_table = dynamodb.Table("Users")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
bearer_scheme = HTTPBearer()

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

# Função para obter usuário do DynamoDB
def get_user_from_dynamodb(email: str):
    response = users_table.get_item(Key={"email": email})
    return response.get("Item")

# Função para obter usuário autenticado
def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials = token.credentials
    payload = verify_jwt_token(credentials)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
    email = payload.get("sub")
    user = get_user_from_dynamodb(email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return user
