import logging
import os
import boto3
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta")
ALGORITHM = "HS256"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
users_table = dynamodb.Table("Users")

bearer_scheme = HTTPBearer()

# Configuração do logger
logger = logging.getLogger(__name__)

def get_user_from_dynamodb(email: str):
    logger.info(f"Buscando usuário {email} no DynamoDB")
    response = users_table.get_item(Key={"email": email})
    return response.get("Item")

def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials = token.credentials
    try:
        payload = jwt.decode(credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            logger.warning("Token inválido: sub não encontrado")
            raise HTTPException(status_code=401, detail="Token inválido")
        user = get_user_from_dynamodb(email)
        if not user:
            logger.warning(f"Usuário {email} não encontrado")
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        logger.info(f"Usuário {email} autenticado com sucesso")
        return user
    except JWTError:
        logger.warning("Token inválido ou expirado")
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")