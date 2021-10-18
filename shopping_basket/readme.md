## Documentation
basket_pricer.py implements the BasketPricer class that calculates the subtotal, discount amount, and total for a shopping basket.
BasketPricer requires:
* a shopping basket (_dict[str, int]_ representing products and their quantities)
* a catalogue (_dict[str, float]_ representing products and their prices)
* a collection of offers (_list[Offer]_ where Offer is implemented in offer.py)

There are two subclasses of Offer avaiable: Discount (for percentage discounts) or BuyXGetYFree (e.g. buy 1 get 1 free)

## Running the tests
Clone this project and run pytest from the _/shopping_basket/_ directory:

_python -m pytest_

To install dependencies via pipenv, run _pipenv install_ from the _/shopping_basket/_ directory to create a virtual environment with the dependencies installed. You can activate the virtual environment via _pipenv shell_, or run the tests directly via _pipenv run pytest_


## Assumptions

Catalogue contains sensible prices, e.g. prices are postitive floats.

Offers are sensible, i.e. no negative discounts, no negative numbers in "Buy x get y free" offers.

When there are multiple offers available for a product, these offers stack.

"Buy x get y free" offers are partially applied when the basket does not contain enough of an item, e.g. if there is a "Buy 5 get 2 free" offer on bananas, and the basket contains 6 bananas, then the customer will receive 1 free banana.

## Limitations

If there are multiple "Buy x get y free" offers, then these will be applied in the order in which they appear in the list of offers. This may result in a suboptimal combination of offers being applied. 
For example: suppose there are both "Buy 6 get 5 free" and "Buy 5 get 4 free" offers on lemons. If there are 11 lemons in a basket and the "Buy 5 get 4 free" offer is applied first, then this will prevent the "Buy 6 get 5 free" offer from being applied, meaning the customer will pay for 7 lemons rather than 6.
