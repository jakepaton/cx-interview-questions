from dataclasses import dataclass
from abc import ABC


@dataclass
class Offer(ABC):
    offer_type: str


@dataclass
class Discount(Offer):
    offer_type = "Discount"
    product: str
    discount_pc: float


@dataclass
class BuyXGetYFree(Offer):
    offer_type = "BuyXGetYFree"
    product: str
    quantity_needed_to_buy: int
    quantity_get_free: int
