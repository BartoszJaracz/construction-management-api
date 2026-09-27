from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

DB_SERVER = getenv("DB_SERVER")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_DRIVER = getenv(
    "DB_DRIVER",
    "ODBC Driver 17 for SQL Server"
)

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not configured")

if not DB_SERVER:
    raise RuntimeError("DB_SERVER is not configured")

if not DB_NAME:
    raise RuntimeError("DB_NAME is not configured")

if not DB_USER:
    raise RuntimeError("DB_USER is not configured")

if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD is not configured")