"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def theta_EurOpt(S, K, sigma, r, T, optype):
    '''计算欧式期权Theta的函数'''
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    # 计算看涨期权Theta
    theta_call = (S * sigma * exp(-power(d1, 2) / 2)) / (2 * sqrt(2 * pi * T)) - r * K * exp(-r * T) * norm.cdf(d2)
    # 计算看跌期权Theta（看涨+看跌平价关系）
    theta_put = theta_call + r * K * np.exp(-r * T)

    if optype == 'call':
        theta = theta_call
    else:
        theta = theta_put
    return theta
