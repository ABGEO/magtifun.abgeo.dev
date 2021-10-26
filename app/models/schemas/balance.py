"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

# pylint: disable=C0115,R0903

# pylint: disable=E0611
from pydantic import BaseModel


class Balance(BaseModel):
    credit: int
    amount: int

    class Config:
        schema_extra = {
            "example": {
                "credit": 50,
                "amount": 5,
            }
        }
