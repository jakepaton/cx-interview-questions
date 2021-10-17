class BasketPricer:
    """A class to calculate the subtotal, discount, and total for a shopping basket"""

    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def subtotal(self) -> float:
        """Calculates the total price of the basket without any offers being applied"""
        subtotal = 0
        for product_name, quantity in self.basket.items():
            price = self.catalogue[product_name]
            subtotal += price * quantity
        return round(subtotal, ndigits=2)

    def discount(self) -> float:
        raise NotImplementedError

    def total(self) -> float:
        raise NotImplementedError
