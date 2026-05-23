"""Function module for swap_value."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def swap_value(fixed_rate, floating_rate, time_points, yield_rate, coupon_frequency, notional_amount, position):
    """Compute swap_value."""
    # 计算固定利率债券价值
    B_fix = (fixed_rate * sum(exp(-yield_rate*time_points))/coupon_frequency + exp(-yield_rate[-1]*time_points[-1]))*notional_amount
    # 计算浮动利率债券价值
    B_flt = (floating_rate/coupon_frequency + 1) * exp(-yield_rate[0] * time_points[0]) * notional_amount
    if position == 'long':
        # 计算互换利率合约的多头价值
        value = B_flt - B_fix
    else:
        # 计算互换利率合约的空头价值
        value = B_fix - B_flt
    return value
