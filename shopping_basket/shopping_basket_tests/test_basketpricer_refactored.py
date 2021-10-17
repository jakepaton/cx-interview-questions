from basket_pricer import BasketPricer
from offer import BuyXGetYFree, Discount
import pytest


@pytest.fixture
def basic_catalogue():
    catalogue = {
        "Baked Beans": 0.99,
        "Biscuits": 1.20,
        "Sardines": 1.89,
        "Shampoo (Small)": 2.00,
        "Shampoo (Medium)": 2.50,
        "Shampoo (Large)": 3.50,
        "Egg": 0.20,
    }
    return catalogue


# No overlapping offers
@pytest.fixture
def basic_offers():
    offers = []

    # 25% discount on sardines
    offers.append(Discount(offer_type="Discount", product="Sardines", discount_pc=0.25))

    # buy 2 get 1 free on baked beans
    offers.append(
        BuyXGetYFree(
            offer_type="BuyXGetYFree",
            product="Baked Beans",
            num_to_buy=2,
            num_get_free=1,
        )
    )

    # buy 10 get 4 free on eggs
    offers.append(
        BuyXGetYFree(
            offer_type="BuyXGetYFree", product="Egg", num_to_buy=10, num_get_free=4
        )
    )
    return offers


# Multiple offers for the same product
@pytest.fixture
def multiple_offers():
    offers = []

    # 25% discount on sardines
    offers.append(Discount(offer_type="Discount", product="Sardines", discount_pc=0.25))

    # also a buy 2 get 1 free on sardines
    offers.append(
        BuyXGetYFree(
            offer_type="BuyXGetYFree", product="Sardines", num_to_buy=2, num_get_free=1
        )
    )

    # 10% discount on eggs
    offers.append(Discount(offer_type="Discount", product="Egg", discount_pc=0.10))

    # also a buy 10 get 4 free on eggs
    offers.append(
        BuyXGetYFree(
            offer_type="BuyXGetYFree", product="Egg", num_to_buy=10, num_get_free=4
        )
    )
    return offers


# subtotal:
#     baked beans: 1 * 0.99 =  0.99
#     biscuits:    1 * 1.20 =  1.20
#     sum = 2.19
# discount:
#     sum = 0.00
# total:
#     subtotal - discount = 2.19 - 0.00 = 2.19
def test_no_offers(basic_catalogue):
    basket = {"Baked Beans": 1, "Biscuits": 1}
    offers = {}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=offers)

    subtotal = pricer.basket_subtotal()
    discount = pricer.basket_discount()
    total = pricer.basket_total()

    assert subtotal >= 0 and abs(subtotal - 2.19) < 0.01
    assert discount >= 0 and abs(discount - 0.00) < 0.01
    assert total >= 0 and abs(total - 2.19) < 0.01


# subtotal:
#     baked beans: 3 * 0.99 =  2.97
#     biscuits:    1 * 1.20 =  1.20
#     sardines:    6 * 1.89 = 11.34
#     sum = 15.51
# discount:
#     baked beans: 1 free @ 0.99 = 0.99
#     sardines: 6 discounted by 25% = 6 * 1.89 * 0.25 = 2.835
#     sum = 3.825
# total:
#     subtotal - discount = 15.51 - 3.825 = 11.685
def test_no_overlapping_offers(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 3, "Biscuits": 1, "Sardines": 6}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)

    subtotal = pricer.basket_subtotal()
    discount = pricer.basket_discount()
    total = pricer.basket_total()

    assert subtotal >= 0 and abs(subtotal - 15.51) < 0.01
    assert discount >= 0 and abs(discount - 3.825) < 0.01
    assert total >= 0 and abs(total - 11.685) < 0.01


# subtotal:
#     baked beans: 3 * 0.99 =  2.97
#     biscuits:    1 * 1.20 =  1.20
#     sardines:    6 * 1.89 = 11.34
#     eggs:       26 * 0.20 =  5.20
#     sum = 20.71
# discount:
#     sardines: 2 free @ 1.89 = 3.78
#     sardines: 4 discounted by 25% = 4 * 1.89 * 0.25 = 1.89
#     eggs: 6 free @ 0.20 = 1.20
#     eggs: 20 discounted by 10% = 20 * 0.20 * 0.10 = 0.40
#     sum = 7.27
# total:
#     subtotal - discount = 20.71 - 7.27 = 13.44
def test_with_overlapping_offers(basic_catalogue, multiple_offers):
    basket = {"Baked Beans": 3, "Biscuits": 1, "Sardines": 6, "Egg": 26}

    pricer = BasketPricer(
        basket=basket, catalogue=basic_catalogue, offers=multiple_offers
    )

    subtotal = pricer.basket_subtotal()
    discount = pricer.basket_discount()
    total = pricer.basket_total()

    assert subtotal >= 0 and abs(subtotal - 20.71) < 0.01
    assert discount >= 0 and abs(discount - 7.27) < 0.01
    assert total >= 0 and abs(total - 13.44) < 0.01
