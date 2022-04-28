import BSM_Model
import KMV_Model

if __name__ == '__main__':
    BSM_new = BSM_Model.BSM(100, '000651.sz',
                            {'start_date': '20200101', 'end_date': '20210101', 'expiry_day': '20220101'})
    # print(BSM_new.df_kline)
    # KMV_new = KMV_Model.KMV(100, '000651.sz',
    #                         {'start_date': '20200101', 'end_date': '20210101', 'expiry_day': '20220101'},
    #                         154527413000, 3354563900, 6015730900)
    # print(KMV_new.bs_call, KMV_new.bs_put, KMV_new.DD, KMV_new.PD, KMV_new.S, KMV_new.Share_MV)
