from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import DataFrame
import pandas_datareader.data as web
import ASHARE_Select


# 计算d1和d2
def cal_d1(S, K, T, r, sigma):
    return (log(S / K) + (r + sigma ** 2 / 2.) * T) / (sigma * sqrt(T))


def cal_d2(S, K, T, r, sigma):
    return cal_d1(S, K, T, r, sigma) - sigma * sqrt(T)


#
def bs_call(S, K, T, r, sigma):
    return S * norm.cdf(cal_d1(S, K, T, r, sigma)) - K * exp(-r * T) * norm.cdf(cal_d2(S, K, T, r, sigma))


def bs_put(S, K, T, r, sigma):
    return K * exp(-r * T) - S + bs_call(S, K, T, r, sigma)


stock = 'SPY'
expiry = '12-18-2022'
strike_price = 370

df = ASHARE_Select.TuShareGet.today('000001.sz')
print(df.get_kline())

#
# sigma = np.sqrt(252) * df['returns'].std()
# uty = (web.DataReader(
#     "^TNX", 'yahoo', today.replace(day=today.day - 1), today)['Close'].iloc[-1]) / 100
# lcp = df['Close'].iloc[-1]
# t = (datetime.strptime(expiry, "%m-%d-%Y") - datetime.utcnow()).days / 365
#
# print('The Option Price is: ', bs_call(lcp, strike_price, t, uty, sigma))
