"""Function module for caplet."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def caplet(notional_amount, rate, forward_price, strike_rate, volatility, start_time, end_time):
    """
    计算利率上限单元价值
    L: 本金
    R: 无风险收益率（连续复利）
    F: 远期利率
    Rk: 上限利率
    sigma: 远期利率年化波动率
    t1: 重置日时间（年）
    t2: 支付日时间（年）
    """
    d1 = (np.log(forward_price/strike_rate) + 0.5 * np.power(volatility, 2) * start_time) / (volatility * np.sqrt(start_time))
    d2 = d1 - volatility * np.sqrt(start_time)
    tau = end_time - start_time  # 期限长度
    value = notional_amount * tau * np.exp(-rate * end_time) * (forward_price * norm.cdf(d1) - strike_rate * norm.cdf(d2))
    return value
