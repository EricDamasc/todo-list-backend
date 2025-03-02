from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.routers import tasks
from app.auth import auth

app = FastAPI(
    title="To-Do List API",
    description="Gerencie suas tarefas na nuvem com AWS DynamoDB!",
    version="1.0.0",
)

# Configurar CORS corretamente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "https://kloc449ejb.execute-api.us-east-1.amazonaws.com"],  # Substitua pelo frontend real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar uma rota OPTIONS manualmente
@app.options("/{path:path}")
async def preflight_request():
    return {
        "message": "Preflight request successful"
    }

# Rota inicial
@app.get("/", tags=["Home"])
def root():
    return {"message": "Bem-vindo à API de Tarefas!"}

# Adicionar rotas
app.include_router(auth.router, prefix="/api", tags=["Autenticação"])
app.include_router(tasks.router, prefix="/api", tags=["Tarefas"])

# Handler para AWS Lambda
handler = Mangum(app)
