from math import log, sqrt, exp
from scipy.stats import norm
from datetime import datetime
import numpy as np
import pandas as pd
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

        # 需要计算的参数 对整个Dataframe运算
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

    def save_data(self, df_kline):
        file_name = self.share_name + '.csv'
        # 储存
        df_kline.to_csv(file_name, index=False)

    def get_kline(self):
        file_name = self.share_name + '.csv'

        try:
            df_kline = pd.read_csv(file_name)

        except FileNotFoundError as e:
            print(e)
            # 需要提前一年的数据计算方差
            start_date = datetime.strptime(self.date_dict['start_date'], '%Y%m%d')
            one_year_ago = start_date.replace(year=start_date.year - 1).strftime('%Y%m%d')

            df_kline = pd.DataFrame(
                ASHARE_Select.TuShareGet(one_year_ago, self.date_dict['end_date']).get_kline(
                    self.share_name))

            # 处理df-kline
            df_kline['trade_date'] = pd.to_datetime(df_kline['trade_date'], format='%Y%m%d')

            # 储存
            df_kline.to_csv(file_name)

        return df_kline

    def cal_s(self):
        # print(self.df_kline.iloc[-1]['pre_close'])
        return self.df_kline.iloc[-1]['pre_close']  # 取出最后一行数据（最新的）

    def cal_sigma(self):

        # 筛选出观测期
        def cal_observe_date(dateframe, end_date):
            start_date = datetime.strptime(end_date, '%Y%m%d')
            # 用提前一年和start_date计算方差
            one_year_ago = start_date.replace(year=start_date.year - 1)

            # 筛选日期
            df_observe = dateframe[(pd.to_datetime(dateframe['trade_date'], format='%Y-%m-%d') <= start_date) & (
                    pd.to_datetime(dateframe['trade_date'], format='%Y-%m-%d') >= one_year_ago)]

            # 使用观测期计算方差
            return np.sqrt(252) * df_observe['return'].std()

        # 筛选出持有期
        def cal_hold_date(dateframe, date_dict):
            # 把日期字符串格式化成可以比较的对象
            start_date = datetime.strptime(date_dict['start_date'], '%Y%m%d')
            end_date = datetime.strptime(date_dict['end_date'], '%Y%m%d')

            # 通过持有期计算sigma
            dateframe['sigma_1y'] = None
            std = cal_observe_date(dateframe, date_dict['start_date'])

            # 筛选日期 loc
            dateframe.loc[(pd.to_datetime(dateframe['trade_date'], format='%Y-%m-%d') <= end_date) & (
                    pd.to_datetime(dateframe['trade_date'], format='%Y-%m-%d') >= start_date), ('sigma_1y',)] = std

            return std

        sigma = cal_hold_date(self.df_kline, self.date_dict)

        # 更新数据
        self.save_data(self.df_kline)

        return sigma

    def cal_r(self):
        risk_free_year = ASHARE_Select.TuShareGet.today().get_shibor()
        risk_free_year_now = risk_free_year.iloc[-1]['1y'] / 100.0
        self.r = risk_free_year_now
        return risk_free_year_now

    # 计算期权到期日
    def cal_t(self):

        # 筛选出持有期
        def cal_hold_date(dateframe, date_dict):
            # 把日期字符串格式化成可以比较的对象
            start_date = datetime.strptime(date_dict['start_date'], '%Y%m%d')
            end_date = datetime.strptime(date_dict['end_date'], '%Y%m%d')

            # 通过持有期计算到期日
            dateframe['expiry_t'] = None

            # 筛选日期 loc
            dateframe.loc[(pd.to_datetime(dateframe['trade_date'], format='%Y-%m-%d') <= end_date) & (
                    pd.to_datetime(dateframe['trade_date'], format='%Y-%m-%d') >= start_date), ('expiry_t',)] = \
                (datetime.strptime(date_dict['expiry_day'], "%Y%m%d") - pd.to_datetime(dateframe['trade_date'],
                                                                                       format='%Y-%m-%d'))

            dateframe['expiry_t'] = pd.to_datetime(dateframe['expiry_t'],
                                                   infer_datetime_format=True) - datetime.strptime(
                '1970-01-01', "%Y-%m-%d")
            dateframe['expiry_t'] = dateframe['expiry_t'].astype('timedelta64[D]').astype('float') / 365.0

        cal_hold_date(self.df_kline, self.date_dict)

        # 更新数据
        self.save_data(self.df_kline)

        t = (datetime.strptime(self.date_dict['expiry_day'], "%Y%m%d") - datetime.strptime(
            self.date_dict['end_date'], "%Y%m%d")).days / 365.0
        self.T = t
        return t

    def cal_d1(self, S, K, T, r, sigma):
        self.d1 = (log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * sqrt(T))

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
