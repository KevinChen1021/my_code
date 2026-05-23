"""Function module for ccs_float_cashflow."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def ccs_float_cashflow(La, Lb, Ra_flt, Rb_flt, coupon_frequency, time_to_maturity, trader, par_value):
    """Compute ccs_float_cashflow."""
    cashflow = np.zeros(coupon_frequency*time_to_maturity + 1)  # 创建存放每期现金流的初始数组
    if par_value == 'La':
        # 依据本金La计算现金流
        cashflow[0] = La  # A交易方第1期的现金流
        cashflow[1:-1] = Ra_flt[:-1] * La / coupon_frequency  # A交易方第2期至倒数第2期的现金流
        cashflow[-1] = (Ra_flt[-1] / coupon_frequency + 1) * La  # A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow  # 针对B交易方
    else:
        # 依据本金Lb计算现金流
        cashflow[0] = Lb  # A交易方第1期的现金流
        cashflow[1:-1] = -Rb_flt[:-1] * Lb / coupon_frequency  # A交易方第2期至倒数第2期的现金流
        cashflow[-1] = -(Rb_flt[-1] / coupon_frequency + 1) * Lb  # A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow
