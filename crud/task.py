from schemas import TaskCreateSchema, TaskReadSchema, TaskUpdateSchema
from models import Task
import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

def get_all_tasks(session: Session):
    rows = session.query(Task).order_by(Task.start_date).all()
    return rows

def get_task(task_id: int, session: Session):
    task = session.query(Task).filter(Task.id == task_id).scalar()
    return task

def create_task(task: TaskCreateSchema, session: Session):
    new_task = Task(title=task.title, description=task.description, end_date=task.end_date)
    session.add(new_task)
    session.flush()
    session.commit()
    return new_task

def update_task(task: TaskUpdateSchema, task_id, session: Session):
    task_for_update = session.query(Task).filter(Task.id == task_id).scalar()
    if task_for_update is None:
        task_for_update = Task(title=task.title, description=task.description, end_date=task.end_date, start_date=task.start_date, is_active=task.is_active)
    else:
        for var, value in vars(task).items():
            if value is not None:
                setattr(task_for_update, var, value)
    session.add(task_for_update)
    session.commit()
    session.refresh(task_for_update)
    return task_for_update

def delete_task(task_id: int, session: Session):
    task = session.query(Task).filter(Task.id == task_id).first()
    if task is not None:
        session.delete(task)
        session.commit()
