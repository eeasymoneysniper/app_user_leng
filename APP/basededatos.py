from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL_PRACTICA = os.getenv("SQLALCHEMY_DATABASE_URL_PRACTICA")

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URL_PRACTICA)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
