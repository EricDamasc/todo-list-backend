from fastapi import FastAPI
from mangum import Mangum
from app.routers import tasks
from app.auth import auth
from app.database.database import engine, Base

# Criar tabelas no banco ao iniciar o app
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do List API",
    description="Gerencie suas tarefas na nuvem com AWS!",
    version="1.0.0",
)

# Rota inicial
@app.get("/", tags=["Home"])
def root():
    return {"message": "Bem-vindo à API de Tarefas!"}

# Adicionar rotas
app.include_router(auth.router, prefix="/api", tags=["Autenticação"])
app.include_router(tasks.router, prefix="/api", tags=["Tarefas"])

# Handler para AWS Lambda
handler = Mangum(app)
