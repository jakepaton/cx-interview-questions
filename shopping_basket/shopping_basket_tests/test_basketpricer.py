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
            num_to_buy=2,
            num_get_free=1,
        )
    )
    return offers


def test_subtotal1(basic_catalogue):
    basket = {"Baked Beans": 4, "Biscuits": 1}
    offers = {}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=offers)
    assert abs(pricer.basket_subtotal() - 5.16) < 0.01


def test_subtotal2(basic_catalogue):
    basket = {"Baked Beans": 2, "Biscuits": 1, "Sardines": 2}
    offers = {}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=offers)
    assert abs(pricer.basket_subtotal() - 6.96) < 0.01


# Test of percentage discounting, without any buy x get y free offers
def test_discount1(basic_catalogue, basic_offers):
    basket = {"Biscuits": 1, "Sardines": 2}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)
    assert abs(pricer.basket_discount() - 0.95) < 0.01


# Test of buy x get y free offer, without any percentage discounting
def test_discount2(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 4, "Biscuits": 1}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)
    assert abs(pricer.basket_discount() - 0.99) < 0.01


def test_discount3(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 2, "Biscuits": 1, "Sardines": 2}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)
    assert abs(pricer.basket_discount() - 0.95) < 0.01


def test_discount4(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 10, "Biscuits": 1, "Sardines": 20}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)
    assert abs(pricer.basket_discount() - 12.42) < 0.01


def test_total1(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 4, "Biscuits": 1}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)
    assert abs(pricer.basket_total() - 4.17) < 0.01


def test_total2(basic_catalogue, basic_offers):
    basket = {"Baked Beans": 2, "Biscuits": 1, "Sardines": 2}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=basic_offers)
    assert abs(pricer.basket_total() - 6.01) < 0.01
