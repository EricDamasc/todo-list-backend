from pydantic import BaseModel
from enum import Enum
from typing import Optional

class PriorityEnum(str, Enum):
    baixa = "baixa"
    media = "média"
    alta = "alta"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: str
    priority: PriorityEnum
    creadted_at: str

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    task_id: str
    user_id: str

    class Config:
        orm_mode = True
