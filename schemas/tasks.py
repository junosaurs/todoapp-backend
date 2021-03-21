from typing import Optional
from pydantic import BaseModel
import datetime

class TaskBase(BaseModel):
    title: str
    description: str
    end_date: Optional[datetime.datetime]
    class Config:
        orm_mode = True

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]

class Task(TaskBase):
    id: int
    start_date: datetime.datetime
    is_active: bool