"""Function module for value_fx_forward."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def value_fx_forward(F0, F1, exchange_rate, notional_a, notional_b, rate_a, rate_b, price_time, end_time, vc, position):
    """Compute value_fx_forward."""
    t = (end_time - price_time).days / 365  # 计算合约的剩余期限（年）

    if position == 'long':
        # 针对合约多头
        if notional_b == 'Na':
            # 合约本金以A货币计价
            if vc == 'A':
                value = exchange_rate * (notional_a / F1 - notional_a / F0) * exp(-rate_b * t)
            else:
                value = (notional_a / F1 - notional_a / F0) * exp(-rate_b * t)
        else:
            # 合约本金以B货币计价
            if vc == 'A':
                value = (notional_b * F1 - notional_b * F0) * exp(-rate_a * t)
            else:
                value = (notional_b * F1 - notional_b * F0) * exp(-rate_a * t) / exchange_rate
    else:
        # 针对合约空头
        if notional_b == 'Na':
            # 合约本金以A货币计价
            if vc == 'A':
                value = exchange_rate * (notional_a / F0 - notional_a / F1) * exp(-rate_b * t)
            else:
                value = (notional_a / F0 - notional_a / F1) * exp(-rate_b * t)
        else:
            # 合约本金以B货币计价
            if vc == 'A':
                value = (notional_b * F0 - notional_b * F1) * exp(-rate_a * t)
            else:
                value = (notional_b * F0 - notional_b * F1) * exp(-rate_a * t) / exchange_rate
    return value
