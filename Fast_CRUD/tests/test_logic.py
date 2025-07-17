from app.schemas import TaskCreate
from app import models

def test_create_and_update_transaction():
    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.crud import create_and_update_task_in_transaction

    db: Session = SessionLocal()
    task = TaskCreate(title="Transactional Task", description="initial")
    updated_task = create_and_update_task_in_transaction(db, task, "updated inside tx")
    assert updated_task.description == "updated inside tx"
    db.close()
