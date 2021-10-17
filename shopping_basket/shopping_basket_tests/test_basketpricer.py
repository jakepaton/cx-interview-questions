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
            offer_type="BuyXGetYFree",
            product="Egg",
            num_to_buy=10,
            num_get_free=4,
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
            offer_type="BuyXGetYFree",
            product="Sardines",
            num_to_buy=2,
            num_get_free=1,
        )
    )

    # 10% discount on eggs
    offers.append(Discount(offer_type="Discount", product="Egg", discount_pc=0.10))

    # also a buy 10 get 4 free on eggs
    offers.append(
        BuyXGetYFree(
            offer_type="BuyXGetYFree",
            product="Egg",
            num_to_buy=10,
            num_get_free=4,
        )
    )
    return offers


# Test of subtotal
# Baked beans: 4 * 0.99 = 3.96
# Biscuits: 1 * 1.20
# Subtotal = 3.96 + 1.20 = 5.16
def test_subtotal1(basic_catalogue):
    basket = {"Baked Beans": 4, "Biscuits": 1}
    offers = {}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=offers)

    subtotal = pricer.basket_subtotal()
    assert subtotal >= 0 and abs(subtotal - 5.16) < 0.001


# Test of subtotal
# Baked beans: 2 * 0.99 = 1.98
# Biscuits: 1 * 1.20
# Sardines: 2 * 1.89 = 3.78
# Subtotal = 1.98 + 1.20 + 3.78 = 6.96
def test_subtotal2(basic_catalogue):
    basket = {"Baked Beans": 2, "Biscuits": 1, "Sardines": 2}
    offers = {}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=offers)

    subtotal = pricer.basket_subtotal()
    assert subtotal >= 0 and abs(subtotal - 6.96) < 0.001


# Test of percentage discounting, without any other offers
# Sardines should get a discount of 2 * 1.89 * 0.25 = 0.945
def test_discount1(basic_catalogue, basic_offers):
    basket = {"Biscuits": 1, "Sardines": 2}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)

    discount = pricer.basket_discount()
    assert discount >= 0 and abs(discount - 0.945) < 0.001


# Test of buy x get y free offer, without any other offers
# Should get 1 baked beans for free
# Discount = 0.99
def test_discount2(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 4, "Biscuits": 1}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)

    discount = pricer.basket_discount()
    assert discount >= 0 and abs(discount - 0.99) < 0.001


# Test of percentage discount and buy x get y free on different products
# Should get 1 baked beans for free; discount of 0.99
# And sardines should get a discount of 2 * 1.89 * 0.25 = 0.945
# Total discount = 0.99 + 0.945 = 1.935
def test_discount3(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 3, "Biscuits": 1, "Sardines": 2}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)

    discount = pricer.basket_discount()
    assert discount >= 0 and abs(discount - 1.935) < 0.001


# Test of buy x get y free applied multiple times on same product
# Should get 3 baked beans for free, having paid for 7
# Discount = 3 * 0.99 = 2.97
def test_discount4(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 10, "Biscuits": 1}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)

    discount = pricer.basket_discount()
    assert discount >= 0 and abs(discount - 2.97) < 0.001


# Test of buy x get y free applied partially
# Should get 3 eggs free having paid for 10 (though would have been eligible for 4 free)
# Discount = 3 * 0.20 = 0.60
def test_discount5(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 1, "Biscuits": 1, "Egg": 13}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)

    discount = pricer.basket_discount()
    assert discount >= 0 and abs(discount - 0.60) < 0.001


# Test of total (including discounts)
# Beans: 1 free => price = 3 * 0.99 = 2.97
# Biscuits: 1 => price = 1.20
# Basket total = 2.97 + 1.20 = 4.17
def test_total1(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 4, "Biscuits": 1}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)

    total = pricer.basket_total()
    assert total >= 0 and abs(total - 4.17) < 0.001


# Test of total (including discounts)
# Beans: 2 => price = 2 * 0.99 = 1.98
# Biscuits: 1 => price = 1.20
# Sardines: 2 with 25% discount => price = 2 * 1.89 * 0.75 = 2.835
# Basket total = 1.98 + 1.20 + 2.835 = 6.015
def test_total2(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 2, "Biscuits": 1, "Sardines": 2}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)

    total = pricer.basket_total()
    assert total >= 0 and abs(total - 6.015) < 0.001


# Test of multiple discounts applied to same product
# 10 Sardines => should get 3 for free as part of buy 2 get 1 free offer
# The remaining 7 paid for should get a 25% discount
# Discount = 3 * 1.89 + 7 * 1.89 * 0.25 = 8.9775
def test_multiple_discounts1(basic_catalogue, multiple_offers):
    basket = {"Sardines": 10}
    pricer = BasketPricer(
        basket=basket, catalogue=basic_catalogue, offers=multiple_offers
    )

    discount = pricer.basket_discount()
    assert discount >= 0 and abs(discount - 8.9775) < 0.001


# Test of multiple discounts applied to same product
# 13 Eggs => should get 3 for free as part of buy 10 get 4 free offer; discount = 3 * 0.20 = 0.60
# The remaining 10 paid for should get a 10% discount; discount = 10 * 0.20 * 0.10 = 0.20
# Total discount = 0.60 + 0.20 = 0.80
def test_multiple_discounts2(basic_catalogue, multiple_offers):
    basket = {"Egg": 13}
    pricer = BasketPricer(
        basket=basket, catalogue=basic_catalogue, offers=multiple_offers
    )

    discount = pricer.basket_discount()
    assert discount >= 0 and abs(discount - 0.80) < 0.001
