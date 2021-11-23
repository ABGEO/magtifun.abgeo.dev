"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.models.domain.user import User
from app.models.schemas.sms import (
    SMSOnSend,
    SMSSendResult,
    SMSHistoryItem,
    SMSHistoryItemRemoveStatus,
)
from app.services.magtifun import send_sms, get_sms_history, remove_sms_from_history

router = APIRouter(prefix="/sms", tags=["SMS"])


@router.post("/", response_model=SMSSendResult)
async def send(
    sms: SMSOnSend, current_user: User = Depends(get_current_user)
) -> SMSSendResult:
    """
    Send SMS.
    """

    return send_sms(current_user.key, sms)


@router.get("/", response_model=List[SMSHistoryItem], name="Get sent SMSs")
async def get_all(
    current_user: User = Depends(get_current_user),
) -> List[SMSHistoryItem]:
    """
    Get sent SMSs.
    """

    return get_sms_history(current_user.key)


@router.delete(
    "/{sms_id}",
    response_model=SMSHistoryItemRemoveStatus,
    name="Remove SMS from history",
)
async def delete(
    sms_id: int,
    current_user: User = Depends(get_current_user),
) -> SMSHistoryItemRemoveStatus:
    """
    Remove SMS from history.
    """

    return SMSHistoryItemRemoveStatus(
        status=remove_sms_from_history(sms_id, current_user.key)
    )
