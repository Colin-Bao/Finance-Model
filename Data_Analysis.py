#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Data_Analysis.py
# @Time      :2022/5/1 22:46
# @Author    :Colin
# @Note      :None
from datetime import datetime
import numpy as np
from scipy.stats import norm
from math import log, sqrt, exp
import pandas as pd
import Data_Generate


# 存储 df 并进行计算
class DA:
    # 自定义计算函数 sqrt exp log cdf
    class Cal:
        def __init__(self, para, df_num):
            self.result = self.cal(para)(df_num)

        def cal(self, para):
            function_name = 'cal_' + para
            method = getattr(self, function_name)
            return method

        def cal_log(self, df_num):
            self.result = df_num.apply(lambda x: log(x) if x is not np.nan else x)

        def cal_exp(self, df_num):
            self.result = df_num.apply(lambda x: exp(x) if x is not np.nan else x)

        def cal_sqrt(self, df_num):
            self.result = df_num.apply(lambda x: sqrt(x) if x is not np.nan else x)

        def cal_cdf(self, df_num):
            self.result = df_num.apply(lambda x: norm.cdf(x) if x is not np.nan else x)

    def __init__(self, data, date_column=None):

        self.df_DA = data

        # 声明时间序列 需要特殊处理
        if date_column:
            # 声明时间序列
            self.date_column = self.set_date_series(date_column)
            # 声明观测期序列
            # self.observe_column = self.set_observe_series(observe_column)
        else:
            self.date_column = None

    # 声明时间序列
    def set_date_series(self, date_column):
        self.date_column = date_column
        return date_column

    # 控制外部访问的参数计算方法
    def switch_para(self, para):
        function_name = 'cal_' + para
        method = getattr(self, function_name, self.cal_default(para, None, None, None, ))
        return method

    def cal_default(self, para, tar_column, create_column, execute_rule):
        return self.df_DA, para, tar_column, create_column, execute_rule

    # 计算前需要初始化时间序列,或者声明时间序列
    def cal_date_return(self, tar_column, create_column='date_return', execute_rule=None):
        if self.date_column:
            # 按照时间顺序排列
            self.df_DA = self.df_DA.sort_values(by=self.date_column)
            # assign是在新增计算行的时候同时增加
            self.df_DA = self.df_DA.assign(price_before=self.df_DA[tar_column].shift(1))

            cal_result = ((self.df_DA[tar_column] - self.df_DA.price_before) / self.df_DA.price_before)
            # 返回计算好的 df
            self.cal_execute(create_column, cal_result, execute_rule)
            return cal_result
        else:
            # pass
            raise KeyError.args

    # 计算sigma
    def cal_sigma(self, tar_column, create_column='sigma', dt_observe=None, execute_rule=None):
        if self.date_column is None:
            raise TypeError

        if dt_observe:
            # 用提前一年和start_date计算方差
            dt_start = datetime.strptime(dt_observe[0], '%Y%m%d')
            dt_end = datetime.strptime(dt_observe[1], '%Y%m%d')

            # 筛选出观测期row
            df_observe = self.df_DA[
                (pd.to_datetime(self.df_DA[self.date_column], format='%Y-%m-%d') <= dt_end) & (
                        pd.to_datetime(self.df_DA[self.date_column], format='%Y-%m-%d') >= dt_start)]
            # print(df_observe)
            # 使用观测期计算方差
            cal_result = np.sqrt(252) * df_observe[tar_column].std()

        else:
            cal_result = np.sqrt(252) * self.df_DA[tar_column].std()

        self.cal_execute(create_column, cal_result, execute_rule)

        return cal_result

    # 筛选出持有期的所有行执行结果
    def cal_execute(self, create_column, cal_result, execute_rule=None):

        def create_column_dup(name, count):
            if name + '_' + str(count) in self.df_DA.columns:
                count += 1
                return create_column_dup(name, count)
                # return
            else:
                return name + '_' + str(count)

        if create_column in self.df_DA.columns:
            create_column = create_column_dup(create_column, 1)

        # 对指定筛选的行执行修改操作
        if execute_rule:
            if execute_rule['type'] == 'date':
                dt_start, dt_end = datetime.strptime(execute_rule['rule'][0], '%Y%m%d'), datetime.strptime(
                    execute_rule['rule'][1], '%Y%m%d')

                self.df_DA.loc[(pd.to_datetime(self.df_DA[self.date_column], format='%Y-%m-%d') <= dt_end) & (
                        pd.to_datetime(self.df_DA[self.date_column], format='%Y-%m-%d') >= dt_start), (
                                   create_column,)] = cal_result
        # 无条件执行
        else:
            self.df_DA.loc[:, (create_column,)] = cal_result

        return self.df_DA


if __name__ == "__main__":
    df = DA(Data_Generate.MyData(20, 1).return_result(), 'date')
    df.switch_para('date_return')('0')
    df.switch_para('sigma')('date_return')

    # df.switch_para('sigma')('date_return', ['20220413', '20220423'],
    #                         {'type': 'date', 'rule': ['20220423', '20220503']})

    print(df.df_DA)
