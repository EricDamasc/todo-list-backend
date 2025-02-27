from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class PriorityEnum(str, Enum):
    baixa = "baixa"
    media = "média"
    alta = "alta"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: str  # 🔹 Alterado para string ISO 8601
    priority: PriorityEnum

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    task_id: str  # 🔹 Alterado para string, já que não há Integers no DynamoDB
    user_id: str  # 🔹 Adicionado, pois DynamoDB precisa de chave de partição

    class Config:
        orm_mode = True
