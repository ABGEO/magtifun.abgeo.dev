"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from datetime import datetime, timedelta
from typing import Dict

from jose import jwt

from app.core.config import SECRET_KEY

ALGORITHM = "HS256"


def create_access_token(data: Dict[str, any], expires_delta: timedelta) -> str:
    """
    Create JWT Token.

    :param Dict[str, any] data: JWT Payload.
    :param timedelta expires_delta: Expiration Delta..
    :return: JWT Token.
    """

    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
