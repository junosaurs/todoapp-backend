from typing import Optional
from pydantic import BaseModel, validator, root_validator
import datetime

class TaskBaseSchema(BaseModel):
    title: str
    description: str
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    class Config:
        orm_mode = True

class TaskCreateSchema(TaskBaseSchema):
    @validator('title')
    def title_max_length(cls, v):
        if len(v) > 100:
            raise ValueError
        return v

    @validator('description')
    def description_max_length(cls, v):
        if len(v) > 1000:
            raise ValueError
        return v
    
    @root_validator
    def end_date_after_start_date(cls, values):
        if values.get("start_date") is not None and values.get("end_date") is not None:
            if values.get("start_date") > values.get("end_date"):
                raise ValueError
        return values

class TaskUpdateSchema(TaskCreateSchema):
    is_active: bool

class TaskReadSchema(TaskBaseSchema):
    id: int
    start_date: datetime.datetime
    is_active: bool