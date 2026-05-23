"""Function module for black_scholes_option_price."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def black_scholes_option_price(spot_price, strike_price, volatility, interest_rate, time_to_maturity, option_type):
    '''运用布莱克-斯科尔斯-默顿模型计算欧式期权价格
    S: 期权基础资产价格
    K: 期权行权价格
    sigma: 基础资产收益率的波动率（年化）
    r: 连续复利的无风险收益率
    T: 期权期限（年）
    opt: 期权类型（'call'=看涨期权，其他=看跌期权）'''
    from numpy import log, exp, sqrt
    d1 = (log(spot_price/strike_price) + (interest_rate + pow(volatility, 2)/2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))  # 计算参数d1
    d2 = d1 - volatility * sqrt(time_to_maturity)  # 计算参数d2
    if option_type == 'call':
        value = spot_price * norm.cdf(d1) - strike_price * exp(-interest_rate * time_to_maturity) * norm.cdf(d2)  # 欧式看涨期权价格
    else:
        value = strike_price * exp(-interest_rate * time_to_maturity) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)  # 欧式看跌期权价格
    return value
