"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def Black_model(F, K, sigma, r, T, typ):
    """
    布莱克模型计算欧式期货期权价格
    F: 期货合约当前价格
    K: 期权行权价格
    sigma: 期货收益率年化波动率
    r: 无风险收益率
    T: 期权期限（年）
    typ: 期权类型，'call'为看涨，其他为看跌
    """
    d1 = (np.log(F/K) + np.power(sigma, 2)*T/2) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if typ == 'call':
        price = np.exp(-r*T) * (F*norm.cdf(d1) - K*norm.cdf(d2))
    else:
        price = np.exp(-r*T) * (K*norm.cdf(-d2) - F*norm.cdf(-d1))
    return price
