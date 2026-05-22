"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def BTM_Nstep(S, K, sigma, r, T, N, types):
    t = T / N  # 每一步长时期限（年）
    u = exp(sigma * sqrt(t))  # 基础资产价格上涨比例
    d = 1 / u  # 基础资产价格下跌比例
    p = (exp(r * t) - d) / (u - d)  # 基础资产价格上涨概率
    N_list = range(0, N + 1)  # 从0到N的自然数序列
    A = []  # 空列表

    for j in N_list:
        # 期权到期日某节点的期权价值
        C_Nj = maximum(S * power(u, j) * power(d, N - j) - K, 0)
        # 到达该节点的实现路径数量
        Num = factorial(N) / (factorial(j) * factorial(N - j))
        A.append(Num * power(p, j) * power(1 - p, N - j) * C_Nj)  # 列表尾部添加新元素

    call = exp(-r * T) * sum(A)  # 看涨期权期初价值
    put = call + K * np.exp(-r * T) - S  # 看跌期权期初价值

    if types == 'call':
        value = call
    else:
        value = put
    return value
