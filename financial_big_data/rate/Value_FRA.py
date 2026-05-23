"""Function module for value_fra."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def value_fra(notional_amount, strike_rate, Rf, rate, start_time, end_time, T2, position):
    """Compute value_fra."""
    from numpy import exp
    tenor1 = (T2 - end_time).days / 365  # 远期参考利率的期限（年）
    tenor2 = (T2 - start_time).days / 365  # 无风险利率贴现的期限（年）
    value_long = notional_amount * (Rf - strike_rate) * tenor1 * exp(-rate * tenor2)  # 远期利率协议多头的估值
    if position == 'long':
        value = value_long  # 针对多头
    else:
        value = -value_long  # 针对空头
    return value
