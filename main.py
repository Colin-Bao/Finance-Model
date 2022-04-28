import BSM_Model

if __name__ == '__main__':
    BSM_new = BSM_Model.BSM(60, '000651.sz',
                            {'start_date': '20200101', 'end_date': '20210101', 'expiry_day': '20210101'})
    # BSM_new.vis_data()
