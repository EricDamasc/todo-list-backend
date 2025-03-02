import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from datetime import datetime
from app.database.database import task_table
from app.schemas.task import TaskCreate, TaskResponse
from dotenv import load_dotenv
from app.utils.auth import get_current_user

load_dotenv()

router = APIRouter()

# Configuração do logger
logger = logging.getLogger(__name__)

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(user: dict = Depends(get_current_user)):
    user_id = user["username"]
    logger.info(f"Fetching tasks for user {user_id}")
    response = task_table.query(
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": user_id}
    )

    if "Items" not in response or not response["Items"]:
        logger.warning(f"Nenhuma tarefa encontrada para o usuário {user_id}")
        raise HTTPException(status_code=200, detail="Nenhuma tarefa encontrada")
    
    elif response['Items'] == []:
        logger.warning(f"Nenhuma tarefa encontrada para o usuário {user_id}")
        return response['Items']

    logger.info(f"Tarefas encontradas para o usuário")
    return response["Items"]

@router.post("/tasks", response_model=List[TaskResponse])
def create_tasks(tasks: List[TaskCreate], user: dict = Depends(get_current_user)):
    user_id = user["username"]
    created_tasks = []

    for task in tasks:
        task_id = str(uuid.uuid4())
        item = {
            "user_id": user_id,
            "task_id": task_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "due_date": task.due_date,
            "priority": task.priority.value,
            "created_at": datetime.now().isoformat()
        }
        task_table.put_item(Item=item)
        created_tasks.append(item)
        logger.info(f"Tarefa {task_id} criada para o usuário {user_id}")

    return created_tasks

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, updated_task: TaskCreate, user: dict = Depends(get_current_user)):
    user_id = user["username"]
    logger.info(f"Atualizando tarefa {task_id} para o usuário {user_id}")
    response = task_table.update_item(
        Key={"user_id": user_id, "task_id": task_id},
        UpdateExpression="SET title=:t, description=:d, completed=:c, due_date=:du, priority=:p",
        ExpressionAttributeValues={
            ":t": updated_task.title,
            ":d": updated_task.description,
            ":c": updated_task.completed,
            ":du": updated_task.due_date,
            ":p": updated_task.priority.value
        },
        ReturnValues="ALL_NEW"
    )

    if "Attributes" not in response:
        logger.warning(f"Tarefa {task_id} não encontrada para o usuário {user_id}")
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    logger.info(f"Tarefa {task_id} atualizada para o usuário {user_id}")
    return response["Attributes"]

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: str, user: dict = Depends(get_current_user)):
    user_id = user["username"]
    logger.info(f"Deleta tarefa {task_id} para o usuário {user_id}")
    response = task_table.delete_item(
        Key={"user_id": user_id, "task_id": task_id},
        ReturnValues="ALL_OLD"
    )

    if "Attributes" not in response:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    logger.info(f"Tarefa {task_id} deletada para o usuário {user_id}")
    return {"message": "Tarefa removida com sucesso"}