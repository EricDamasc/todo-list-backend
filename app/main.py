from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware  # 🔹 Importação necessária
from mangum import Mangum
from app.routers import tasks
from app.auth import auth

app = FastAPI(
    title="To-Do List API",
    description="Gerencie suas tarefas na nuvem com AWS DynamoDB!",
    version="1.0.0",
)

# 🔹 Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔹 Permite qualquer origem (mas sem credenciais)
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Rota inicial
@app.get("/", tags=["Home"])
def root():
    return {"message": "Bem-vindo à API de Tarefas!"}

# 🔹 Adicionar rotas
app.include_router(auth.router, prefix="/api", tags=["Autenticação"])
app.include_router(tasks.router, prefix="/api", tags=["Tarefas"])

# 🔹 Handler para AWS Lambda
handler = Mangum(app)
