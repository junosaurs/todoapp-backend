# for test purposes only!
from schemas import Task
import datetime
TEST_DATA = {
    1: Task(id=1, title="qwe123", description="asd", start_date=datetime.datetime.now(),  active=True),
    3: Task(id=3, title="456", description="x", start_date=datetime.datetime.now(), active=True),
    2: Task(id=2, title="789", description="y", start_date=datetime.datetime.now(), active=True),
    4: Task(id=4, title="QQQ", description="qdsfg;lkjhgfdwsdf", start_date=datetime.datetime.now(), active=True),
    5: Task(id=5, title="WWW", description="q wertyiouytrerfgjnvb hjghjv fghnfn fg fdg sa", start_date=datetime.datetime.now(), active=True),
}

def get_all_tasks():
    return list(TEST_DATA.values())

def get_task(task_id: int):
    task = TEST_DATA.get(task_id)
    return task

def create_task(task):
    return task

def update_task(task):
    task = TEST_DATA.get(task_id)
    return task

def delete_task(task_id: int):
    return True