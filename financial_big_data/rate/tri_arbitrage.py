"""Function module for tri_arbitrage."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def tri_arbitrage(notional_amount, E1a, E1b, E2a, E2b, E3a, E3b, amount, coupon_rate):
    """Compute tri_arbitrage."""
    if E3b / (E1a * E2a) > 1:
        # 套利路径1存在套利机会
        profit = (E3b / (E1a * E2a) - 1) * notional_amount
        path = ['套利路径: ', amount, '→', amount, '→', coupon_rate, '→', amount]
    elif E1b * E2b / E3a > 1:
        # 套利路径2存在套利机会
        profit = (E1b * E2b / E3a - 1) * notional_amount
        path = ['套利路径: ', amount, '→', coupon_rate, '→', amount, '→', amount]
    else:
        # 不存在套利机会
        profit = 0
        path = ['不存在套利机会']
    return [profit, path]
