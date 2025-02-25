from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.auth import UserLogin, Token
from app.models.user import User
from app.auth.auth import verify_password, create_jwt_token

router = APIRouter()

# 🔹 Rota de login (Retorna JWT)
@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_jwt_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
