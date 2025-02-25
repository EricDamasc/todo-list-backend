from fastapi import FastAPI
from mangum import Mangum
from app.routers import tasks
from app.auth import auth
from app.database.database import engine, Base
from fastapi.openapi.utils import get_openapi

# Criar tabelas no banco ao iniciar o app
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do List API",
    description="Gerencie suas tarefas na nuvem com AWS!",
    version="1.0.0",
)

# Função para modificar o Swagger com o BearerToken
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="To-Do List API",
        version="1.0.0",
        description="Gerencie suas tarefas na nuvem com AWS!",
        routes=app.routes,
    )
    # Configuração do Swagger UI para usar o Bearer Token
    security_scheme = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["components"]["securitySchemes"] = security_scheme
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Adicionando a customização no app
app.openapi = custom_openapi


# Rota inicial
@app.get("/", tags=["Home"])
def root():
    return {"message": "Bem-vindo à API de Tarefas!"}

# Adicionar rotas
app.include_router(auth.router, prefix="/api", tags=["Autenticação"])
app.include_router(tasks.router, prefix="/api", tags=["Tarefas"])

# Handler para AWS Lambda
handler = Mangum(app)
