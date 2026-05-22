"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def forward_swaprate(S_list, t, n, m):
    """
    计算远期互换利率
    S_list: 不同期限的互换利率数组
    t: 期权期限（年）
    n: 互换合约期限（年）
    m: 每年支付次数
    """
    t_list = m*t + np.arange(1, m*n+1) / m
    # 计算分子
    A = (pow(1+S_list[0]/m, -m*t) - pow(1+S_list[-1]/m, -m*(t+n)))
    # 计算分母
    B = (1/m) * np.sum(pow(1+S_list[1:]/m, -t_list))
    value = A / B
    return value
