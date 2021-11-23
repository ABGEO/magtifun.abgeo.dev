"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

# pylint: disable=C0115,R0903

from datetime import datetime

# pylint: disable=E0611
from pydantic import BaseModel

from app.resources.strings import SEND_SMS_STATUSES


class SMSOnSend(BaseModel):
    recipient: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "recipient": "599123456",
                "message": "Hello",
            }
        }


class SMSSendResult(BaseModel):
    status: bool
    message: str

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": SEND_SMS_STATUSES["success"],
            }
        }


class SMSHistoryItem(BaseModel):
    id: int
    date: datetime
    recipient: str
    text: str
    delivered: bool


class SMSHistoryItemRemoveStatus(BaseModel):
    status: bool
