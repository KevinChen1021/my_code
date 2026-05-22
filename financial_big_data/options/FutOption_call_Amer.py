"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def FutOption_call_Amer(F, K, sigma, r, T, N):
    """
    N步二叉树计算美式看涨期货期权价格
    F: 期货合约当前价格
    K: 期权行权价格
    sigma: 期货收益率年化波动率
    r: 无风险收益率
    T: 期权期限（年）
    N: 二叉树步数
    """
    t = T / N  # 每步期限（年）
    u = np.exp(sigma * np.sqrt(t))  # 期货价格上涨比例
    d = 1 / u  # 期货价格下跌比例
    p = (1 - d) / (u - d)  # 上涨概率
    call_matrix = np.zeros((N+1, N+1))  # 存储期权价值的矩阵

    # 到期节点价值
    N_list = np.arange(0, N+1)
    F_end = F * np.power(u, N - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(F_end - K, 0)

    # 倒推计算非到期节点价值
    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i+1)
        for j in j_list:
            Fi = F * np.power(u, i - j) * np.power(d, j)
            call_strike = np.maximum(Fi - K, 0)  # 提前行权收益
            # 不提前行权的价值（折现）
            call_nostrike = np.exp(-r*t) * (p*call_matrix[i+1, j+1] + (1-p)*call_matrix[i+1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)
    return call_matrix[0, 0]
