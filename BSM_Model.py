from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import DataFrame
import ASHARE_Select


class BSM:
    S, K, T, r, sigma = 0.0, 0.0, 0.0, 0.0, 0.0
    share_name = None
    df_kline = None
    date_dict = {'start_date': '', 'end_date': '', 'expiry_day': ''}

    d1 = 0.0
    d2 = 0.0
    bs_call = 0.0
    bs_put = 0.0

    def __init__(self, K, share_name, date_dict):
        # ----------- 自定义参数 ---------#
        self.K = K
        self.share_name = share_name
        self.date_dict = date_dict

        # 需要计算的参数
        self.df_kline = self.get_kline()
        self.S = self.cal_s()
        self.sigma = self.cal_sigma()
        self.r = self.cal_r()
        self.t = self.cal_t()

        # 计算期权
        self.cal_bs_put(self.S, self.K, self.T, self.r, self.sigma)
        self.cal_bs_call(self.S, self.K, self.T, self.r, self.sigma)

    @classmethod
    def today(cls, K, share_name):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        one_year_ago = now.replace(year=now.year - 1).strftime('%Y%m%d')
        return cls(K, share_name, {'start_date': one_year_ago, 'end_date': today})

    def get_kline(self):
        return ASHARE_Select.TuShareGet(self.date_dict['start_date'], self.date_dict['end_date']).get_kline(
            self.share_name)

    def cal_s(self):
        # print(self.df_kline.iloc[-1]['pre_close'])
        return self.df_kline.iloc[-1]['pre_close']  # 取出最后一行数据（最新的）

    def cal_sigma(self):
        return np.sqrt(252) * self.df_kline['return'].std()

    def cal_r(self):
        risk_free_year = ASHARE_Select.TuShareGet.today().get_shibor()
        risk_free_year_now = risk_free_year.iloc[-1]['1y'] / 100.0
        self.r = risk_free_year_now
        return risk_free_year_now

    def cal_t(self):
        t = (datetime.strptime(self.date_dict['expiry_day'], "%Y%m%d") - datetime.strptime(
            self.date_dict['end_date'], "%Y%m%d")).days / 365.0
        self.T = t
        return t

    def cal_d1(self, S, K, T, r, sigma):
        self.d1 = (log(S / K) + (r + sigma ** 2 / 2.0) * T) / (sigma * sqrt(T))
        return self.d1

    def cal_d2(self, S, K, T, r, sigma):
        self.d2 = self.cal_d1(S, K, T, r, sigma) - sigma * sqrt(T)
        return self.d2

    def cal_bs_call(self, S, K, T, r, sigma):
        self.d1 = self.cal_d1(S, K, T, r, sigma)
        self.d2 = self.cal_d2(S, K, T, r, sigma)

        bs_call = S * norm.cdf(self.d1) - K * exp(-r * T) * norm.cdf(self.d2)
        self.bs_call = bs_call
        return bs_call

    def cal_bs_put(self, S, K, T, r, sigma):
        self.bs_put = K * exp(-r * T) - S + self.cal_bs_call(S, K, T, r, sigma)
        return self.bs_put

    def get_result(self):
        return [self.S, self.K, self.T, self.r, self.sigma, self.bs_call, self.bs_put]

    def get_all_name(self):
        return vars(self).keys()
