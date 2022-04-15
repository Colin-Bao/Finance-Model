import tushare as ts

ts.set_token('0c996bdea9d77679946a1c85dc2ee87b60dfad62b2d15f0f9a312603')
pro = ts.pro_api()


# 查询当前所有正常上市交易的股票列表


def get_shares_list():
    return pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
