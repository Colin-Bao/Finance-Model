import BSM_Model
from scipy.stats import norm
from math import log, sqrt


class KMV(BSM_Model.BSM):
    # -------- KMV模型需要扩展的参数 --------#
    Debt_Short = 0.0
    Debt_Long = 0.0
    Share_Amount = 0.0

    # 计算的参数
    Debt_Total = 0.0
    Share_MV = 0.0
    DD = 0.0
    PD = 0.0
    d1_KMV = 0.0
    d2_KMV = 0.0

    # 从BSM父类继承方法和属性#
    def __init__(self, K, share_name, date_dict, Debt_Short, Debt_Long, Share_Amount):
        super().__init__(K, share_name, date_dict)
        self.Debt_Short, self.Debt_Long, self.Share_Amount = Debt_Short, Debt_Long, Share_Amount

        # 计算股权价值
        self.Share_MV = Share_Amount * self.S
        # 计算债权价值
        self.Debt_Total = Debt_Short + 0.5 * Debt_Long

        # 计算新的DD
        self.DD = self.cal_DD()

        # 计算PD
        self.PD = self.cal_PD()

    def cal_d1_KMV(self, S, K, T, r, sigma):
        self.d1_KMV = (log(S / K) + (r + sigma ** 2 / 2.0) * T) / (sigma * sqrt(T))
        return self.d1_KMV

    def cal_d2_KMV(self, S, K, T, r, sigma):
        self.d2_KMV = self.cal_d1_KMV(S, K, T, r, sigma) - sigma * sqrt(T)
        return self.d2_KMV

    # 把股权价值换成股价，债务价值换成K
    def cal_DD(self):
        return self.cal_d2_KMV(self.Share_MV, self.Debt_Total, self.T, self.r, self.sigma)

    def cal_PD(self):
        return norm.cdf(-self.d2_KMV)
