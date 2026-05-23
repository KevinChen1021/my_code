"""Function module for american_put."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def american_put(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps):
    """Compute american_put."""
    t = time_to_maturity / steps  # 步长期限
    u = np.exp(volatility * np.sqrt(t))  # 价格上涨比例
    d = 1 / u  # 价格下跌比例
    p = (np.exp(interest_rate * t) - d) / (u - d)  # 风险中性概率
    put_matrix = np.zeros((steps + 1, steps + 1))  # 存储节点期权价值的矩阵

    # 计算到期日节点的基础资产价格与期权价值
    N_list = np.arange(0, steps + 1)
    S_end = spot_price * np.power(u, steps - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(strike_price - S_end, 0)

    # 倒推计算非到期日节点的期权价值
    i_list = list(range(0, steps))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = spot_price * np.power(u, i - j) * np.power(d, j)  # 当前节点基础资产价格
            put_strike = np.maximum(strike_price - Si, 0)  # 提前行权收益
            # 不提前行权的期权价值（折现）
            put_nostrike = np.exp(-interest_rate * t) * (p * put_matrix[i + 1, j + 1] + (1 - p) * put_matrix[i + 1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)  # 取最大值

    put_begin = put_matrix[0, 0]  # 初始期权价值
    return put_begin
