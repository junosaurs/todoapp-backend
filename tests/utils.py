from schemas.tasks import TaskCreateSchema
from models.tasks import Task
from datetime import timedelta, datetime
import string
import random

def random_string(str_len: int, min_len=1):
    seq = string.ascii_letters + string.digits
    return ''.join(random.choice(seq) for _ in range(random.randint(min_len, str_len)))

def create_task_random_data(is_active=True, with_end_date=False):
    title = random_string(100)
    description = random_string(1000)
    if with_end_date:
        end_date = datetime.now() + timedelta(days=random.randint(1, 7), hours=random.randint(1,12))
    else:
        end_date = None
    return Task(title=title, description=description, end_date=end_date, is_active=is_active)

def create_task_random_data_create(is_active=True, with_end_date=False):
    title = random_string(100)
    description = random_string(1000)
    if with_end_date:
        end_date = datetime.now() + timedelta(days=random.randint(1, 7), hours=random.randint(1,12))
    else:
        end_date = None
    return TaskCreateSchema(title=title, description=description, end_date=end_date, is_active=is_active)