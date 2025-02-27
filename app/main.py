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
    allow_origins=["http://localhost:4200"],  # URL do frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os headers
)

@app.options("/{path:path}")
async def preflight_request(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:4200"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# 🔹 Rota inicial
@app.get("/", tags=["Home"])
def root():
    return {"message": "Bem-vindo à API de Tarefas!"}

# 🔹 Adicionar rotas
app.include_router(auth.router, prefix="/api", tags=["Autenticação"])
app.include_router(tasks.router, prefix="/api", tags=["Tarefas"])

# 🔹 Handler para AWS Lambda
handler = Mangum(app)
