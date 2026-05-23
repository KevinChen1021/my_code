"""Function module for swaption_price."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def swaption_price(notional_amount, forward_swap_rate, strike_swap_rate, coupon_frequency, volatility, time_points, n, rate_list, direction):
    """
    计算利率互换期权价值
    L: 本金
    Sf: 远期互换利率
    Sk: 固定利率
    m: 每年支付次数
    sigma: 远期互换利率年化波动率
    t: 期权期限（年）
    n: 互换合约期限（年）
    R_list: 无风险收益率（连续复利）数组
    direction: 'pay'=支付固定利息，其他=收取固定利息
    """
    d1 = (np.log(forward_swap_rate/strike_swap_rate) + np.power(volatility, 2)*time_points/2) / (volatility * np.sqrt(time_points))
    d2 = d1 - volatility * np.sqrt(time_points)
    # 构建支付日期限数组
    T_list = coupon_frequency*time_points + np.arange(1, coupon_frequency*n+1) / coupon_frequency
    if direction == 'pay':
        value = np.sum(np.exp(-rate_list * T_list) * notional_amount * (forward_swap_rate*norm.cdf(d1) - strike_swap_rate*norm.cdf(d2)) / coupon_frequency)
    else:
        value = np.sum(np.exp(-rate_list * T_list) * notional_amount * (strike_swap_rate*norm.cdf(-d2) - forward_swap_rate*norm.cdf(-d1)) / coupon_frequency)
    return value
