"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.models.domain.user import User
from app.models.schemas.sms import SMSOnSend, SMSSendResult
from app.services.magtifun import send_sms

router = APIRouter(prefix="/sms", tags=["SMS"])


@router.post("/", response_model=SMSSendResult)
async def send(
    sms: SMSOnSend, current_user: User = Depends(get_current_user)
) -> SMSSendResult:
    """
    Send SMS.

    :param SMSOnSend sms: SMS Body.
    :param User current_user: Current User.
    :return: SMS send result.
    """

    return send_sms(current_user.key, sms)
