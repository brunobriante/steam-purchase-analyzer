from enum import Enum


class Currency(Enum):
    BRL = 1
    USD = 2
    EUR = 3
    Other = 4


class PurchaseType(Enum):
    Purchase = 1
    IAP = 2
    Gift = 3
    Other = 4
