from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import (
    DB_SERVER,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_DRIVER
)

connection_string = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
    f"?driver={DB_DRIVER.replace(' ', '+')}"
)

engine = create_engine(connection_string)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()