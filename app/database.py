import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from dotenv import load_dotenv

load_dotenv()

# load DB
DB_URL= os.getenv("DATABASE_URL")

# crating engine
engine= create_async_engine(DB_URL)

# checking connection
try:
    with engine.connect():
        print("Connected to the database")
except:
    print("Failed to connect to the database")

# create global session
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# create BASE
Base = declarative_base()

# function for creating local session and closinng it
def get_db():
    with AsyncSessionLocal() as Session:
        yield Session

# checking db exist or not
def init_db():
    if not database_exists(DB_URL):
        create_database(DB_URL)
        print("DB created successfully")


