from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

DATABASE_URL = "postgresql://admin:password@user_db:5432/user_crud"

# Async database instance
database = Database(DATABASE_URL)

# SQLAlchemy metadata for creating tables
metadata = MetaData()

# Base class for models
Base = declarative_base()

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)
