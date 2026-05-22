"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def value_CB(S, sigma, par, X, Lambda, r, R, Q2, T, N):
    """
    N步二又树模型计算可转换债券价值
    S: 股票初始价格
    sigma: 股票年化波动率
    par: 可转债本金
    X: 转股比例（每份可转债转股数）
    Lambda: 年化违约概率（连续复利）
    r: 无风险收益率
    R: 违约回收率
    Q2: 赎回价格
    T: 可转债期限（年）
    N: 二又树步数
    """
    # 步骤1：计算参数
    t = T / N  # 每步期限（年）
    u = np.exp(np.sqrt((np.power(sigma, 2) - Lambda) * t))  # 股价上涨比例
    d = 1 / u  # 股价下跌比例
    Pu = (np.exp(r * t) - d * np.exp(-Lambda * t)) / (u - d)  # 股价上涨概率
    Pd = (u * np.exp(-Lambda * t) - np.exp(r * t)) / (u - d)  # 股价下跌概率
    P_default = 1 - np.exp(-Lambda * t)  # 违约概率
    D_value = par * R  # 违约回收价值
    CB_matrix = np.zeros((N + 1, N + 1))  # 存储各节点可转债价值的矩阵

    # 步骤2：计算到期节点的可转债价值
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)  # 到期节点股价
    Q1 = par  # 到期不转股/不赎回的本金
    Q3 = X * S_end  # 到期转股价值
    # 到期价值：取（min(本金,赎回价)、转股价值）的最大值
    CB_matrix[:, -1] = np.maximum(np.minimum(Q1, Q2), Q3)

    # 步骤3：倒推计算非到期节点的可转债价值
    i_list = list(range(0, N))
    i_list.reverse()  # 从N-1到0倒推
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)  # 当前节点股价
            # 非违约时的价值（折现后）
            Q1 = np.exp(-r * t) * (Pu * CB_matrix[i + 1, j + 1] + Pd * CB_matrix[i + 1, j] + P_default * D_value)
            Q3 = X * Si  # 当前节点转股价值
            # 当前节点价值：取（min(本金,赎回价)、转股价值）的最大值
            CB_matrix[i, j] = np.maximum(np.minimum(Q1, Q2), Q3)

    V0 = CB_matrix[0, 0]  # 初始价值
    return V0
