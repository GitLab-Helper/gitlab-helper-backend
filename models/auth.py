from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str


class TokenData(BaseModel):
    app_url: str
    api_key: str
    refresh_token: Optional[str]
