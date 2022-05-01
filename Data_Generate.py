#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Data_Generate.py
# @Time      :2022/5/1 20:52
# @Author    :Colin
# @Note      :数据生成的类,返回一个指定 df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class MyData:
    def __init__(self, row, column=2):
        self.date_df = pd.DataFrame()
        # str_column = list(str(range(column)))
        for i in list(range(column)):
            self.date_df[str(i)] = np.random.normal(0, 1, row)

        self.date_df['date'] = pd.date_range(start=datetime.now(), periods=row, freq="-1D")

        # print(self.date_df.columns)
        self.date_plt = plt

    def distri_data(self):
        return self.date_df

    def finance_data(self):
        return self.date_df

    def show_data(self, y_tag=0, pic_type='hist'):
        # print(self.date_df)
        if pic_type == 'scatter':
            self.date_plt.scatter(self.date_df.index, self.date_df[y_tag])
        elif pic_type == 'hist':
            self.date_plt.hist(self.date_df[y_tag], bins=15, rwidth=0.8, density=True)
        # self.date_plt.scatter(self.date_df.index, self.date_df[y_tag])
        self.date_plt.show()
        # return self.date_plt

    def return_result(self):
        return self.date_df
