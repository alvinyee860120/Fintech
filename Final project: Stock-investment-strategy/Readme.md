# Fintech: Stock-investment-strategy:
* Implement a trading strategy for 台指期 by submit a function in Python: action=myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice)
* where:
1. openPrice: Open price at day i, which is the price used to execute "buy" or "sell".
2. action: 1 for "buy", -1 for "sell", 0 for "no action". Every time you execute an action we will use all the money to buy or sell 台指期.
>If your hold position is not 0 and you execute "buy", it means" no action" because you have no money to buy.
>On the other hand, if your hold position is 0 and execute "sell", it means "no action" because you have nothing to sell.
3. Execution of either "buy" or "sell" in day i is based on open(i), which is the "open" price at day i.

### Note:
1. The initial fund for such investment is 500,000 NTD.
2. The transaction fee is 100 NTD for each "buy" or "sell".
3. The main program to call your function: projectEval.py. (At day i, the historical data contains all available information before or equal to day i−1

### My method:
1. you can see my implementation with details in final_report.pdf 
2. fintech KD.xlsx is printed out by using the KD indicator as my investment strategy.

### Return Rate: 353%
