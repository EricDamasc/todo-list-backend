from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from datetime import datetime
from app.database.database import task_table
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter()

# 🔹 Obter todas as tarefas (sem filtro por usuário)
@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    response = task_table.scan()  # Retorna todos os itens da tabela
    return response.get("Items", [])  # Retorna a lista de tarefas

# 🔹 Criar múltiplas tarefas
@router.post("/tasks", response_model=List[TaskResponse])
def create_tasks(tasks: List[TaskCreate], user_id: str):
    created_tasks = []

    for task in tasks:
        task_id = str(uuid.uuid4())  # Gerar um UUID para cada tarefa
        item = {
            "user_id": user_id,
            "task_id": task_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "due_date": task.due_date,
            "priority": task.priority.value,  # Convertendo Enum para string
            "created_at": datetime.utcnow().isoformat(),
        }
        task_table.put_item(Item=item)
        created_tasks.append(item)

    return created_tasks

# 🔹 Atualizar uma tarefa pelo ID
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, user_id: str, updated_task: TaskCreate):
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

# 🔹 Deletar uma tarefa pelo ID
@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: str, user_id: str):
    response = task_table.delete_item(
        Key={"user_id": user_id, "task_id": task_id},
        ReturnValues="ALL_OLD"
    )

    if "Attributes" not in response:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {"message": "Tarefa removida com sucesso"}
