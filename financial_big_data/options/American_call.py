"""Function module for american_call."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def american_call(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps):
    """Compute american_call."""
    t = time_to_maturity / steps  # 步长期限
    u = np.exp(volatility * np.sqrt(t))  # 价格上涨比例
    d = 1 / u  # 价格下跌比例
    p = (np.exp(interest_rate * t) - d) / (u - d)  # 风险中性概率
    call_matrix = np.zeros((steps + 1, steps + 1))  # 存储节点期权价值的矩阵

    # 计算到期日节点的基础资产价格与期权价值
    N_list = np.arange(0, steps + 1)
    S_end = spot_price * np.power(u, steps - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(S_end - strike_price, 0)

    # 倒推计算非到期日节点的期权价值
    i_list = list(range(0, steps))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = spot_price * np.power(u, i - j) * np.power(d, j)  # 当前节点基础资产价格
            call_strike = np.maximum(Si - strike_price, 0)  # 提前行权收益
            # 不提前行权的期权价值（折现）
            call_nostrike = np.exp(-interest_rate * t) * (p * call_matrix[i + 1, j + 1] + (1 - p) * call_matrix[i + 1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)  # 取最大值

    call_begin = call_matrix[0, 0]  # 初始期权价值
    return call_begin
