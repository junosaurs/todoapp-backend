from typing import Optional
from pydantic import BaseModel
import datetime

class TaskBase(BaseModel):
    title: str
    description: str
    end_date: Optional[datetime.datetime]

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str]
    description: Optional[str]
    active: Optional[bool]

class Task(TaskBase):
    id: int
    start_date: datetime.datetime
    active: bool