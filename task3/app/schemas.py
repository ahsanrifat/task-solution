from pydantic import BaseModel

class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
    """
    username: str
    email: str
    password: str

class User(BaseModel):
    """
    Schema for returning user details.

    Attributes:
        id (int): The primary key.
        username (str): The username of the user.
        email (str): The email of the user.
        is_active (bool): Status indicating if the user is active.
    """
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        """
        Pydantic configuration to allow ORM mode, which makes it easier to return database models.
        """
        from_attributes = True
