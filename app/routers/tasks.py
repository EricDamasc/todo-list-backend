from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter()


# 🔹 Obter todas as tarefas
@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


# 🔹 Criar uma nova tarefa
@router.post("/tasks", response_model=List[TaskResponse])
def create_tasks(tasks: List[TaskCreate], db: Session = Depends(get_db)):
    db_tasks = [Task(**task.dict()) for task in tasks]
    db.add_all(db_tasks)
    db.commit()
    for task in db_tasks:
        db.refresh(task)
    return db_tasks

# 🔹 Atualizar uma tarefa pelo ID
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    # Atualizando os campos da tarefa
    for key, value in updated_task.dict().items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


# 🔹 Deletar uma tarefa pelo ID
@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(task)
    db.commit()
    return {"message": "Tarefa removida com sucesso"}
