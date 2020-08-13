from datetime import datetime, timedelta
from typing import Optional

import requests
from fastapi import HTTPException, Depends, APIRouter
from jose import jwt
from pydantic import HttpUrl
from starlette import status

from config import settings
from dependencies.auth import GitlabAPiKeyRequestForm, encrypt, get_refresh_token
from models.auth import TokenData, Token
from models.core import ErrorResponse

router = APIRouter()


def authenticate_gitlab(app_url: HttpUrl, api_key: str):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(app_url + '/api/v4/version/', headers=headers)
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect gitlab instance url",
        )
    return TokenData(app_url=app_url, api_key=api_key)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.access_token_algorithm)
    return encoded_jwt


@router.post(
    "/token",
    response_model=Token,
    summary="Authorization of gitlab service",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized",
        }
    }
)
async def get_gitlab_token(form_data: GitlabAPiKeyRequestForm = Depends()):
    gitlab = authenticate_gitlab(form_data.app_url, form_data.api_key)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": gitlab.app_url, "api_key": encrypt(gitlab.api_key, settings.fernet_key)},
        expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=settings.refresh_token_expire_minutes)
    refresh_token = create_access_token(
        data={"sub": encrypt(gitlab.app_url + ' ' + gitlab.api_key, settings.fernet_key)},
        expires_delta=refresh_token_expires
    )
    return {"token_type": "bearer", "access_token": access_token,
            "expires_in": settings.access_token_expire_minutes, "refresh_token": refresh_token}


@router.post(
    "/refresh_token",
    response_model=Token,
    summary="Refresh authorization token with refresh token",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized",
        }
    }
)
async def get_refresh_gitlab_token(token: TokenData = Depends(get_refresh_token)):
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": token.app_url, "api_key": encrypt(token.api_key, settings.fernet_key)},
        expires_delta=access_token_expires
    )
    return {"token_type": "bearer", "access_token": access_token,
            "expires_in": settings.access_token_expire_minutes, "refresh_token": token.refresh_token}
