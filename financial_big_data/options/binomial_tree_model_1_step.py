"""Function module for binomial_tree_model_1_step."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def binomial_tree_model_1_step(spot_price, strike_price, up_factor, down_factor, interest_rate, time_to_maturity, option_type):
    '''运用一步二叉树模型计算欧式期权价值
    S: 基础资产当前价格
    K: 期权行权价格
    u: 基础资产价格上涨比例
    d: 基础资产价格下跌比例
    r: 连续复利无风险收益率
    T: 期权期限（年）
    types: 期权类型（'call'=看涨，其他=看跌）'''
    p = (exp(interest_rate * time_to_maturity) - down_factor) / (up_factor - down_factor)  # 基础资产价格上涨概率
    # 期权到期时的价值
    Cu = maximum(spot_price * up_factor - strike_price, 0)
    Cd = maximum(spot_price * down_factor - strike_price, 0)
    # 初始日期的看涨期权价值
    call = (p * Cu + (1 - p) * Cd) * exp(-interest_rate * time_to_maturity)
    # 运用看跌-看涨平价关系计算看跌期权价值
    put = call + strike_price * exp(-interest_rate * time_to_maturity) - spot_price

    if option_type == 'call':
        value = call
    else:
        value = put
    return value
