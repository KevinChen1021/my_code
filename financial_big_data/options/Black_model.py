"""Function module for black_model."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def black_model(forward_price, strike_price, volatility, interest_rate, time_to_maturity, typ):
    """
    布莱克模型计算欧式期货期权价格
    F: 期货合约当前价格
    K: 期权行权价格
    sigma: 期货收益率年化波动率
    r: 无风险收益率
    T: 期权期限（年）
    typ: 期权类型，'call'为看涨，其他为看跌
    """
    d1 = (np.log(forward_price/strike_price) + np.power(volatility, 2)*time_to_maturity/2) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    if typ == 'call':
        price = np.exp(-interest_rate*time_to_maturity) * (forward_price*norm.cdf(d1) - strike_price*norm.cdf(d2))
    else:
        price = np.exp(-interest_rate*time_to_maturity) * (strike_price*norm.cdf(-d2) - forward_price*norm.cdf(-d1))
    return price
