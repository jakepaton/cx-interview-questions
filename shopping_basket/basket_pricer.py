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

        # Keep track of which items are eligible for further discounts, and their discounted prices
        eligible_for_discount = dict(self.basket)
        discounted_catalogue = dict(self.catalogue)

        for offer in self.offers:
            if offer.offer_type == "Discount":
                total_discount += self.calc_percentage_discount(
                    basket=eligible_for_discount,
                    catalogue=discounted_catalogue,
                    product=offer.product,
                    discount_pc=offer.discount_pc,
                )
            elif offer.offer_type == "BuyXGetYFree":
                total_discount += self.calc_buy_x_get_y_free(
                    basket=eligible_for_discount,
                    catalogue=discounted_catalogue,
                    product=offer.product,
                    num_to_buy=offer.num_to_buy,
                    num_get_free=offer.num_get_free,
                )

        return total_discount

    def basket_total(self) -> float:
        """Calculates the total price of the basket after application of discounts"""
        return self.basket_subtotal() - self.basket_discount()

    def calc_percentage_discount(
        self,
        basket: dict[str, int],
        catalogue: dict[str, float],
        product: str,
        discount_pc: float,
    ) -> float:
        if product in basket:
            quantity = basket[product]
            price_pre_discount = catalogue[product]

            discounted_price = price_pre_discount * (1 - discount_pc)

            # Update catalogue with the discounted price for use with further discounts
            catalogue[product] = discounted_price

            discount_amount = (price_pre_discount - discounted_price) * quantity
            return discount_amount
        else:
            return 0

    def calc_buy_x_get_y_free(
        self,
        basket: dict[str, int],
        catalogue: dict[str, float],
        product: str,
        num_to_buy: int,
        num_get_free: int,
    ) -> float:
        if product in basket:
            num_in_basket = basket[product]
            price = catalogue[product]

            # quantity x + y is required to receive all y for free,
            # otherwise the deal can only be partially applied.
            full_deals = num_in_basket // (num_to_buy + num_get_free)
            remainder = num_in_basket % (num_to_buy + num_get_free)
            partial_deals = max(remainder - num_to_buy, 0)

            total_num_free = full_deals + partial_deals

            # Keep track of free items so these can't be discounted further
            basket[product] -= total_num_free

            return total_num_free * price
        else:
            return 0
