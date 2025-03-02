from fastapi import APIRouter, HTTPException, Depends
from app.database.database import get_user_table
from app.schemas.auth import UserRegister, UserLogin, Token
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=Token)
def register(user: UserRegister, db = Depends(get_user_table)):
    response = db.get_item(Key={"email": user.email})
    if "Item" in response:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    new_user = {
        "email": user.email,
        "password": user.password,
        "username": user.username
    }
    db.put_item(Item=new_user)

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db = Depends(get_user_table)):
    response = db.get_item(Key={"email": user_data.email})
    user = response.get("Item")

    if not user or user_data.password != user["password"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token({"sub": user["email"], "username": user["username"]})
    return {"access_token": token, "token_type": "bearer"}