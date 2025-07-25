from sqlalchemy.orm import Session
from . import models, schemas

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 10, keyword: str = None):
    query = db.query(models.Task)
    if keyword:
        query = query.filter(models.Task.title.contains(keyword))
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def create_and_update_task_in_transaction(db: Session, task: schemas.TaskCreate, update_desc: str):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.flush()
    new_task.description = update_desc
    db.commit()
    db.refresh(new_task)
    return new_task
