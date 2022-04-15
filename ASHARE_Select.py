import tushare as ts
from datetime import datetime


# 用于给其他文件调用的类

class TuShareGet:
    __TOKEN = None
    ts_code = None
    start_date = None
    end_date = None
    data_df = None

    def __init__(self, start_date, end_date):
        self.start_date, self.end_date = start_date, end_date
        self.__TOKEN = '0c996bdea9d77679946a1c85dc2ee87b60dfad62b2d15f0f9a312603'
        ts.set_token(self.__TOKEN)
        self.pro = ts.pro_api()

    @classmethod
    def today(cls):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        one_year_ago = now.replace(year=now.year - 1).strftime('%Y%m%d')
        return cls(one_year_ago, today)

    def get_shares_list(self):
        return self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    def get_kline(self, ts_code, flag_return=True):
        def cal_return(df):
            # print(self.start_date)
            cal_df = df.sort_values(by="trade_date").dropna()
            cal_df = cal_df.assign(close_day_before=cal_df.pre_close.shift(1))
            cal_df['return'] = ((cal_df.pre_close - cal_df.close_day_before) / cal_df.close_day_before)
            return cal_df

        self.ts_code = ts_code
        self.data_df = self.pro.daily(ts_code=self.ts_code, start_date=self.start_date, end_date=self.end_date)

        if flag_return:
            self.data_df = cal_return(self.data_df)

        return self.data_df

    def get_shibor(self):
        return self.pro.shibor(start_date=self.start_date, end_date=self.end_date)
