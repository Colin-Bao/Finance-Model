import BSM_Model

if __name__ == '__main__':
    # 用K，S，t完成初始化
    BSM = BSM_Model.BSM(60, '000651.sz',
                        {'start_date': '20200101', 'end_date': '20210101', 'expiry_day': '20210101'})
    # 可视化
    # BSM.show_data('kline', BSM.df_kline)
    BSM.show_data('my', (50, 25, 1, 0.03, 0.3))
