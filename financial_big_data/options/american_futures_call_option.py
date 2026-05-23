"""Function module for american_futures_call_option."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def american_futures_call_option(forward_price, strike_price, volatility, interest_rate, time_to_maturity, steps):
    """
    N步二叉树计算美式看涨期货期权价格
    F: 期货合约当前价格
    K: 期权行权价格
    sigma: 期货收益率年化波动率
    r: 无风险收益率
    T: 期权期限（年）
    N: 二叉树步数
    """
    t = time_to_maturity / steps  # 每步期限（年）
    u = np.exp(volatility * np.sqrt(t))  # 期货价格上涨比例
    d = 1 / u  # 期货价格下跌比例
    p = (1 - d) / (u - d)  # 上涨概率
    call_matrix = np.zeros((steps+1, steps+1))  # 存储期权价值的矩阵

    # 到期节点价值
    N_list = np.arange(0, steps+1)
    F_end = forward_price * np.power(u, steps - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(F_end - strike_price, 0)

    # 倒推计算非到期节点价值
    i_list = list(range(0, steps))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i+1)
        for j in j_list:
            Fi = forward_price * np.power(u, i - j) * np.power(d, j)
            call_strike = np.maximum(Fi - strike_price, 0)  # 提前行权收益
            # 不提前行权的价值（折现）
            call_nostrike = np.exp(-interest_rate*t) * (p*call_matrix[i+1, j+1] + (1-p)*call_matrix[i+1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)
    return call_matrix[0, 0]
