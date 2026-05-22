"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def swaption(L, Sf, Sk, m, sigma, t, n, R_list, direction):
    """
    计算利率互换期权价值
    L: 本金
    Sf: 远期互换利率
    Sk: 固定利率
    m: 每年支付次数
    sigma: 远期互换利率年化波动率
    t: 期权期限（年）
    n: 互换合约期限（年）
    R_list: 无风险收益率（连续复利）数组
    direction: 'pay'=支付固定利息，其他=收取固定利息
    """
    d1 = (np.log(Sf/Sk) + np.power(sigma, 2)*t/2) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    # 构建支付日期限数组
    T_list = m*t + np.arange(1, m*n+1) / m
    if direction == 'pay':
        value = np.sum(np.exp(-R_list * T_list) * L * (Sf*norm.cdf(d1) - Sk*norm.cdf(d2)) / m)
    else:
        value = np.sum(np.exp(-R_list * T_list) * L * (Sk*norm.cdf(-d2) - Sf*norm.cdf(-d1)) / m)
    return value
