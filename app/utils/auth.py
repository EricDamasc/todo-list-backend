import os
import boto3
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta")
ALGORITHM = "HS256"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
users_table = dynamodb.Table("Users")

# Esquema HTTP Bearer para autenticação
bearer_scheme = HTTPBearer()

# Função para obter usuário do DynamoDB
def get_user_from_dynamodb(email: str):
    response = users_table.get_item(Key={"email": email})
    return response.get("Item")

# Função para verificar se o token é válido
def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials = token.credentials
    try:
        payload = jwt.decode(credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        user = get_user_from_dynamodb(email)
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return user  # Retorna o objeto User do DynamoDB
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
