from sqlalchemy import select
from . import models, schemas
from .database import database
from .auth import get_password_hash

async def get_user_by_username(username: str):
    """
    Retrieve a user from the database by username.

    Args:
        username (str): The username to search for.

    Returns:
        User: The user object if found, or None otherwise.
    """
    query = select(models.User).where(models.User.username == username)
    return await database.fetch_one(query)

async def create_user(user: schemas.UserCreate) -> models.User:
    """
    Create a new user in the database.

    Args:
        user (UserCreate): The user data to create.

    Returns:
        User: The newly created user object.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password, is_active=True
    )
    query = models.User.__table__.insert().values(
        username=db_user.username,
        email=db_user.email,
        hashed_password=db_user.hashed_password,
        is_active=db_user.is_active
    )
    await database.execute(query)
    return db_user
