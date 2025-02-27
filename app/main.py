from fastapi import FastAPI
from mangum import Mangum
from app.routers import tasks
from app.auth import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="To-Do List API",
    description="Gerencie suas tarefas na nuvem com AWS DynamoDB!",
    version="1.0.0",
)

# 🔹 Configurar CORS no FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens (ideal para testes)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
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
