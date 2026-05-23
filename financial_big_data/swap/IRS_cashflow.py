"""Function module for irs_cashflow."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def irs_cashflow(floating_rate, fixed_rate, notional_amount, coupon_frequency, position):
    """Compute irs_cashflow."""
    if position == 'long':
        # 计算利率互换多头时期的净现金流
        cashflow = (floating_rate - fixed_rate) * notional_amount / coupon_frequency
    else:
        # 计算利率互换空头时期的净现金流
        cashflow = (fixed_rate - floating_rate) * notional_amount / coupon_frequency
    return cashflow
