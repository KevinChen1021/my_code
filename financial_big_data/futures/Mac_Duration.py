"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def Mac_Duration(C, M, m, y, t):
    '''计算债券麦考利久期的函数
    C: 债券票面利率
    M: 债券面值
    m: 每年付息频次
    y: 连续复利到期收益率
    t: 定价日后各现金流支付日的期限（数组）'''
    if C == 0:
        duration = t  # 零息债券久期
    else:
        coupon = ones_like(t) * M * C / m  # 每期利息金额
        NPV_coupon = sum(coupon * exp(-y * t))  # 利息现值和
        NPV_par = M * exp(-y * t[-1])  # 本金现值
        Bond_value = NPV_coupon + NPV_par  # 债券价格

        cashflow = coupon
        cashflow[-1] = M * (1 + C / m)  # 最后一期现金流（本息和）
        weight = cashflow * exp(-y * t) / Bond_value  # 时间权重
        duration = sum(t * weight)  # 麦考利久期
    return duration
