from enum import Enum


class Currency(str, Enum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"
    Other = "Other"


class PurchaseType(str, Enum):
    Purchase = "Purchase"
    IAP = "IAP"
    Gift = "Gift"
    Other = "Other"
