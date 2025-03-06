import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.routers import tasks
from app.auth import auth
from watchtower import CloudWatchLogHandler

# Configuração do logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuração do CloudWatch
cloudwatch_handler = CloudWatchLogHandler(
    log_group=os.getenv("CLOUDWATCH_LOG_GROUP", "todo-list-backend-logs"),)
logger.addHandler(cloudwatch_handler)

app = FastAPI(
    title="To-Do List API",
    description="Gerencie suas tarefas na nuvem com AWS DynamoDB!",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "https://kloc449ejb.execute-api.us-east-1.amazonaws.com", "http://todo-list-angular-app.s3-website-us-east-1.amazonaws.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.options("/{path:path}")
async def preflight_request():
    logger.info("Preflight request received")
    print("Preflight request received")
    return {
        "message": "Preflight request successful"
    }


@app.get("/", tags=["Home"])
def root():
    logger.info("Root endpoint accessed")
    print("Root endpoint accessed")
    return {"message": "Bem-vindo à API de Tarefas!"}


app.include_router(auth.router, prefix="/api", tags=["Autenticação"])
app.include_router(tasks.router, prefix="/api", tags=["Tarefas"])

handler = Mangum(app)
