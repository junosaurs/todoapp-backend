# for test purposes only!
from schemas import Task, TaskCreate
from models import TaskObj
import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

def get_all_tasks(session: Session):
    rows = session.query(TaskObj).all()
    return rows

def get_task(task_id: int, session: Session):
    task = session.query(TaskObj).filter(TaskObj.id == task_id).scalar()
    return task

def create_task(task: TaskCreate, session: Session):
    new_task = TaskObj(title=task.title, description=task.description, end_date=task.end_date)
    session.add(new_task)
    session.flush()
    session.commit()
    return new_task

def update_task(task, task_id, session: Session):
    task_for_update = session.query(TaskObj).filter(TaskObj.id == task_id).scalar()
    for var, value in vars(task).items():
        setattr(task_for_update, var, value) if value else None
    session.add(task_for_update)
    session.commit()
    session.refresh(task_for_update)
    return task_for_update

def delete_task(task_id: int, session: Session):
    task = session.query(TaskObj).filter(TaskObj.id == task_id).first()
    if task is not None:
        session.delete(task)
        session.commit()