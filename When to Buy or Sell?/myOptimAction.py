
# coding: utf-8

# In[2]:


import numpy as np
import operator


# In[3]:


def myOptimAction(priceMat, transFeeRate):
    # Explanation of my approach:
	# 1. Technical indicator used: Watch combine next day and skip day price and also seek for ups/downs
	# 2. if next day price > today price + transFee && skip m days==> buy
    #       * buy the best stock
	#    if next day price < today price + transFee && skip n days==> sell
    #       * sell if you are holding stock
    # 3. You should sell before buy to get cash each day
    
    # default
    cash = 1000
    hold = 0
    #parameter setting
    m=1
    n=5
    # user definition
    dataLen, stockCount = priceMat.shape  # day size & stock count   
    stockHolding = np.zeros((dataLen,stockCount))  # Matrix of stock holdings
    actionMat = []  # An k-by-4 action matrix which holds k transaction records.
    
    for day in range( 0, dataLen-1 ) :
        dayPrices = priceMat[day]  # Today price of each stock
        #nextDayPrices = priceMat[ day + 1 ]  # Next day price of each stock
        
        if day > 0:
            stockHolding[day] = stockHolding[day-1]  # The stock holding from the previous action day
        
        buyStock = -1  # which stock should buy. No action when is -1
        buyPrice = 0  # use how much cash to buy
        sellStock = []  # which stock should sell. No action when is null
        sellPrice = []  # get how much cash from sell
        bestPriceDiff = 0  # difference in today price & next day price of "buy" stock
        stockCurrentPrice = 0  # The current price of "buy" stock
        
        # Check next day price to "sell"
        for stock in range(stockCount) :
            todayPrice = dayPrices[stock]
            holding = stockHolding[day][stock]  # how much stock you are holding
            if day + n > dataLen:
                    nextDayPrices = priceMat[day+1]
                    nextDayPrice = nextDayPrices[stock]  # Next day price
            elif day + n < dataLen:
                    nextDayPrices = priceMat[day+n]
                    nextDayPrice = nextDayPrices[stock]  # skip day price
                
            if holding > 0 :  # "sell" only when you have stock holding
                if nextDayPrice < todayPrice*(1+transFeeRate) :  # next day price < today price, should "sell"
                    sellStock.append(stock)
                    # "Sell"
                    sellPrice.append(holding * todayPrice)
                    cash += holding * todayPrice*(1-transFeeRate) # Sell stock to have cash
                    stockHolding[day][sellStock] = 0
        
        # Check next day price to "buy"
        if cash > 0 :  # "buy" only when you have cash
            for stock in range(stockCount) :
                todayPrice = dayPrices[stock]
                if day + m > dataLen:
                    nextDayPrices = priceMat[day+1]
                    nextDayPrice = nextDayPrices[stock]  # Next day price
                elif day + m < dataLen:
                    nextDayPrices = priceMat[day+m]
                    nextDayPrice = nextDayPrices[stock]  # skip day price
                
                if nextDayPrice > todayPrice*(1+transFeeRate) :  # next day price > today price, should "buy"
                    diff = nextDayPrice - todayPrice*(1+transFeeRate)
                    if diff > bestPriceDiff :  # this stock is better
                        bestPriceDiff = diff
                        buyStock = stock
                        stockCurrentPrice = todayPrice
            # "Buy" the best stock
            if buyStock >= 0 :
                buyPrice = cash
                stockHolding[day][buyStock] = cash*(1-transFeeRate) / stockCurrentPrice # Buy stock using cash
                cash = 0
                
        # Save your action this day
        if buyStock >= 0 or len(sellStock) > 0 :
            action = []
            if len(sellStock) > 0 :
                for i in range( len(sellStock) ) :
                    action = [day, sellStock[i], -1, sellPrice[i]]
                    actionMat.append( action )
            if buyStock >= 0 :
                action = [day, -1, buyStock, buyPrice]
                actionMat.append( action )
    return actionMat 

