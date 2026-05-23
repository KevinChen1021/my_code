"""Function module for binomial_tree_model_n_step."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def binomial_tree_model_n_step(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps, option_type):
    '''运用N步二叉树模型计算欧式期权价值
    S: 基础资产当前价格
    K: 期权行权价格
    sigma: 基础资产年化波动率
    r: 连续复利无风险收益率
    T: 期权期限（年）
    N: 二叉树步数
    types: 期权类型（'call'=看涨，其他=看跌）'''
    from numpy import exp, maximum, sqrt
    t = time_to_maturity / steps  # 每一步的步长期限（年）
    u = exp(volatility * sqrt(t))  # 价格上涨比例
    d = 1 / u  # 价格下跌比例
    p = (exp(interest_rate * t) - d) / (u - d)  # 风险中性概率
    N_list = range(0, steps + 1)
    A = []

    for j in N_list:
        # 计算到期日某节点的期权价值
        C_Nj = maximum(spot_price * pow(u, j) * pow(d, steps - j) - strike_price, 0)
        # 计算到达该节点的路径数量
        Num = factorial(steps) / (factorial(j) * factorial(steps - j))
        A.append(Num * pow(p, j) * pow(1 - p, steps - j) * C_Nj)

    # 计算看涨期权价值
    call = exp(-interest_rate * time_to_maturity) * sum(A)
    # 运用看跌-看涨平价关系计算看跌期权价值
    put = call + strike_price * exp(-interest_rate * time_to_maturity) - spot_price

    if option_type == 'call':
        value = call
    else:
        value = put
    return value
