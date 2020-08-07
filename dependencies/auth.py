from cryptography.fernet import Fernet
from fastapi import Form, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from pydantic import HttpUrl
from starlette import status

from config import settings
from models.auth import TokenData

auth_scheme = HTTPBearer(scheme_name="Bearer")


class GitlabAPiKeyRequestForm:
    """
    This is a dependency class, use it like:

        @app.post("/login")
        def login(form_data: GitlabAPiKeyRequestForm = Depends()):
            data = form_data.parse()
            print(data.app_url)
            print(data.api_key)
            return data


    It creates the following Form request parameters in your endpoint:

    app_url: app_url HttpUrl. Url to gitlab instance.
    api_key: api_key string. Account access token used for authorization.
    """

    def __init__(
            self,
            app_url: HttpUrl = Form(...),
            api_key: str = Form(...),
    ):
        # TODO: Fix app_url to have '/' on the end of the url
        self.app_url = app_url
        self.api_key = api_key


def encrypt(message: str, key: bytes) -> str:
    return Fernet(key).encrypt(bytes(message, "utf-8")).decode()


def decrypt(token: str, key: bytes) -> str:
    return Fernet(key).decrypt(bytes(token, "utf-8")).decode()


def get_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.secret_key, algorithms=[settings.access_token_algorithm])
        app_url: HttpUrl = payload.get("sub")
        api_key: str = decrypt(payload.get("api_key"), settings.fernet_key)
        if app_url is None or api_key is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return TokenData(app_url=app_url, api_key=api_key)


def get_refresh_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.secret_key, algorithms=[settings.access_token_algorithm])
        sub: list = decrypt(payload.get("sub"), settings.fernet_key).split(' ')
        app_url: HttpUrl = sub[0]
        api_key: str = sub[1]
        if app_url is None or api_key is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return TokenData(app_url=app_url, api_key=api_key, refresh_token=token.credentials)