"""Function module for binomial_tree_model_n_step."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def binomial_tree_model_n_step(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps, option_type):
    """Compute binomial_tree_model_n_step."""
    t = time_to_maturity / steps  # 每一步长时期限（年）
    u = exp(volatility * sqrt(t))  # 基础资产价格上涨比例
    d = 1 / u  # 基础资产价格下跌比例
    p = (exp(interest_rate * t) - d) / (u - d)  # 基础资产价格上涨概率
    N_list = range(0, steps + 1)  # 从0到N的自然数序列
    A = []  # 空列表

    for j in N_list:
        # 期权到期日某节点的期权价值
        C_Nj = maximum(spot_price * power(u, j) * power(d, steps - j) - strike_price, 0)
        # 到达该节点的实现路径数量
        Num = factorial(steps) / (factorial(j) * factorial(steps - j))
        A.append(Num * power(p, j) * power(1 - p, steps - j) * C_Nj)  # 列表尾部添加新元素

    call = exp(-interest_rate * time_to_maturity) * sum(A)  # 看涨期权期初价值
    put = call + strike_price * np.exp(-interest_rate * time_to_maturity) - spot_price  # 看跌期权期初价值

    if option_type == 'call':
        value = call
    else:
        value = put
    return value
