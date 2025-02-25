from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse
from app.utils.auth import get_current_user

router = APIRouter()

# 🔹 Obter todas as tarefas (Protegida com JWT)
@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Task).all()

# 🔹 Criar uma nova tarefa (Protegida com JWT)
@router.post("/tasks", response_model=List[TaskResponse])
def create_tasks(tasks: List[TaskCreate], db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_tasks = [Task(**task.dict()) for task in tasks]
    db.add_all(db_tasks)
    db.commit()
    for task in db_tasks:
        db.refresh(task)
    return db_tasks

# 🔹 Atualizar uma tarefa pelo ID (Protegida com JWT)
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    for key, value in updated_task.dict().items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

# 🔹 Deletar uma tarefa pelo ID (Protegida com JWT)
@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(task)
    db.commit()
    return {"message": "Tarefa removida com sucesso"}
