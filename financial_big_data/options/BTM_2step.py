"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def BTM_2step(S, K, u, d, r, T, types):
    '''运用两步二叉树模型计算欧式期权价值
    参数定义同一步二叉树模型'''
    t = T / 2  # 每一步的步长期限（年）
    p = (exp(r * t) - d) / (u - d)  # 基础资产价格上涨概率
    # 期权到期时的价值（两步后的三种状态）
    Cuu = maximum(pow(u, 2) * S - K, 0)
    Cud = maximum(S * u * d - K, 0)
    Cdd = maximum(pow(d, 2) * S - K, 0)
    # 初始日期的看涨期权价值
    call = (pow(p, 2) * Cuu + 2 * p * (1 - p) * Cud + pow(1 - p, 2) * Cdd) * exp(-r * T)
    # 运用看跌-看涨平价关系计算看跌期权价值
    put = call + K * exp(-r * T) - S

    if types == 'call':
        value = call
    else:
        value = put
    return value
