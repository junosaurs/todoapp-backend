from typing import List
from fastapi import FastAPI, Depends, HTTPException, Response, status
import crud
import schemas
import database

database.Base.metadata.create_all(database.engine)

app = FastAPI()

# базовая точка входа
@app.get('/')
async def root():
    return {'msg': "Welcome to the ToDoApp API"}

# CRUD для задач 
@app.get('/task/', response_model = List[schemas.tasks.Task])
async def get_all_tasks():
    return crud.tasks.get_all_tasks(database.session)

@app.get('/task/{task_id}', response_model=schemas.tasks.Task)
async def get_task(task_id: int, response: Response):
    task = crud.tasks.get_task(task_id, database.session)
    if task is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return schemas.tasks.Task.from_orm(task)

@app.post('/task/', response_model=schemas.tasks.Task)
async def create_task(task: schemas.tasks.TaskCreate, response: Response):
    response.status_code = status.HTTP_201_CREATED
    return crud.tasks.create_task(task, database.session)

@app.put('/task/{task_id}')
async def update_task(task: schemas.tasks.TaskUpdate, task_id: int):
    return crud.tasks.update_task(task, task_id, database.session)

@app.delete('/task/{task_id}')
async def delete_task(task_id: int, response: Response):
    crud.tasks.delete_task(task_id, database.session)
    response.status_code = status.HTTP_204_NO_CONTENT
