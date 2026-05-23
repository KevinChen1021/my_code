"""Function module for binomial_tree_model_2_step."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def binomial_tree_model_2_step(spot_price, strike_price, up_factor, down_factor, interest_rate, time_to_maturity, option_type):
    """Compute binomial_tree_model_2_step."""
    t = time_to_maturity / 2  # 每一步的步长期限（年）
    p = (exp(interest_rate * t) - down_factor) / (up_factor - down_factor)  # 基础资产价格上涨概率
    # 期权到期时的价值（两步后的三种状态）
    Cuu = maximum(pow(up_factor, 2) * spot_price - strike_price, 0)
    Cud = maximum(spot_price * up_factor * down_factor - strike_price, 0)
    Cdd = maximum(pow(down_factor, 2) * spot_price - strike_price, 0)
    # 初始日期的看涨期权价值
    call = (pow(p, 2) * Cuu + 2 * p * (1 - p) * Cud + pow(1 - p, 2) * Cdd) * exp(-interest_rate * time_to_maturity)
    # 运用看跌-看涨平价关系计算看跌期权价值
    put = call + strike_price * exp(-interest_rate * time_to_maturity) - spot_price

    if option_type == 'call':
        value = call
    else:
        value = put
    return value
