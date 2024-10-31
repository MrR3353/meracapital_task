import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from databases import Database
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


database = Database(DATABASE_URL)
metadata = MetaData()


prices = Table(
    "prices",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ticker", String, nullable=False),
    Column("price", Float, nullable=False),
    Column("timestamp", Integer, nullable=False),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
