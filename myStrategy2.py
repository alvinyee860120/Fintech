
# coding: utf-8

# In[ ]:


import sys
import numpy as np
import pandas as pd

def myStrategy(pastdata, currPrice, stockType):
# stockType='SPY', 'IAU', 'LQD', 'DSI'
# find suitable parameters for different stocks
#Brute force to find parameters
#Explanation of my approach:
# 1. Technical indicator used: MA、利用MA計算短期MA與長期MA黃金交叉與死亡交叉
# 2. if price-ma>alpha and 短期MA>長期MA ==> buy, if price-ma<-beta and 短期MA<長期MA==> sell
# 3. Modifiable parameters: alpha, beta, windowsize1 for short MA, windowsize2 for long MA
# 4. exhaustive search: for loop 尋找最佳參數 alpha range(0~10), beta range (0~20), windowsize1 range(1~10), windowsize2 range(20~60)
    
# Set parameters for different stocks(exhaustive search完的參數結果)
    paramSetting={'SPY': {'alpha':4, 'beta':12, 'windowSize1':1, 'windowSize2':20}, 
                  'IAU': {'alpha':0, 'beta':2, 'windowSize1':10,'windowSize2':45},
                  'LQD': {'alpha':0, 'beta':1, 'windowSize1':4,'windowSize2':25},
                  'DSI': {'alpha':2, 'beta':8, 'windowSize1':10,'windowSize2':20}}
    windowSize1=paramSetting[stockType]['windowSize1']
    windowSize2=paramSetting[stockType]['windowSize2']
    alpha=paramSetting[stockType]['alpha']
    beta=paramSetting[stockType]['beta']
    
    
    dataLen=len(pastdata) # Length of the data vector
    action = 0 # action=1(buy), -1(sell), 0(hold), with 0 as the default action
    
    if dataLen==0: 
        return action
    # Compute MA
    if dataLen<windowSize1:
        sma=np.mean(pastdata) # If given price vector is small than windowSize, compute MA by taking the average
        lma=0
    elif dataLen>=windowSize1 and dataLen<windowSize2:
        windowedData=pastdata[-windowSize1:] # Compute the normal MA using windowSize 
        sma=np.mean(windowedData)
        lma=0
    else: 
        windowedData1=pastdata[-windowSize1:]
        windowedData2=pastdata[-windowSize2:] 
        sma=np.mean(windowedData1)
        lma=np.mean(windowedData2)
    
    # Determine action
    if (currPrice-sma)>alpha and sma>lma: # If price-ma > alpha ==> buy
        action=1
    elif (currPrice-sma)<-beta and sma<lma: # If price-ma < -beta ==> sell
        action=-1
    return action

    

# Compute return rate over a given price vector, with 3 modifiable parameters
def calculateReturnRate( file, stocksType) :
    # stocksType = "SPY" or "IAU" or "DSI" , "LQD"
    # read file
    df = pd.read_csv(file)
    adjClose = df["Adj Close"].values  # get adj close
    dataCount=len(adjClose) # day size
    
    # init.
    capital=1  # 持有資金
    capitalOrig=capital  # cost
    suggestedAction= np.zeros((dataCount,1))  # 判斷action
    stockHolding=np.zeros((dataCount,1))  # 持有股票
    total = np.zeros((dataCount,1))  # 結算資金
    realAction=np.zeros((dataCount,1))  # 實際action
    
    # run each day
    for ic in range(dataCount):
        currPrice=adjClose[ic]  # 當天價格
        suggestedAction[ic]=myStrategy(adjClose[0:ic], currPrice, stocksType) # 取得當天action
        
        # get real action by suggested action
        if ic > 0: 
            # 更新手上持有股票
            stockHolding[ic]=stockHolding[ic-1]
        if suggestedAction[ic] == 1:
            # 若未持有股票: 買
            if stockHolding[ic]==0:            
                stockHolding[ic]=capital/currPrice # 買入股票
                capital=0   # 持有資金
                realAction[ic]=1
        elif suggestedAction[ic] == -1:
            # 若持有股票： 賣
            if stockHolding[ic]>0:
                capital=stockHolding[ic]*currPrice # 賣出股票
                stockHolding[ic]=0  # 持有股票
                realAction[ic]=-1
        elif suggestedAction[ic] == 0:
            # 不買不賣
            realAction[ic]=0
        else:
            assert False
        # 當天結算資金
        total[ic]=capital+stockHolding[ic]*currPrice
    # 最終盈利率
    returnRate=(total[-1]-capitalOrig)/capitalOrig 
    return returnRate
    
if __name__ == '__main__':
    returnRate = calculateReturnRate( sys.argv[1], sys.argv[1][-7:-4] ) # ( file , stock_name ) 
    print(returnRate)

