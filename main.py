from typing import List
from fastapi import FastAPI, Depends, HTTPException, Response, status
import crud_tasks
import schemas

app = FastAPI()

@app.get('/')
async def root():
    return {'msg': "Welcome to the ToDoApp API"}

# CRUD для задач 

@app.get('/task/', response_model = List[schemas.Task])
async def get_all_tasks():
    tasks = crud_tasks.get_all_tasks()
    return tasks

@app.get('/task/{task_id}', response_model=schemas.Task)
async def get_task(task_id: int, response: Response):
    task = crud_tasks.get_task(task_id)
    if task is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    return task

@app.post('/task/')
async def create_task(task: schemas.TaskCreate, response: Response):
    response.status_code = status.HTTP_201_CREATED
    return crud_tasks.create_task(task)

@app.post('/task/{task_id}')
async def update_task(task: schemas.TaskUpdate):
    return crud_tasks.update_task(task)

@app.delete('/task/{task_id}')
async def delete_task(task_id: int):
    success = crud_tasks.delete_task(task_id)
    if success:
        return Response(status_code=204)