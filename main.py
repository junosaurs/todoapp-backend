from typing import List
from fastapi import FastAPI, Depends, HTTPException, Response, status
import crud_tasks
import schemas
import database


database.Base.metadata.create_all(database.engine)

app = FastAPI()

@app.get('/')
async def root():
    return {'msg': "Welcome to the ToDoApp API"}

# CRUD для задач 

# DONE
@app.get('/task/', response_model = List[schemas.Task])
async def get_all_tasks():
    tasks = crud_tasks.get_all_tasks(database.session)
    return tasks

#DONE
@app.get('/task/{task_id}', response_model=schemas.Task)
async def get_task(task_id: int, response: Response, ):
    task = crud_tasks.get_task(task_id, database.session)
    if task is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return schemas.Task.from_orm(task)

#DONE
@app.post('/task/', response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, response: Response):
    response.status_code = status.HTTP_201_CREATED
    return crud_tasks.create_task(task, database.session)


@app.put('/task/{task_id}')
async def update_task(task: schemas.TaskUpdate, task_id: int):
    return crud_tasks.update_task(task, task_id, database.session)

#DONE
@app.delete('/task/{task_id}')
async def delete_task(task_id: int, response: Response):
    crud_tasks.delete_task(task_id, database.session)
    response.status_code = status.HTTP_204_NO_CONTENT
