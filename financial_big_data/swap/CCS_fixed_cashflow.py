"""Function module for ccs_fixed_cashflow."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def ccs_fixed_cashflow(La, Lb, Ra_fix, Rb_fix, coupon_frequency, time_to_maturity, trader, par_value):
    """Compute ccs_fixed_cashflow."""
    cashflow = np.zeros(coupon_frequency*time_to_maturity + 1)  # 创建存放每期现金流的初始数组
    if par_value == 'La':
        # 依据本金La计算现金流
        cashflow[0] = La  # 计算A交易方第1期的现金流
        cashflow[1:-1] = Ra_fix * La / coupon_frequency  # 计算A交易方第2期至倒数第2期的现金流
        cashflow[-1] = (Ra_fix / coupon_frequency + 1) * La  # 计算A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow  # 针对B交易方
    else:
        # 依据本金Lb计算现金流
        cashflow[0] = Lb  # 计算A交易方第1期的现金流
        cashflow[1:-1] = Rb_fix * Lb / coupon_frequency  # 计算A交易方第2期至倒数第2期的现金流
        cashflow[-1] = (Rb_fix / coupon_frequency + 1) * Lb  # 计算A交易方最后一期的现金流
        if trader == 'A':
            return -cashflow  # 针对A交易方
        else:
            return cashflow
