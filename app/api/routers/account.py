"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.models.domain.user import User
from app.models.schemas.account import Account
from app.services.magtifun import get_account_info

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/", response_model=Account)
async def account_info(current_user: User = Depends(get_current_user)) -> Account:
    """
    Get current account info.

    :param User current_user: Authenticated User.
    :return: Account info.
    """

    return get_account_info(current_user.key)
