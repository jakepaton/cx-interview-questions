from basket_pricer import BasketPricer
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


def test_subtotal1(basic_catalogue):
    basket = {"Baked Beans": 4, "Biscuits": 1}
    offers = {}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=offers)
    assert pricer.subtotal() == 5.16


def test_subtotal2(basic_catalogue):
    basket = {"Baked Beans": 2, "Biscuits": 1, "Sardines": 2}
    offers = {}
    pricer = BasketPricer(basket=basket, catalogue=basic_catalogue, offers=offers)
    assert pricer.subtotal() == 6.96
