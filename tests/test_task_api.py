from fastapi.testclient import TestClient
from main import app, get_session
from database.base_class import Base
from pydantic import BaseSettings
from schemas.tasks import TaskCreateSchema, TaskReadSchema, TaskUpdateSchema
from models.tasks import Task
from .utils import create_task_random_data, create_task_random_data_create, random_string
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker
from config import test_settings
import pytest
import datetime
import functools
import json

DB_USERNAME="junosaurs"
DB_PASSWORD="junosaurs2021"
DB_NAME="tests" 

url = URL(
    drivername="postgresql",
    username=test_settings.DB_USERNAME,
    password=test_settings.DB_PASSWORD,
    host='localhost',
    port=5432,
    database=test_settings.DB_NAME
)
engine = create_engine(url)
Base.metadata.create_all(bind=engine)
TestSessionLocal = sessionmaker(bind=engine)

def get_test_session():
    try:
        session = TestSessionLocal()
        yield session
    finally:
        session.close()

app.dependency_overrides[get_session] = get_test_session

client = TestClient(app)

def setup_task_database_table():
    s = TestSessionLocal()
    # обычные таски
    for _ in range(3):
        s.add(create_task_random_data(is_active=True, with_end_date=False))
    # таски со сроком выполнения
    for _ in range(3):
        s.add(create_task_random_data(with_end_date=True))
    # выполненные таски
    for _ in range(3):
        s.add(create_task_random_data(is_active=False, with_end_date=False))
    s.commit()
    s.close()

def clear_task_database_table():
    s = TestSessionLocal()
    rows = s.query(Task).delete()
    s.commit()
    s.close()

def db_setup_fixture(need_setup=False, need_clear=True):
    def inner_function(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if need_setup:
                setup_task_database_table()
            try:
                func()
            finally:
                if need_clear:
                    clear_task_database_table()
        return wrapper
    return inner_function


@db_setup_fixture(need_setup=True)
def test_get_tasks():
    response = client.get("/task/")
    with TestSessionLocal() as s: 
        assert response.status_code == 200
        assert len(response.json()) == 9
        non_active_tasks = s.query(Task).filter(Task.is_active == False).all()
        assert len(non_active_tasks) == 3
        with_end_date_tasks = s.query(Task).filter(Task.end_date != None).all()
        for i in range(len(with_end_date_tasks)):
            print(with_end_date_tasks[i].end_date)
        assert len(with_end_date_tasks) == 3

@db_setup_fixture()
def test_get_tasks_empty_response():
    response = client.get("/task/")
    assert response.status_code == 200
    assert response.json() == []

@db_setup_fixture()
def test_get_task():
    s = TestSessionLocal()
    task = create_task_random_data(with_end_date=True, is_active=True)
    s.add(task)
    s.commit()

    response = client.get(f'/task/{task.id}')
    obj = response.json()
    assert response.status_code == 200
    assert task.id == obj.get("id")
    assert task.title == obj.get("title")
    assert task.description == obj.get("description")
    assert task.start_date == datetime.datetime.strptime(obj.get("start_date"), "%Y-%m-%dT%H:%M:%S.%f")
    assert task.end_date == datetime.datetime.strptime(obj.get("end_date"), "%Y-%m-%dT%H:%M:%S.%f")
    assert task.is_active == obj.get("is_active")

    s.delete(task)
    s.commit()

    response = client.get(f'/task/{task.id}')
    assert response.status_code == 404
    assert response.json() == None


@db_setup_fixture()
def test_create_task():
    s = TestSessionLocal()
    task = create_task_random_data_create(with_end_date=True, is_active=True)
    response = client.post('/task/', data=task.json())
    obj = response.json()
    # проверка на то, что возвращает метод
    assert response.status_code == 201
    assert "id" in obj
    assert task.title == obj.get("title")
    assert task.description == obj.get("description")
    assert "start_date" in obj
    assert task.end_date == datetime.datetime.strptime(obj.get("end_date"), "%Y-%m-%dT%H:%M:%S.%f")
    assert "is_active" in obj

    # проверка на то, что успешно записалось в БД
    db_response_obj = s.query(Task).filter(Task.id == obj["id"]).one()
    assert obj["id"] == db_response_obj.id
    assert task.title == db_response_obj.title
    assert task.description == db_response_obj.description
    assert datetime.datetime.strptime(obj.get("start_date"), "%Y-%m-%dT%H:%M:%S.%f") == db_response_obj.start_date
    assert datetime.datetime.strptime(obj.get("end_date"), "%Y-%m-%dT%H:%M:%S.%f") == db_response_obj.end_date
    assert task.end_date == db_response_obj.end_date
    assert obj["is_active"] == db_response_obj.is_active

    s.delete(db_response_obj)
    s.commit()
    # проверка на удаление из БД
    response = client.get(f'/task/{obj["id"]}')
    assert response.status_code == 404
    assert response.json() == None

@db_setup_fixture()
def test_create_task_not_enough_values():
    s = TestSessionLocal()
    task = create_task_random_data_create(with_end_date=True, is_active=True)
    del(task.title)
    response = client.post("/task/", data=task.json())
    assert response.status_code == 422
    assert s.query(Task).first() is None
    s.close()
    
@db_setup_fixture()
def test_create_task_invalid_data():
    s = TestSessionLocal()
    task = create_task_random_data_create(with_end_date=True, is_active=True)
    task.title = random_string(str_len=200, min_len=200)
    response = client.post("/task/", data=task.json())
    assert response.status_code == 422
    assert s.query(Task).first() is None

    task.description = random_string(str_len=2000, min_len=2000)
    assert response.status_code == 422
    assert s.query(Task).first() is None
    s.close()

@db_setup_fixture()
def test_update_task():
    s = TestSessionLocal()
    t = create_task_random_data(is_active=True, with_end_date=True)
    s.add(t)
    s.commit()
    task = s.query(Task).first()

    new_title = random_string(50)
    new_description = random_string(500)

    task.title = new_title
    task.description = new_description
    task.is_active = False
    updated_task = TaskUpdateSchema.from_orm(task)
    response = client.put(f"/task/{task.id}", data=updated_task.json())
    assert response.status_code == 200
    task = s.query(Task).filter(Task.id == task.id).first()

    assert task.title == new_title
    assert task.description == new_description
    assert task.is_active == False

    s.close()

@db_setup_fixture()
def test_update_task_not_in_db():
    s = TestSessionLocal()

    task = create_task_random_data(with_end_date=False, is_active=True)
    updated_task = TaskUpdateSchema.from_orm(task)
    response = client.put(f"/task/{10000}", data=updated_task.json())
    assert response.status_code == 201
    assert response.json().get("title") == task.title
    assert response.json().get("description") == task.description
    assert response.json().get("end_date") == None
    assert response.json().get("is_active") == task.is_active
    s.close()

@db_setup_fixture()
def test_update_task_invalid_data():
    s = TestSessionLocal()
    t = create_task_random_data(is_active=True, with_end_date=True)
    s.add(t)
    s.commit()
    task = s.query(Task).first()
    new_title = random_string(2000)
    new_description = random_string(20000)
    data = {"title": new_title, "description": new_description,
    "start_date": None, "end_date": None, "is_active": True}
    response = client.put(f"/task/{task.id}", data=json.dumps(data))
    assert response.status_code == 422
    s.close()


@db_setup_fixture()
def test_delete_task():
    s = TestSessionLocal()
    s.add(create_task_random_data())
    s.commit()
    task = s.query(Task).first()

    response = client.delete(f"/task/{task.id}")
    assert response.status_code == 204
    assert s.query(Task).first() is None
    s.close()

@db_setup_fixture()    
def test_delete_task_not_in_db():
    s = TestSessionLocal()
    response = client.delete(f"/task/1")
    assert response.status_code == 204
    assert s.query(Task).first() is None
    s.close()