"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.models.domain.user import User
from app.models.schemas.balance import Balance
from app.services.magtifun import get_balance

router = APIRouter(prefix="/balance", tags=["Balance"])


@router.get("/", response_model=Balance, name="Get balance")
async def get(current_user: User = Depends(get_current_user)) -> Balance:
    """
    Get balance.
    """

    return get_balance(current_user.key)
