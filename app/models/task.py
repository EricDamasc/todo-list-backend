from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from datetime import datetime
from app.database.database import Base
import enum

class PriorityEnum(str, enum.Enum):
    baixa = "baixa"
    media = "média"
    alta = "alta"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime, default=lambda: datetime.utcnow())  # 🔹 Corrigido
    priority = Column(Enum(PriorityEnum, native_enum=False), default=PriorityEnum.media)  # 🔹 Melhor compatibilidade
