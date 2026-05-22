"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def BTM_Nstep(S, K, sigma, r, T, N, types):
    '''运用N步二叉树模型计算欧式期权价值
    S: 基础资产当前价格
    K: 期权行权价格
    sigma: 基础资产年化波动率
    r: 连续复利无风险收益率
    T: 期权期限（年）
    N: 二叉树步数
    types: 期权类型（'call'=看涨，其他=看跌）'''
    from numpy import exp, maximum, sqrt
    t = T / N  # 每一步的步长期限（年）
    u = exp(sigma * sqrt(t))  # 价格上涨比例
    d = 1 / u  # 价格下跌比例
    p = (exp(r * t) - d) / (u - d)  # 风险中性概率
    N_list = range(0, N + 1)
    A = []

    for j in N_list:
        # 计算到期日某节点的期权价值
        C_Nj = maximum(S * pow(u, j) * pow(d, N - j) - K, 0)
        # 计算到达该节点的路径数量
        Num = factorial(N) / (factorial(j) * factorial(N - j))
        A.append(Num * pow(p, j) * pow(1 - p, N - j) * C_Nj)

    # 计算看涨期权价值
    call = exp(-r * T) * sum(A)
    # 运用看跌-看涨平价关系计算看跌期权价值
    put = call + K * exp(-r * T) - S

    if types == 'call':
        value = call
    else:
        value = put
    return value
