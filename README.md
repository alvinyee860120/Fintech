# fintech-Profit-Optimization-for-SPY-Trading
## Desciprtion:
design trading strategies such that the total return of 4 stocks over a given period of time can be maximized.

### Datasets
There are 4 stocks for evaluation:

SPY: SPDR S&P 500 ETF (SPY)

IAU: iShares Gold Trust (IAU)

LQD: iShares iBoxx $ Investment Grade Corporate Bond ETF (LQD)

DSI: iShares MSCI KLD 400 Social ETF (DSI)

Each of the above dataset, which will fetch the stock price during the period Jan 01, 2005 to Sept 30, 2019.
We shall use the price of "Adj Close" for trading.

## Goal: 
find a strategy that can be applied to each of the stocks, such that the overall return can be maximized.

### Restriction:
1. Can only take the currently available historical data for reaching a decision of "buy" or "sell".

2. Since all the data is open, not allowed to "memorize the future data"
==>In other words, find the best way to use technical indicators (MA, RSI, etc) for maximizing the return.
