"""Function module for ccs_value."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm

from .swap_value import swap_value


def ccs_value(option_type, La, Lb, Ra, benchmark_return, ya, yb, exchange_rate, coupon_frequency, time_points, trader):
    """Compute ccs_value."""
    if option_type == '双固定利率货币互换':
        # 计算对应A货币本金的固定利率债券价值
        Bond_A = (Ra * np.sum(exp(-ya * time_points)) / coupon_frequency + exp(-ya[-1] * time_points[-1])) * La
        # 计算对应B货币本金的固定利率债券价值
        Bond_B = (benchmark_return * np.sum(exp(-yb * time_points)) / coupon_frequency + exp(-yb[-1] * time_points[-1])) * Lb
        if trader == 'A':
            # 计算货币互换合约的价值（以A货币计价）
            swap_value = Bond_A - Bond_B * exchange_rate
        else:
            # 计算货币互换合约的价值（以B货币计价）
            swap_value = Bond_B - Bond_A / exchange_rate
    elif option_type == '双浮动利率货币互换':
        # 计算对应A货币本金的浮动利率债券价值
        Bond_A = (Ra / coupon_frequency + 1) * exp(-ya[0] * time_points[0]) * La
        # 计算对应B货币本金的浮动利率债券价值
        Bond_B = (benchmark_return / coupon_frequency + 1) * exp(-yb[0] * time_points[0]) * Lb
        if trader == 'A':
            swap_value = Bond_A - Bond_B * exchange_rate
        else:
            swap_value = Bond_B - Bond_A / exchange_rate
    else:
        # 固定对浮动货币互换：A货币固定，B货币浮动
        Bond_A = (Ra * np.sum(exp(-ya * time_points)) / coupon_frequency + exp(-ya[-1] * time_points[-1])) * La
        Bond_B = (benchmark_return / coupon_frequency + 1) * exp(-yb[0] * time_points[0]) * Lb
        if trader == 'A':
            swap_value = Bond_A - Bond_B * exchange_rate
        else:
            swap_value = Bond_B - Bond_A / exchange_rate
    return swap_value
