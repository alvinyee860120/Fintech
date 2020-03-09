# Fintech: When to Buy and Sell?
* Suppose we only has a single stock to buy or sell. Since all the price information is known in advance, we can use a simple strategy to do trading:
1. Buy if the price is up for the next day. If there are more than one stocks going up, choose the one that has the biggest "up".
2. Sell if the price is down for the next day. If there are more than one stocks going down, choose the one that has the biggest "down".

### Note:
1. Assume the price is available at the beginning of each day, and you can use this price for "buy" and "sell" and the transaction will always be granted.
2. we can have several transactions within a day.
3. To run the main program, you can type as follows: **python rrEstimateOpen.py priceMat.txt 0.01**
4. PriceMat.txt is the price of 4 stocks, with each column being the daily price of a stock.
