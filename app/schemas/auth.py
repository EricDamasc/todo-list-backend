from pydantic import BaseModel, EmailStr

# 🔹 Esquema para registro de usuário
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    username: str

# 🔹 Esquema para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 🔹 Esquema para resposta com token JWT
class Token(BaseModel):
    access_token: str
    token_type: str
