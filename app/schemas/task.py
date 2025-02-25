from pydantic import BaseModel
from datetime import datetime
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
    due_date: datetime
    priority: PriorityEnum

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int

    class Config:
        orm_mode = True
