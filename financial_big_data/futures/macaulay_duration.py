"""Function module for macaulay_duration."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def macaulay_duration(coupon_rate, par_value, coupon_frequency, yield_rate, time_points):
    '''计算债券麦考利久期的函数
    C: 债券票面利率
    M: 债券面值
    m: 每年付息频次
    y: 连续复利到期收益率
    t: 定价日后各现金流支付日的期限（数组）'''
    if coupon_rate == 0:
        duration = time_points  # 零息债券久期
    else:
        coupon = ones_like(time_points) * par_value * coupon_rate / coupon_frequency  # 每期利息金额
        NPV_coupon = sum(coupon * exp(-yield_rate * time_points))  # 利息现值和
        NPV_par = par_value * exp(-yield_rate * time_points[-1])  # 本金现值
        Bond_value = NPV_coupon + NPV_par  # 债券价格

        cashflow = coupon
        cashflow[-1] = par_value * (1 + coupon_rate / coupon_frequency)  # 最后一期现金流（本息和）
        weight = cashflow * exp(-yield_rate * time_points) / Bond_value  # 时间权重
        duration = sum(time_points * weight)  # 麦考利久期
    return duration
