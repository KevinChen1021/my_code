"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def option_BSM(S, K, sigma, r, T, opt):
    '''运用布莱克-斯科尔斯-默顿模型计算欧式期权价格
    S: 期权基础资产价格
    K: 期权行权价格
    sigma: 基础资产收益率的波动率（年化）
    r: 连续复利的无风险收益率
    T: 期权期限（年）
    opt: 期权类型（'call'=看涨期权，其他=看跌期权）'''
    from numpy import log, exp, sqrt
    d1 = (log(S/K) + (r + pow(sigma, 2)/2) * T) / (sigma * sqrt(T))  # 计算参数d1
    d2 = d1 - sigma * sqrt(T)  # 计算参数d2
    if opt == 'call':
        value = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)  # 欧式看涨期权价格
    else:
        value = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)  # 欧式看跌期权价格
    return value
