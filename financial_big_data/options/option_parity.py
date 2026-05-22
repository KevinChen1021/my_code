"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def option_parity(opt, c, p, S, K, r, T):
    '''通过看跌-看涨平价关系式计算欧式看涨、看跌期权价格
    opt: 期权类型（'call'=看涨，其他=看跌）
    c: 看涨期权价格（计算看涨时输入'Na'）
    p: 看跌期权价格（计算看跌时输入'Na'）
    S: 基础资产价格
    K: 行权价格
    r: 连续复利无风险收益率
    T: 期权期限（年）'''
    from numpy import exp
    if opt == 'call':
        value = p + S - K * exp(-r * T)  # 计算看涨期权价格
    else:
        value = c + K * exp(-r * T) - S  # 计算看跌期权价格
    return value
