

ALGORITHM:
----------
x1. make static lists of all stocks for all strategies (3 per strat)
x2. for each stock, get price, PEG
x3. find out ranking and ratios per stock
x4. get amount per stock + round down number of stocks
x5. figure out what to do with remainder
x6. catch http error
x7. add remaining lists
x8. performance caching
x9. plot each stocks and portfolio chart

FRONT END INPUT:
-----------
x1. dropdown lists for strategy picking
x2. text box for amount
3. portfolio values for multiple strategy

FRONT END OUTPUT:
-----------
z1. P elements with portfolio details:
x2. for each in stock:
3.	amount spent - pie chart
x4. portfolio image itself

BACKEND 
-----------
x1. pass information back
x2. handle server.pys strategy split
x3. execute clean script as part of click (clear_Everything)
x4. remove clean script from git

ERROR CHECKS:
-----------
x1. for invalid strategy, 
x1. invalid amount
x2. httperror in lookup.py while doing history
x3. empty input from html
x4. sometimes portfolio exceeds total amount - for all except growth stocks
5. FIX all in the bug list
6. Build retry and timeout mechanism for server error
7. performance tracking


BUG LIST:
-----------
1. 
  File "/Users/kprasad/Desktop/portfolio_engine/lookup.py", line 24, in draw_stock
    five_day_data = stock.get_historical(str(date_five_before), str(date_now))
  File "/Library/Python/2.7/site-packages/yahoo_finance/__init__.py", line 342, in get_historical
    result = self._request(query)
  File "/Library/Python/2.7/site-packages/yahoo_finance/__init__.py", line 125, in _request
    raise YQLResponseMalformedError()
YQLResponseMalformedError: Response malformed.

