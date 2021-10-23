"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import SECRET_KEY
from app.models.domain.user import User
from app.resources import strings
from app.services.jwt import ALGORITHM
from app.services.magtifun import check_auth_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Load user from JWT token.

    :param str token: JWT user.
    :raises HTTPException: if unable to get user from given JWT.
    :return: User.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=strings.MALFORMED_PAYLOAD,
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        key: str = payload.get("sub")
        if key is None or not check_auth_key(key):
            raise credentials_exception

        return User(key=key)
    except JWTError as exception:
        raise credentials_exception from exception
