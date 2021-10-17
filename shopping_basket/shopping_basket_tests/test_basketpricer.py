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
    }
    return catalogue


@pytest.fixture
def basic_offers():
    offers = []
    offers.append(Discount(offer_type="Discount", product="Sardines", discount_pc=0.25))
    offers.append(
        BuyXGetYFree(
            offer_type="BuyXGetYFree",
            product="Baked Beans",
            quantity_needed_to_buy=2,
            quantity_get_free=1,
        )
    )
    return offers


def test_subtotal1(basic_catalogue):
    basket = {"Baked Beans": 4, "Biscuits": 1}
    offers = {}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=offers)
    assert pricer.basket_subtotal() == 5.16


def test_subtotal2(basic_catalogue):
    basket = {"Baked Beans": 2, "Biscuits": 1, "Sardines": 2}
    offers = {}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=offers)
    assert pricer.basket_subtotal() == 6.96


# Test of percentage discounting, without any buy x get y free offers
def test_discount1(basic_catalogue, basic_offers):
    basket = {"Biscuits": 1, "Sardines": 2}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)
    assert pricer.basket_discount() == 0.945


# Test of buy x get y free offer, without any percentage discounting
def test_discount2(basic_catalogue, basic_offers):
    basket = {"Biscuits": 1, "Beans": 5}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)
    assert pricer.basket_discount() == 1.98
