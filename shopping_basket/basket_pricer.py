from offer import Offer


class BasketPricer:
    """A class to calculate the subtotal, discount, and total for a shopping basket"""

    def __init__(
        self, basket: dict[str, int], catalogue: dict[str, float], offers: list[Offer]
    ):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def basket_subtotal(self) -> float:
        """Calculates the total price of the basket without any offers being applied"""
        subtotal = 0
        for product_name, quantity in self.basket.items():
            price = self.catalogue[product_name]
            subtotal += price * quantity
        return round(subtotal, ndigits=2)

    def basket_discount(self) -> float:
        """Calculates the total amount of discount to be applied"""
        total_discount = 0
        for offer in self.offers:
            if offer.offer_type == "Discount":
                total_discount += self.calc_percentage_discount(
                    product=offer.product, discount_pc=offer.discount_pc
                )
        return total_discount

    def basket_total(self) -> float:
        raise NotImplementedError

    def calc_percentage_discount(self, product: str, discount_pc: float) -> float:
        if product in self.basket:
            quantity = self.basket[product]
            price_pre_discount = self.catalogue[product]
            discount_amount = price_pre_discount * quantity * discount_pc
            return discount_amount
        else:
            return 0
