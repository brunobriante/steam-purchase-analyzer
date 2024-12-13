import locale
import re
from datetime import date, datetime

import pandas as pd
from bs4 import BeautifulSoup as bs

from utils.enum import Currency, PurchaseType

MARKETPLACE_VALUE = (
    "Steam Community Market",  # English
    "Mercado da Comunidade Steam",  # Portuguese
)
WALLET_CREDIT_VALUE = (
    "Wallet Credit",  # English
    "crédito p/ Carteira",  # Portuguese
)
REFUND_VALUE = (
    "Refund",  # English
    "Reembolso",  # Portuguese
)
PURCHASE_VALUE = (
    "Purchase",  # English
    "Compra",  # Portugese
)
IAP_VALUE = (
    "In-Game Purchase",  # English
    "Transação no Mercado",  # Portuguese
)
GIFT_VALUE = (
    "Gift",  # English
    "Compra de presente",  # Portuguese
)

PRICE_RE = r"[0-9]*[.,][0-9]*"


def get_soup(file):
    try:
        return bs(file.getvalue().decode("utf-8"), "lxml")
    except BaseException:
        return bs("", "lxml")


def get_date(column: str, locale: str = "EN") -> date:
    return datetime.strptime(column, "%d %b, %Y").date()


def get_games(column: str) -> list:
    column = column.replace("\t", "")
    column = column.splitlines()
    return [game for game in column if game]


def get_amount(column: str) -> int:
    return len(get_games(column))


def get_type(column: str) -> PurchaseType:
    if column.startswith(PURCHASE_VALUE):
        return PurchaseType.Purchase
    if column.startswith(IAP_VALUE):
        return PurchaseType.IAP
    if column.startswith(GIFT_VALUE):
        return PurchaseType.Gift

    return PurchaseType.Other


def get_price(column: str) -> float:
    currency = get_currency(column)

    if currency in [Currency.BRL, Currency.EUR]:
        locale._override_localeconv["thousands_sep"] = "."
        locale._override_localeconv["decimal_point"] = ","

        return locale.atof(re.findall(PRICE_RE, column)[0])

    if currency in [Currency.USD]:
        locale._override_localeconv["thousands_sep"] = ","
        locale._override_localeconv["decimal_point"] = "."

        return locale.atof(re.findall(PRICE_RE, column)[0])


def get_currency(column: str) -> Currency:
    price = re.sub(PRICE_RE, "", column, 0).strip()
    if "R$" in price:
        return Currency.BRL
    if "$ USD" in price:
        return Currency.USD
    if "€" in price:
        return Currency.EUR

    return Currency.Other


def get_dataframe(file):
    data = []

    soup = get_soup(file)
    table = soup.find("table", "wallet_history_table")
    body = table.find("tbody")
    rows = body.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if (
            any(columns)
            and columns[1].text.strip() not in MARKETPLACE_VALUE
            and not columns[1].text.strip().endswith(WALLET_CREDIT_VALUE)
            and columns[2].text.strip() not in REFUND_VALUE
        ):
            data.append(
                {
                    "date": get_date(columns[0].text.strip()),
                    "games": get_games(columns[1].text.strip()),
                    "amount": get_amount(columns[1].text.strip()),
                    "type": get_type(columns[2].text.strip()),
                    "price": get_price(columns[3].text.strip()),
                    "currency": get_currency(columns[3].text.strip()),
                }
            )

    return pd.DataFrame().from_records(data)
