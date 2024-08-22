from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class User(Base):
    """
    SQLAlchemy model for the User table.

    Attributes:
        id (int): The primary key.
        username (str): The unique username of the user.
        email (str): The unique email of the user.
        hashed_password (str): The hashed password of the user.
        is_active (bool): Status indicating if the user is active.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
