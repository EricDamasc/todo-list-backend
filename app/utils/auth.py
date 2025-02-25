from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta")
ALGORITHM = "HS256"

# Esquema HTTP Bearer (usado para autenticar endpoints)
bearer_scheme = HTTPBearer()

# Função para verificar se o token é válido
def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    print(f"Token recebido: {token}") 
    credentials = token.credentials
    try:
        # Tentando decodificar o token
        payload = jwt.decode(credentials, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload decodificado: {payload}")  # Verifique se está imprimindo o payload
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        # Verificando se o usuário existe no banco de dados
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return user  # Retorna o objeto User
    except JWTError as e:
        print(f"Erro ao decodificar o token: {e}") 
        raise HTTPException(status_code=401, detail="Token inválido")
