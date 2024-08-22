from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from . import models, schemas, crud, auth
from .database import engine, database

# Initialize the FastAPI app
app = FastAPI()

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    """
    Event that is triggered on application startup.
    Connects to the database.
    """
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    """
    Event that is triggered on application shutdown.
    Disconnects from the database.
    """
    await database.disconnect()

@app.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate):
    """
    Register a new user.

    Args:
        user (UserCreate): The user data to register.

    Returns:
        User: The registered user.
    """
    db_user = await crud.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    await crud.create_user(user)
    return await crud.get_user_by_username(user.username)

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login a user and provide an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login form data (username and password).

    Returns:
        dict: The access token and token type.
    """
    user = await auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(access_token: schemas.User = Depends(auth.oauth2_scheme)):
    """
    Get the current logged-in user.

    Args:
        access_token (User): The current logged-in user's token.

    Returns:
        User: The current logged-in user.
    """
    username= auth.decode_access(token=access_token)
    return await crud.get_user_by_username(username)

@app.get("/users/logout")
async def logut(access_token: schemas.User = Depends(auth.oauth2_scheme)):
    """
    Get the current logged-out.

    Args:
        access_token (User): The current logged-in user's token.

    Returns:
        dict: A message indicating that the user has been logged out.
    """
    auth.blacklist_token_set.add(access_token)
    return {"Message":"Logged Out Successfully"}

