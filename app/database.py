from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/fasty';
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.fasty_db_username}:{settings.fasty_db_password}@{settings.fasty_db_hostname}:{settings.fasty_db_port}/{settings.fasty_db_name}';

engine = create_engine(SQLALCHEMY_DATABASE_URL);

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbcon = Depends(get_db);

# psycopg2
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fasty', user='postgres',
#                                 password='1234', cursor_factory=RealDictCursor);
#         cursor = conn.cursor();
#         print("Database connection was succusfull !");
#         break;
#     except Exception as error:
#         print("Connecting to database failed");
#         print("Error :", error);
#         time.sleep(2);