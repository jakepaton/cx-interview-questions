from abc import ABC, abstractmethod


class Offer(ABC):
    """Abstract base class for offers to inherit from"""

    offer_type: str

    @abstractmethod
    def __init__(self):
        pass


class Discount(Offer):
    """A class for specifying a percentage discount for a product"""

    offer_type = "Discount"

    def __init__(self, product: str, discount_pc: float):
        self.product = product
        self.discount_pc = discount_pc


class BuyXGetYFree(Offer):
    """A class for specifying a buy x get y free promotion for a product"""

    offer_type = "BuyXGetYFree"

    def __init__(self, product: str, num_to_buy: int, num_get_free: int):
        self.product = product
        self.num_to_buy = num_to_buy
        self.num_get_free = num_get_free
