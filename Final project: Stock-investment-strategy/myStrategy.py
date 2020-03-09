
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import operator



# In[ ]:
def compute_RSI(priceData, n):
    U = []
    D = []
    for i in range(n,0,-1):
        # print(i)
        diff = priceData[-i] - priceData[-i-1]
        if diff > 0:
            U.append(diff)
            D.append(0)
        elif diff < 0:
            U.append(0)
            D.append(-diff)
        else:
            U.append(0)
            D.append(0)
    avgU = np.mean(U)
    avgD = np.mean(D)
    RSI =  (avgU / (avgU + avgD))*100
    return RSI
#final: 353
def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPricev):
    open_history = dailyOhlcvFile['open'].values
    open_history4 = open_history[-4:] #最後4天開盤價
    open_history19 = open_history[-19:] #最後19天開盤價
    sum1 = sum(open_history4)
    sum1 += openPricev
    sum2 = sum(open_history19)
    sum2 += openPricev
    #短線操作(均線法): 5MA、20MA
    short_MA = sum1 / 5
    long_MA = sum2 / 20


    #距預測日最近3天的股票開盤價是否有連續漲/跌三天
    O1 = open_history[-3] - open_history[-4]
    O2 = open_history[-2] - open_history[-3]
    O3 = open_history[-1] - open_history[-2]
    if O1 > 0 and O2 > 0 and O3 > 0:
        trend = 1
    elif O1 < 0 and O2 < 0 and O3 < 0:
        trend = -1
    else:
        trend = 0

    #越靠近預測日的資料可操考性的權重比例越高，compute加權平均過的ma
    #parameter c
    c = 64
    windowedsize_Data = open_history[-c:]
    weight = []
    for i in range(1,c+1):
        weight.append(i)
    weight = np.array(weight)
    norm_weight = weight / sum(weight) #normalized
    weight_ma = np.dot(norm_weight, windowedsize_Data)

    #parameter n
    n = 20
    RSI = compute_RSI(open_history, n)
    #print(RSI) #印出後發現取的時間長會介於50~70，取的時間短會介於40~80之間、
    #調整參數後得到取20天時最佳結果，並取RSI超買/超賣界定值分別為60, 70

    #parameter a, b
    a, b  = 0, 20
    #如果是RSI_value > 80 or RSI_value < 50  ==> final: 20
    # RSI_value > 50 or RSI_value < 20
    if RSI <= 60 and short_MA > long_MA and ((openPricev - weight_ma) > a or trend == 1) :
        action = 1
    elif RSI >= 70 and short_MA < long_MA and ((openPricev - weight_ma) < -b or trend == -1):
        action = -1
    else:
        action = 0
    return action

# 221
#baseline method: sma,lma交叉, 昨日開盤價與今日開盤價差
#final 160
# def myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev):
#     open_history = dailyOhlcvFile['open'].tail(4).values
#     open_history2 = dailyOhlcvFile['open'].tail(19).values
#     #print(open_history)
#     today_price = openPricev
#     sum1 = 0
#     sum2 = 0
#     for i in open_history:
#         sum1 +=i
#     for i in open_history2:
#         sum2 +=i
#     sum1 += today_price
#     sum2 += today_price
#     short_MA = sum1/5
#     long_MA = sum2/20
#     if open_history[-1] < today_price or short_MA > long_MA:
#         action = 1
#     elif open_history[-1] > today_price or short_MA < long_MA:
#         action = -1
#     else:
#         action = 0
#     return action


# final: 160
# +最近三天連續漲/跌
# def myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev):
#     open_history = dailyOhlcvFile['open'].tail(4).values
#     open_history2 = dailyOhlcvFile['open'].tail(19).values
#     #print(open_history)
#     today_price = openPricev
#     sum1 = 0
#     sum2 = 0
#     for i in open_history:
#         sum1 +=i
#     for i in open_history2:
#         sum2 +=i
#     sum1 += today_price
#     sum2 += today_price
#     short_MA = sum1/5
#     long_MA = sum2/20
#     #距預測日最近3天的股票開盤價是否有連續漲/跌三天
#     O1 = open_history[-3] - open_history[-4]
#     O2 = open_history[-2] - open_history[-3]
#     O3 = open_history[-1] - open_history[-2]
#     if O1 > 0 and O2 > 0 and O3 > 0:
#         trend = 1
#     elif O1 < 0 and O2 < 0 and O3 < 0:
#         trend = -1
#     else:
#         trend = 0
#
#     if open_history[-1] < today_price or short_MA > long_MA or trend == 1:
#         action = 1
#     elif open_history[-1] > today_price or short_MA < long_MA or trend == -1:
#         action = -1
#     else:
#         action = 0
#     return action

#final: 202
# + RSI i=20
# def myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev):
#     open_history = dailyOhlcvFile['open'].values
#     RSI_value = compute_RSI(dailyOhlcvFile['open'].values, 29)
#     open_history4 = open_history[-4:] #最後4天開盤價
#     open_history19 = open_history[-19:] #最後19天開盤價
#     sum1 = sum(open_history4)
#     sum1 += openPricev
#     sum2 = sum(open_history19)
#     sum2 += openPricev
#     #短線操作(均線法): 5MA、20MA
#     short_MA = sum1 / 5
#     long_MA = sum2 / 20
#
#     #距預測日最近3天的股票開盤價是否有連續漲/跌三天
#     O1 = open_history[-3] - open_history[-4]
#     O2 = open_history[-2] - open_history[-3]
#     O3 = open_history[-1] - open_history[-2]
#     if O1 > 0 and O2 > 0 and O3 > 0:
#         trend = 1
#     elif O1 < 0 and O2 < 0 and O3 < 0:
#         trend = -1
#     else:
#         trend = 0
#
#     if  short_MA > long_MA and (RSI_value < 20 or RSI_value > 50)  and trend == 1:
#         action = 1
#     elif short_MA > long_MA and (RSI_value > 80 or RSI_value < 50) and trend == -1:
#         action = -1
#     else:
#         action = 0
#     return action

#242
# final 272 +前一天開始算的KD -sma lma 交叉
def myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev):
    open_history = dailyOhlcvFile['open'].values
    RSI_value = compute_RSI(dailyOhlcvFile['open'].values, 20)
    open_history4 = open_history[-4:] #最後4天開盤價
    open_history19 = open_history[-19:] #最後19天開盤價
    sum1 = sum(open_history4)
    sum1 += openPricev
    sum2 = sum(open_history19)
    sum2 += openPricev
    #短線操作(均線法): 5MA、20MA
    short_MA = sum1 / 5
    long_MA = sum2 / 20

    #距預測日最近3天的股票開盤價是否有連續漲/跌三天
    O1 = open_history[-3] - open_history[-4]
    O2 = open_history[-2] - open_history[-3]
    O3 = open_history[-1] - open_history[-2]
    if O1 > 0 and O2 > 0 and O3 > 0:
        trend = 1
    elif O1 < 0 and O2 < 0 and O3 < 0:
        trend = -1
    else:
        trend = 0

    kk = 50 #initial K值
    dd = 50 #initial D值
    a1 = 0 #count 9 days

    #for today
    highest1 = []
    lowest1 = []
    #for yesterday
    highest2 = []
    lowest2 = []
    #抓取最高價/最低價資料
    low = dailyOhlcvFile['low']
    high = dailyOhlcvFile['high']
    today_price = openPricev

    #取預測日前一天的收盤價
    # open 跟 close rr都為155
    yesterday_price = dailyOhlcvFile['open'].tail(1).values[0]

    for i in range(len(dailyOhlcvFile)-1,0,-1):
        if i > 0:
            if a1<=9:
                #預測日的最近9天最高/低價
                highest1.append(high[i])
                lowest1.append(low[i])
                #預測日昨日的最近9天最高/低價
                highest2.append(high[i-1])
                lowest2.append(low[i-1])
            a1+=1
        else:
            break
    highest1 = max(highest1)
    lowest1 = min(lowest1)
    highest2 = max(highest2)
    lowest2 = min(lowest2)

    yesterdayRSV = (yesterday_price-lowest2)/(highest2-lowest2)*100
    todayRSV = (today_price-lowest1)/(highest1-lowest1)*100
    # RSI_value = RSI(dailyOhlcvFile['open'].values, 29)

    #RSV formula:(今日收盤價 - 最近九天的最低價)/(最近九天的最高價 - 最近九天最低價)
    #當日K值: 昨日K值 * 2/3 + 當日RSV * 1/3
    k1 = kk*2/3+yesterdayRSV*1/3 #yesterday K
    k2 = k1*2/3+todayRSV*1/3 #today K

    #當日D值: 昨日D值 * 2/3  + 當日K值 * 1/3
    d1 = dd*2/3 + k1*1/3 #yesterdat D
    d2= d1*2/3 + k2*1/3 #today D


    # 依據KD指標決定action
    # 只從前一天開始製作KD
    if ((k1<d1 and k2>d2) or (k2<20 and d2<20)) or (RSI_value <= 60) or trend == 1:
        action = 1
    elif ((k1>d1 and k2<d2) or (k2>80 and d2>80)) or (RSI_value >= 70) or trend == -1:
        action = -1
    else:
        action = 0
    return action

#271
#final 160 with KD
# def myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev, i):
#     open_history = dailyOhlcvFile['open'].tail(4).values
#     open_history2 = dailyOhlcvFile['open'].tail(19).values
#     today_price = openPricev
#     sum1 = 0
#     sum2 = 0
#     for i in open_history: #sum1 for 最近四天資料
#         sum1 += i
#     for i in open_history2: #sum2 for 最近19天資料
#         sum2 += i
#     sum1 += today_price
#     sum2 += today_price
#     short_MA = sum1 / 5 #5日均線
#     long_MA = sum2 / 20 #20日均線
#
#     kk = 50  # initial K值
#     dd = 50  # initial D值
#     a1 = 0  # count for 9 days
#
#     # for today
#     highest1 = []
#     lowest1 = []
#     # for yesterday
#     highest2 = []
#     lowest2 = []
#     # 抓取最高價/最低價資料
#     low = dailyOhlcvFile['low']
#     high = dailyOhlcvFile['high']
#
#
#     # 取預測日前一天的收盤價
#     # open 跟 close rr都為155
#     yesterday_price = dailyOhlcvFile['open'].tail(1).values[0]
#
#     for i in range(len(dailyOhlcvFile) - 1, 0, -1):
#         if i > 0:
#             if a1 <= 9:
#                 # 預測日的最近9天最高/低價
#                 highest1.append(high[i])
#                 lowest1.append(low[i])
#                 # 預測日昨日的最近9天最高/低價
#                 highest2.append(high[i - 1])
#                 lowest2.append(low[i - 1])
#             a1 += 1
#         else:
#             break
#     highest1 = max(highest1)
#     lowest1 = min(lowest1)
#     highest2 = max(highest2)
#     lowest2 = min(lowest2)
#
#     yesterdayRSV = (yesterday_price - lowest2) / (highest2 - lowest2) * 100
#     todayRSV = (today_price - lowest1) / (highest1 - lowest1) * 100
#     RSI_value = RSI(dailyOhlcvFile['open'].values, i)


    # RSV formula:(今日收盤價 - 最近九天的最低價)/(最近九天的最高價 - 最近九天最低價)
    # 當日K值: 昨日K值 * 2/3 + 當日RSV * 1/3
    # k1 = kk * 2 / 3 + yesterdayRSV * 1 / 3  # yesterday K
    # k2 = k1 * 2 / 3 + todayRSV * 1 / 3  # today K
    #
    # # 當日D值: 昨日D值 * 2/3  + 當日K值 * 1/3
    # d1 = dd * 2 / 3 + k1 * 1 / 3  # yesterdat D
    # d2 = d1 * 2 / 3 + k2 * 1 / 3  # today D
    #
    # if short_MA > today_price or short_MA > long_MA or k1 < d1 and (RSI_value < 20 or RSI_value > 50):
    #     if k2 > d2 or (k2 > 80 and d2 > 80):
    #         action = 1
    #     else:
    #         action = 0
    # elif k1 > d1 or short_MA < today_price or short_MA < long_MA and (RSI_value > 80 or RSI_value < 50):
    #     if k2 < d2 or (k2 < 20 and d2 < 20):
    #         action = -1
    #     else:
    #         action = 0
    # else:
    #     action = 0
    # return action

    #220
    #final 153
    # if short_MA > today_price and short_MA > long_MA and k1 < d1:
    #     if k2 > d2:
    #         action = 1
    #     elif k2 < d2:
    #         if k2 > 80 or d2 > 80:
    #             action = 1
    #         elif k2 < 20 or d2 < 20:
    #             action = -1
    #         else:
    #             action = -1
    # elif short_MA < today_price and short_MA < long_MA and k1 > d1:
    #     if k2 < d2:
    #         if k2 > 80 or d2 > 80:
    #             action = 1
    #         elif k2 < 20 or d2 < 20:
    #             action = -1
    #         else:
    #             action = -1
    #     elif k2 > d2:
    #         action = 1
    # else:
    #     action = 0
    # return action

    # dict = {'RSV':RSV_list,'K': k, 'D': d}
    # df = pd.DataFrame(dict)
    # df.to_csv('fintechKD.csv', sep=",")


# final: 46
def myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev):
    k = [] #存放history k值
    d = [] #存放history d值
    RSV_list = [] #存放history RSV值
    kk = 50 #initial K值
    dd = 50 #initial D值
    a1 = 0 #count 9 days

    #for today
    highest1 = []
    lowest1 = []
    #for yesterday
    highest2 = []
    lowest2 = []
    #for history
    highest3 = []
    lowest3 = []
    #抓取最高價/最低價資料
    low = dailyOhlcvFile['low']
    high = dailyOhlcvFile['high']
    today_price = openPricev
    #open 跟 close rr都為155
    #取預測日之前的所有收盤價
    topdown_history_price = dailyOhlcvFile['open']
    history_price = []
    for i in range(len(topdown_history_price)-1,0,-1):
        history_price.append(topdown_history_price[i])

    #取預測日前一天的收盤價
    #yesterday_price = dailyOhlcvFile['close'].tail(1).values[0]

    for i in range(len(dailyOhlcvFile)-1,0,-1):
        if i > 0:
            if a1<=9:
                #預測日的最近9天最高/低價
                highest1.append(high[i])
                lowest1.append(low[i])
                #預測日昨日的最近9天最高/低價
                #highest2.append(high[i-1])
                #lowest2.append(low[i-1])
            a1+=1
        else:
            break
    highest1 = max(highest1)
    lowest1 = min(lowest1)
    #highest2 = max(highest2)
    #lowest2 = min(lowest2)

    #yesterdayRSV = (yesterday_price-lowest2)/(highest2-lowest2)*100
    todayRSV = (today_price-lowest1)/(highest1-lowest1)*100

    history_high = []
    history_low = []
    for i in range(len(dailyOhlcvFile)-1,0,-1):
        a = 0  # count 9 days
        #print(i)
        for x in range(0,len(dailyOhlcvFile)-1,1):
            if a<=9:
                #print(x)
                if i-x > 0:
                    highest3.append(high[i-x])
                    lowest3.append(low[i-x])
                    a += 1
                elif i-x == 0:
                    highest3.append(high[i-x])
                    lowest3.append(low[i-x])
                    a += 1
                else:
                    break
            else:
                break
        highest33 = max(highest3)
        lowest33 = min(lowest3)
        history_high.append(highest33)
        history_low.append(lowest33)
    highest33 = max(highest3)
    lowest33 = min(lowest3)
    history_high.append(highest33)
    history_low.append(lowest33)

    # print(history_high[0])
    # print('/n')
    # print(history_low[0])
    # print('/n')
    # print(history_price[0])

    #RSV formula:(今日收盤價 - 最近九天的最低價)/(最近九天的最高價 - 最近九天最低價)
    history = []
    for i in range(len(history_price)):
        history.append(history_price[i])
    for i in range(len(history)):
        historyRSV = 100*(history[i]-history_low[i])/(history_high[i]-history_low[i])
        RSV_list.append(historyRSV)
    #print(len(RSV_list))
    #print(yesterdayRSV)
    #print(todayRSV)

    #當日K值: 昨日K值 * 2/3 + 當日RSV * 1/3
    # k1 = kk*2/3+yesterdayRSV*1/3 #yesterday K
    # k2 = k1*2/3+todayRSV*1/3 #today K

    #當日D值: 昨日D值 * 2/3  + 當日K值 * 1/3
    # d1 = dd*2/3 + k1*1/3 #yesterdat D
    # d2= d1*2/3 + k2*1/3 #today D

    for i in range(len(RSV_list)):
        k3 = kk*2/3+RSV_list[i]*1/3
        k.append(k3)
    for i in range(len(k)):
        d3 = dd*2/3+k[i]*1/3
        d.append(d3)


    #依據KD指標決定action

    #只從前一天開始製作KD
    #第一個為or時=155，為and時=13
    #為or且反指標時=368，為and且反指標時=507

    # if k1<d1:
    #     if k2>d2 or (k2>80 or d2>80):
    #         action = 1
    #     else:
    #         action= -1
    # elif k1>d1:
    #     if k2<d2 or (k2<20 or d2<20):
    #         action = -1
    #     else:
    #         action = 1
    # else:
    #     action = 0
    # return action

    #從所有history資料開始做KD
    #昨日KD
    K1 = k[len(k)-1] #2199
    D1 = d[len(d)-1]
    #前天KD
    K2 = k[len(k)-2] #2198
    D2 = d[len(d)-2]
    #大前天KD
    K3 = k[len(k)-3] #2197
    D3 = d[len(d)-3]
    #今日KD
    k2 = K1 * 2 / 3 + todayRSV * 1 / 3  # today K
    d2 = D1 * 2 / 3 + k2 * 1 / 3  # today D
    #連續K的差
    A = k2 - K1 #今天跟昨天差
    B = K1 - K2 #昨天跟前天差
    C = K2 - K3 #前天跟大前天差
    #連續D的差
    A2 = d2 - D1 #今天跟昨天差
    B2 = D1 - D2 #昨天跟前天差
    C2 = D2 - D3 #前天跟大前天差

    # dict = {'RSV':RSV_list,'K': k, 'D': d}
    # df = pd.DataFrame(dict)
    # df.to_csv('fintechKD.csv', sep=",")

    # print(k2)
    # print(d2)
    # print('/n')

    if K1<D1 or (A>0 and B>0 and C>0) or (A2>0 and B2>0 and C2>0):
        if k2>d2:
            if k2>80 or d2>80:
                action = 1
            elif k2 < 20 or d2 < 20:
                action = -1
            else:
                action = 1
        else:
                action = -1
    elif K1>D1 or (A<0 and B<0 and C<0) or (A2<0 and B2<0 and C2<0):
        if k2<d2:
            if k2<20 or d2<20:
                action = -1
            elif k2>80 or d2>80:
                action = 1
            else:
                action = -1
        else:
                action = 1
    else:
        action = 0
    return action



