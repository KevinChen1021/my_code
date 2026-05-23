"""Function module for delta_eur_opt."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def delta_eur_opt(spot_price, strike_price, volatility, interest_rate, time_to_maturity, option_type, position_type):
    '''计算欧式期权Delta的函数
    S: 基础资产价格
    K: 行权价格
    sigma: 年化波动率
    r: 连续复利无风险收益率
    T: 期权期限（年）
    optype: 期权类型（'call'=看涨，其他=看跌）
    positype: 头寸方向（'long'=多头，其他=空头）'''
    d1 = (log(spot_price/strike_price) + (interest_rate + power(volatility, 2)/2)*time_to_maturity) / (volatility * sqrt(time_to_maturity))
    if option_type == 'call':
        if position_type == 'long':
            delta = norm.cdf(d1)
        else:
            delta = -norm.cdf(d1)
    else:
        if position_type == 'long':
            delta = norm.cdf(d1) - 1
        else:
            delta = 1 - norm.cdf(d1)
    return delta
