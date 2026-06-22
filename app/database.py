from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SERVER = "localhost"
DATABASE = "project_management_db"

connection_string = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


#connection generator
def get_db():
    with engine.begin() as connection:
        yield connection
