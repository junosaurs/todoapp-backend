from typing import List
from fastapi import FastAPI, Depends, HTTPException, Response, status
import crud
import schemas
from database.session import SessionLocal, engine
from database.base_class import Base
from sqlalchemy.orm import Session, sessionmaker

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()
Base.metadata.create_all(engine)

# базовая точка входа
@app.get('/')
async def root():
    return {'msg': "Welcome to the ToDoApp API"}

# CRUD для задач 
@app.get('/task/', response_model = List[schemas.tasks.TaskReadSchema])
async def get_all_tasks(session: Session = Depends(get_session)):
    return crud.task.get_all_tasks(session)

@app.get('/task/{task_id}', response_model=schemas.tasks.TaskReadSchema)
async def get_task(task_id: int, response: Response, session: Session = Depends(get_session)):
    task = crud.task.get_task(task_id, session)
    if task is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return schemas.tasks.TaskReadSchema.from_orm(task)

@app.post('/task/', response_model=schemas.tasks.TaskReadSchema)
async def create_task(task: schemas.tasks.TaskCreateSchema, response: Response, session: Session = Depends(get_session)):
    response.status_code = status.HTTP_201_CREATED
    return crud.task.create_task(task, session)

@app.put('/task/{task_id}')
async def update_task(task: schemas.tasks.TaskUpdateSchema, task_id: int,  response: Response, session: Session = Depends(get_session)):
    update_task = crud.task.update_task(task, task_id, session)
    if update_task.id != task_id:
        response.status_code = status.HTTP_201_CREATED
        return update_task

@app.delete('/task/{task_id}')
async def delete_task(task_id: int, response: Response, session: Session = Depends(get_session)):
    crud.task.delete_task(task_id, session)
    response.status_code = status.HTTP_204_NO_CONTENT
