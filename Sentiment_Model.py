#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Sentiment_Model.py
# @Time      :2022/5/1 19:39
# @Author    :Colin
# @Note      :None
import pandas as pd

from Data_Generate import MyData


class BWSentiment:
    def __init__(self):
        self.df_sen = pd.DataFrame()
        self.data_define()
        self.data_cal()

    # 数据收集
    def data_define(self):
        index_1 = ['firm_size_age', 'profitability', 'dividends', 'asset_tangibility', 'growth_opportunities_distress']
        index_2 = ['date', 'P', 'R', 'R-sigma', 'ME', 'Age', 'E', 'E+', 'BE', 'E+/BE', 'D', 'D/BE']

        self.df_sen = MyData(20, index_2).date_df

    # 数据计算
    def data_cal(self):
        self.df_sen = self.df_sen.sort_values(by='date')
        # self.df_sen.loc[:, 'P_1'] = self.df_sen['P'].shift(1)
        self.df_sen.loc[:, 'R'] = (self.df_sen['P'] - self.df_sen['P'].shift(1)) / self.df_sen['P'].shift(1)
        self.df_sen.loc[:, 'R-sigma'] = self.df_sen['R'].std()
        self.df_sen.loc[self.df_sen.E <= 0, 'E+'] = 0
        self.df_sen.loc[self.df_sen.E > 0, 'E+'] = 1
        self.df_sen.loc[:, 'E+/BE'] = self.df_sen['E+'] / self.df_sen['BE']
        self.df_sen.loc[:, 'D/BE'] = self.df_sen['D'] / self.df_sen['BE']

    # 数据收集
    def load_data(self):
        return

    def clean_data(self):
        return

    def analysis_data(self):
        return

    def date(self):
        return


if __name__ == "__main__":
    BW = BWSentiment()
    # BW.df_sen.to_csv('BW.csv')
    df = BW.df_sen
    print(df['date'])
