"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def BTM_1step(S, K, u, d, r, T, types):
    '''运用一步二叉树模型计算欧式期权价值
    S: 基础资产当前价格
    K: 期权行权价格
    u: 基础资产价格上涨比例
    d: 基础资产价格下跌比例
    r: 连续复利无风险收益率
    T: 期权期限（年）
    types: 期权类型（'call'=看涨，其他=看跌）'''
    p = (exp(r * T) - d) / (u - d)  # 基础资产价格上涨概率
    # 期权到期时的价值
    Cu = maximum(S * u - K, 0)
    Cd = maximum(S * d - K, 0)
    # 初始日期的看涨期权价值
    call = (p * Cu + (1 - p) * Cd) * exp(-r * T)
    # 运用看跌-看涨平价关系计算看跌期权价值
    put = call + K * exp(-r * T) - S

    if types == 'call':
        value = call
    else:
        value = put
    return value
