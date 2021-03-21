from typing import List
from fastapi import FastAPI, Depends, HTTPException, Response, status
import crud
import schemas
import database
from sqlalchemy.orm import Session

database.Base.metadata.create_all(database.engine)

app = FastAPI()

def get_session():
    session = database.SessionLocal()
    try:
        yield session
    finally:
        session.close()

# базовая точка входа
@app.get('/')
async def root():
    return {'msg': "Welcome to the ToDoApp API"}

# CRUD для задач 
@app.get('/task/', response_model = List[schemas.tasks.Task])
async def get_all_tasks(session: Session = Depends(get_session)):
    return crud.tasks.get_all_tasks(session)

@app.get('/task/{task_id}', response_model=schemas.tasks.Task)
async def get_task(task_id: int, response: Response, session: Session = Depends(get_session)):
    task = crud.tasks.get_task(task_id, session)
    if task is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return schemas.tasks.Task.from_orm(task)

@app.post('/task/', response_model=schemas.tasks.Task)
async def create_task(task: schemas.tasks.TaskCreate, response: Response, session: Session = Depends(get_session)):
    response.status_code = status.HTTP_201_CREATED
    return crud.tasks.create_task(task, session)

@app.put('/task/{task_id}')
async def update_task(task: schemas.tasks.TaskUpdate, task_id: int, session: Session = Depends(get_session)):
    return crud.tasks.update_task(task, task_id, session)

@app.delete('/task/{task_id}')
async def delete_task(task_id: int, response: Response, session: Session = Depends(get_session)):
    crud.tasks.delete_task(task_id, session)
    response.status_code = status.HTTP_204_NO_CONTENT
