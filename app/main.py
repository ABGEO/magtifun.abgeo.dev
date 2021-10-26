"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from fastapi import FastAPI

from app.api.routers import account, auth, balance, sms

app = FastAPI()

app.include_router(account.router)
app.include_router(auth.router)
app.include_router(balance.router)
app.include_router(sms.router)
