from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import auth
from app.database import get_db  # Corrigido
from app.schemas import task  # Corrigido
from app.models import task  # Corrigido

router = APIRouter()


@router.post("/")
def create_user(user: task.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Args:
        user (schemas.TaskCreate): The user data to create a new user.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        models.User: The newly created user.
    """
    hashed_password = auth.hash_password(user.password)
    db_user = task.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
