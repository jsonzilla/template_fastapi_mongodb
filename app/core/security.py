import secrets
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core import Hasher, settings
from app.repositories import UserRepository
from app.storages.database_storage import get_db

_security = HTTPBasic()


async def get_token_header(x_token: str = Header(...)):
    """
    Get the token data from the header
    :param x_token: str
    :return: None
    """
    if x_token != settings.API_TOKEN:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")


async def get_token_app_header(x_token: str = Header(...), identifier: str = Header(...), client: str = Header(...)):
    """
    Get the token and application identifier data from the header
    :param x_token: str
    :param identifier: str
    :param client: str
    :return: None
    """
    if x_token != settings.API_TOKEN:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    if identifier is None:
        raise HTTPException(status_code=401, detail="Missing Identifier")
    if client is None:
        raise HTTPException(status_code=401, detail="Missing Client")


async def validate_auth(credentials: HTTPBasicCredentials = Depends(_security), db=Depends(get_db)):
    """
    Validate the user credentials
    :param credentials: HTTPBasicCredentials
    :param db: Database
    :return: str username
    """
    repo = UserRepository()
    user = await repo.get_one({'username': credentials.username}, db)

    if user:
        correct_username = secrets.compare_digest(credentials.username, user['username'])
        correct_password = Hasher.verify_password(credentials.password, user['password'])

        if (correct_username and correct_password):
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
