from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .utils import get_url

engine = create_engine(url=get_url(),echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)