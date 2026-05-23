"""Function module for theta_eur_opt."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def theta_eur_opt(spot_price, strike_price, volatility, interest_rate, time_to_maturity, option_type):
    '''计算欧式期权Theta的函数'''
    d1 = (log(spot_price / strike_price) + (interest_rate + power(volatility, 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
    d2 = d1 - volatility * sqrt(time_to_maturity)
    # 计算看涨期权Theta
    theta_call = (spot_price * volatility * exp(-power(d1, 2) / 2)) / (2 * sqrt(2 * pi * time_to_maturity)) - interest_rate * strike_price * exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
    # 计算看跌期权Theta（看涨+看跌平价关系）
    theta_put = theta_call + interest_rate * strike_price * np.exp(-interest_rate * time_to_maturity)

    if option_type == 'call':
        theta = theta_call
    else:
        theta = theta_put
    return theta
