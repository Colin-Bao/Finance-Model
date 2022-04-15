from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import DataFrame
import ASHARE_Select


class BSMCalculate:
    S, K, T, r, sigma = 0.0, 0.0, 0.0, 0.0, 0.0
    share_name = None
    df_kline = None
    bs_call = 0.0
    bs_put = 0.0

    def __init__(self, K, share_name):
        self.K = K
        self.share_name = share_name

        # 需要计算的参数
        self.df_kline = self.get_kline()
        self.S = self.cal_s()
        self.sigma = self.cal_sigma()
        self.cal_r()
        self.cal_t()

        # 计算期权
        self.cal_bs_put(self.S, self.K, self.T, self.r, self.sigma)
        self.cal_bs_call(self.S, self.K, self.T, self.r, self.sigma)

    def get_kline(self):
        return ASHARE_Select.TuShareGet.today().get_kline(self.share_name)

    def cal_s(self):
        return self.df_kline.iloc[-1]['pre_close']  # 取出最后一行数据（最新的）

    def cal_sigma(self):
        return np.sqrt(252) * self.df_kline['return'].std()

    def cal_r(self):
        risk_free_year = ASHARE_Select.TuShareGet.today().get_shibor()
        risk_free_year_now = risk_free_year.iloc[-1]['1y'] / 100.0
        self.r = risk_free_year_now
        return risk_free_year_now

    def cal_t(self):
        expiry_day = '20220606'
        t = (datetime.strptime(expiry_day, "%Y%m%d") - datetime.now()).days / 365.0
        self.T = t
        return t

    def cal_bs_call(self, S, K, T, r, sigma):
        # 计算d1和d2
        def cal_d1(S, K, T, r, sigma):
            return (log(S / K) + (r + sigma ** 2 / 2.0) * T) / (sigma * sqrt(T))

        def cal_d2(S, K, T, r, sigma):
            return cal_d1(S, K, T, r, sigma) - sigma * sqrt(T)

        bs_call = S * norm.cdf(cal_d1(S, K, T, r, sigma)) - K * exp(-r * T) * norm.cdf(cal_d2(S, K, T, r, sigma))
        self.bs_call = bs_call
        return bs_call

    def cal_bs_put(self, S, K, T, r, sigma):
        self.bs_put = K * exp(-r * T) - S + self.cal_bs_call(S, K, T, r, sigma)

    def get_result(self):
        return [self.S, self.K, self.T, self.r, self.sigma, self.bs_call, self.bs_put]


result = BSMCalculate(9, '000001.sz')
print(result.get_result())
