"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

# pylint: disable=C0115,R0903

from datetime import datetime
from enum import Enum
from typing import Optional

# pylint: disable=E0611
from pydantic import BaseModel


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Account(BaseModel):
    first_name: str
    last_name: str
    username: Optional[str] = None
    phone: str
    city: str
    birthdate: Optional[datetime] = None
    gender: Gender

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "john.doe",
                "phone": "599123456",
                "city": "თბილისი",
                "birthdate": datetime(1970, 1, 1),
                "gender": Gender.MALE,
            }
        }
