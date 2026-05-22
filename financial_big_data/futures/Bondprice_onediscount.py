"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def Bondprice_onediscount(C, M, m, y, t):
    '''基于单一贴现率计算债券价格的函数
    C: 票面利率（0表示零息债券）
    M: 债券本金（面值）
    m: 每年付息频次
    y: 连续复利到期收益率
    t: 定价日后各付息日的期限（数组格式）'''
    if C == 0:
        price = exp(-y * t) * M  # 零息债券定价
    else:
        coupon = np.ones_like(t) * M * C / m  # 每期利息金额
        NPV_coupon = np.sum(coupon * exp(-y * t))  # 利息现值和
        NPV_par = M * exp(-y * t[-1])  # 本金现值
        price = NPV_coupon + NPV_par  # 全价
    return price
