import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from contextlib import asynccontextmanager
# from sqlalchemy_utils import database_exists, create_database

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

# Create async engine
engine = create_async_engine(DB_URL, echo=True)

# Sessionmaker
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base model
Base = declarative_base()

# Async DB Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Async DB connection check
async def check_connection():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None)
        print("Connected to the database")
    except Exception as e:
        print("Failed to connect to the database:", e)

# def create_db_if_not_exists():
#     if not database_exists(DB_URL):
#         create_database(DB_URL)
#         print("✅ Database created.")
#     else:
#         print("🟢 Database already exists.")

