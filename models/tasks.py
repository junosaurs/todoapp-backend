from database.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100))
    description = Column(String(1000))
    start_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)