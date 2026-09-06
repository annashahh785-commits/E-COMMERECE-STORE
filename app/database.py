from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase , sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

Engine=create_engine(DATABASE_URL)

SessionLocal =sessionmaker(
    bind=Engine,
    autocommit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()

    try:
        yield db

    finally:
        db.close()