import BSM_Model
from scipy.stats import norm


class KMV(BSM_Model.BSM):
    # -------- KMV模型需要扩展的参数 --------#
    Debt_Short = 0.0
    Debt_Long = 0.0
    Share_Amount = 0.0

    # 计算的参数
    Share_MV = 0.0
    DD = 0.0
    PD = 0.0

    # 从BSM父类继承方法和属性#
    def __init__(self, K, share_name, date_dict, Debt_Short, Debt_Long, Share_Amount):
        super().__init__(K, share_name, date_dict)
        self.Debt_Short, self.Debt_Long, self.Share_Amount = Debt_Short, Debt_Long, Share_Amount

        # 计算股权价值
        self.Share_MV = self.Share_Amount * self.S

        # 计算新的DD
        self.DD = self.cal_DD

        # 计算PD
        self.PD = self.cal_PD

    def cal_DD(self):
        return self.d2

    def cal_PD(self):
        return norm.cdf(-self.d2)


KMV_new = KMV(100, '000001.sz', {'start_date': '20200101', 'end_date': '20210101', 'expiry_day': '20220101'},
              154527413000, 3354563900, 6015730900)
print(KMV_new.bs_call, KMV_new.bs_put, KMV_new.DD)
