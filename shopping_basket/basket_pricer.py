class BasketPricer:
    """A class to calculate the subtotal, discount, and total for a shopping basket"""

    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def subtotal(self):
        raise NotImplementedError

    def discount(self) -> float:
        raise NotImplementedError

    def total(self) -> float:
        raise NotImplementedError
