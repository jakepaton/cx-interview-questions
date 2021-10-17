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
        return subtotal

    def basket_discount(self) -> float:
        """Calculates the total amount of discount to be applied"""
        total_discount = 0
        for offer in self.offers:
            if offer.offer_type == "Discount":
                total_discount += self.calc_percentage_discount(
                    product=offer.product, discount_pc=offer.discount_pc
                )
            elif offer.offer_type == "BuyXGetYFree":
                total_discount += self.calc_buy_x_get_y_free(
                    product=offer.product,
                    num_to_buy=offer.num_to_buy,
                    num_get_free=offer.num_get_free,
                )

        return total_discount

    def basket_total(self) -> float:
        return self.basket_subtotal() - self.basket_discount()

    def calc_percentage_discount(self, product: str, discount_pc: float) -> float:
        if product in self.basket:
            quantity = self.basket[product]
            price_pre_discount = self.catalogue[product]

            discount_amount = price_pre_discount * quantity * discount_pc
            return discount_amount
        else:
            return 0

    def calc_buy_x_get_y_free(
        self, product: str, num_to_buy: int, num_get_free: int
    ) -> float:
        if product in self.basket:
            num_in_basket = self.basket[product]
            price = self.catalogue[product]

            # quantity x + y is required to receive all y for free,
            # otherwise the deal can only be partially applied.
            full_deals = num_in_basket // (num_to_buy + num_get_free)
            remainder = num_in_basket % (num_to_buy + num_get_free)
            partial_deals = max(remainder - num_to_buy, 0)

            total_quantity_free = full_deals + partial_deals

            return total_quantity_free * price
        else:
            return 0
