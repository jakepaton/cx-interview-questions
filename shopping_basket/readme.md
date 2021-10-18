## Documentation

Should be compatible with Python3.9+

Tests can be run via pytest from the /shopping_basket/ directory

basket_pricer.py implements the BasketPricer class that calculates the subtotal, discount amount, and total for a shopping basket.



## Assumptions

Catalogue contains sensible prices, e.g. prices are postitive floats.

Offers are sensible, i.e. no negative discounts, no negative numbers in "Buy x get y free" offers.

When there are multiple offers available for a product, these offers stack.

"Buy x get y free" offers are partially applied when the basket does not contain enough of an item, e.g. if there is a "Buy 5 get 2 free" offer on bananas, and the basket contains 6 bananas, then the customer will receive 1 free banana.
