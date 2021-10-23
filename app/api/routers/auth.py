"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.schemas.jwt import Token
from app.resources import strings
from app.services.jwt import create_access_token
from app.services.magtifun import authenticate_user

router = APIRouter(tags=["Auth"])


@router.post("/token", response_model=Token)
async def token_authentication(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    Create Authentication JWT Token.

    :param OAuth2PasswordRequestForm form_data: Authentication data.
    :raises HTTPException: if unable to     create JWT.
    :return: Authentication Token.
    """

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=strings.INCORRECT_LOGIN_INPUT,
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.key},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token, token_type="bearer")
