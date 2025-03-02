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

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(user: dict = Depends(get_current_user)):
    user_id = user["username"]
    response = task_table.query(
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": user_id}
    )

    if "Items" not in response or not response["Items"]:
        raise HTTPException(status_code=404, detail="Nenhuma tarefa encontrada")

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
            "created_at": datetime.utcnow().isoformat(),
        }
        task_table.put_item(Item=item)
        created_tasks.append(item)

    return created_tasks

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, updated_task: TaskCreate, user: dict = Depends(get_current_user)):
    user_id = user["username"]
    response = task_table.update_item(
        Key={"user_id": user_id, "task_id": task_id},
        UpdateExpression="SET title=:t, description=:d, completed=:c, due_date=:du, priority=:p",
        ExpressionAttributeValues={
            ":t": updated_task.title,
            ":d": updated_task.description,
            ":c": updated_task.completed,
            ":du": updated_task.due_date,
            ":p": updated_task.priority.value,
        },
        ReturnValues="ALL_NEW"
    )

    if "Attributes" not in response:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return response["Attributes"]

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: str, user: dict = Depends(get_current_user)):
    user_id = user["username"]
    response = task_table.delete_item(
        Key={"user_id": user_id, "task_id": task_id},
        ReturnValues="ALL_OLD"
    )

    if "Attributes" not in response:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {"message": "Tarefa removida com sucesso"}