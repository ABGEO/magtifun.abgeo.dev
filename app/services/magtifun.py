"""
This file is part of the magtifun.abgeo.dev.

(c) 2021 Temuri Takalandze <me@abgeo.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from datetime import datetime
from typing import Union

import requests
from bs4 import BeautifulSoup as bs
from fastapi import HTTPException

from app.models.domain.user import User
from app.models.schemas.account import Account, Gender
from app.models.schemas.balance import Balance, BalanceHistoryItem
from app.models.schemas.sms import SMSOnSend, SMSSendResult, SMSHistoryItem
from app.resources.strings import SEND_SMS_STATUSES

SITE_BASE_URL: str = "http://www.magtifun.ge"


def get_session(key: str) -> requests.Session():
    """
    Get authenticated session with given authentication key.

    :param str key: Authentication Key.
    :return: Authenticated Session.
    """

    session = requests.Session()
    session.cookies.set("User", key)
    session.headers["Referer"] = SITE_BASE_URL

    return session


def check_auth_key(key: str) -> bool:
    """
    Check if Authentication Key is correct or not.

    :param str key: Authentication Key.
    :return: Whether if Authentication Key is correct or not.
    """

    session = get_session(key)

    response = session.get(f"{SITE_BASE_URL}/")
    response.encoding = "utf-8"

    return "თქვენს ანგარიშზეა" in response.text


def authenticate_user(username: str, password: str) -> Union[User, None]:
    """
    Authenticate user with given username and password.

    :param str username: Authentication username.
    :param str password: Authentication password.
    :return: Authenticated User or none.
    """

    session = requests.Session()

    form_response = session.get(f"{SITE_BASE_URL}/")
    soup = bs(form_response.text, "html.parser")
    form_data = {
        "user": username,
        "password": password,
        "act": "1",
        "csrf_token": soup.select('input[name="csrf_token"]')[0]["value"],
    }

    login_response = session.post(f"{SITE_BASE_URL}/index.php?page=11", data=form_data)
    login_response.encoding = "utf-8"

    key = session.cookies.get("User")
    if check_auth_key(key):
        return User(key=key)

    return None


def send_sms(key: str, sms: SMSOnSend) -> SMSSendResult:
    """
    Send SMS.

    :param str key: Authentication Key.
    :param SMSOnSend sms: SMS Body.
    :return: SMS send result.
    """

    session = get_session(key)

    form_response = session.get(f"{SITE_BASE_URL}/index.php?page=2")
    soup = bs(form_response.text, "html.parser")
    form_data = {
        "csrf_token": soup.select('input[name="csrf_token"]')[0]["value"],
        "recipients": sms.recipient,
        "message_body": sms.message,
    }
    send_response = session.post(
        f"{SITE_BASE_URL}/scripts/sms_send.php", data=form_data
    )
    status_message = send_response.text

    if status_message == "not_logged_in":
        raise HTTPException(status_code=401)

    if status_message not in SEND_SMS_STATUSES:
        status_message = "default"

    return SMSSendResult(
        status=status_message == "success", message=SEND_SMS_STATUSES[status_message]
    )


def get_account_info(key: str) -> Account:
    """
    Get current account info.

    :param str key: Authentication key.
    :return: Account info.
    """

    session = get_session(key)

    response = session.get(f"{SITE_BASE_URL}/index.php?page=7")
    response.encoding = "utf-8"
    soup = bs(response.text, "html.parser")

    day = soup.find("select", {"id": "day"}).find("option", {"selected": True}).text
    month = soup.find("select", {"id": "month"}).find("option", {"selected": True}).text
    year = soup.find("select", {"id": "year"}).find("option", {"selected": True}).text

    birthdate = None
    if day and month and year:
        months = {
            "იანვარი": 1,
            "თებერვალი": 2,
            "მარტი": 3,
            "აპრილი": 4,
            "მაისი": 5,
            "ივნისი": 6,
            "ივლისი": 7,
            "აგვისტო": 8,
            "სექტემბერი": 9,
            "ოქტომბერი": 10,
            "ნოემბერი": 11,
            "დეკემბერი": 12,
        }

        birthdate = datetime(int(year), months[month], int(day))

    return Account(
        first_name=soup.find("input", {"id": "f_name"}).get("value"),
        last_name=soup.find("input", {"id": "l_name"}).get("value"),
        username=soup.find("input", {"id": "user_name"}).get("value"),
        phone=soup.find(
            "input", {"class": "round_border large_box", "disabled": True}
        ).get("value"),
        city=soup.find("select", {"id": "city"})
        .find("option", {"selected": True})
        .text.strip(),
        birthdate=birthdate,
        gender=Gender.FEMALE
        if soup.find("input", {"id": "female", "checked": True})
        else Gender.MALE,
    )


def get_balance(key: str) -> Balance:
    """
    Get account balance.

    :param str key: Authentication key.
    :return: Balance.
    """

    session = get_session(key)
    form_user_action = bs(session.get(SITE_BASE_URL).text, "html.parser").find(
        "form", {"name": "user_action"}
    )

    return Balance(
        credit=form_user_action.find("span", {"class": "xxlarge dark english"}).text,
        amount=form_user_action.find("span", {"class": "dark english"}).text,
    )


def get_balance_history(key: str):
    """
    Get account balance history.

    :param str key: Authentication key.
    :return: List of BalanceHistoryItems.
    """

    session = get_session(key)

    response = session.get(f"{SITE_BASE_URL}/index.php?page=16&lang=en")
    response.encoding = "utf-8"
    soup = bs(response.text, "html.parser")

    div_left_side = soup.find("div", {"class": "left_side"})
    divs = div_left_side.find_all("div")

    last_date = None
    items = []
    for div in divs:
        if div.has_attr("class"):
            classes = div["class"]
            if "date_separator" in classes:
                last_date = div.text
            elif "box_div" in classes:
                row = div.find("tr")
                time = row.find("td", {"class": "msg_date"}).text
                amount_parts = row.find(
                    "td", {"class": "credit_list_amount"}
                ).text.split(" ")

                item = BalanceHistoryItem(
                    date=datetime.strptime(f"{last_date} {time}", "%d %B %Y %H:%M:%S"),
                    message=row.find("td", {"class": "msg_body"}).text,
                    amount=int(amount_parts[1]),
                    charge=amount_parts[0] == "-",
                )

                items.append(item)

    return items


def get_sms_history(key: str):
    """
    Get SMS history.

    :param str key: Authentication key.
    :return: List of SMSHistoryItems.
    """

    session = get_session(key)

    url = f"{SITE_BASE_URL}/index.php?page=10&lang=en"
    response = session.get(url)
    pages = bs(response.text, "html.parser").find_all("span", {"class": "page_number"})
    items = _parse_sms_history_items(response)

    if len(pages) != 0:
        del pages[0]
        for page in pages:
            items = items + _parse_sms_history_items(
                session.post(url, {"cur_page": page.text})
            )

    return items


def remove_sms_from_history(sms_id: int, key: str):
    """
    Remove SMS from history.

    :param int sms_id: SMS ID to remove.
    :param str key: Authentication key.
    :return: List of SMSHistoryItems.
    """

    session = get_session(key)
    response = session.post(
        f"{SITE_BASE_URL}/scripts/delete_message.php",
        {"type": "single", "msg_id": sms_id},
    )

    return response.status_code == 200 and response.text == "success"


def _parse_sms_history_items(response):
    response.encoding = "utf-8"
    soup = bs(response.text, "html.parser")
    messages = soup.find("div", {"id": "message_list"})

    items = []
    for message in messages:
        body = message.find("td", {"class": "msg_body"})
        date = datetime.strptime(
            message.find("td", {"class": "msg_date"}).text, "%d%b%Y%H:%M:%S"
        )
        recipient = (
            body.find("p", {"class": "message_list_recipient"})
            .find_all("span", {"class": "red"})[1]
            .text
        )

        item = SMSHistoryItem(
            id=message["id"][4:],
            date=date,
            recipient=recipient,
            text=body.find("p", {"class": "msg_text"}).text,
            delivered=("msg_sent" in message["class"]),
        )

        items.append(item)

    return items
