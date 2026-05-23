"""Function module for forward_swaprate."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def forward_swaprate(spot_price_list, time_points, n, coupon_frequency):
    """
    计算远期互换利率
    S_list: 不同期限的互换利率数组
    t: 期权期限（年）
    n: 互换合约期限（年）
    m: 每年支付次数
    """
    t_list = coupon_frequency*time_points + np.arange(1, coupon_frequency*n+1) / coupon_frequency
    # 计算分子
    A = (pow(1+spot_price_list[0]/coupon_frequency, -coupon_frequency*time_points) - pow(1+spot_price_list[-1]/coupon_frequency, -coupon_frequency*(time_points+n)))
    # 计算分母
    B = (1/coupon_frequency) * np.sum(pow(1+spot_price_list[1:]/coupon_frequency, -t_list))
    value = A / B
    return value
