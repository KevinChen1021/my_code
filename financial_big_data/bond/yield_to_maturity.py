"""Function module for yield_to_maturity."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def yield_to_maturity(price, coupon_rate, par_value, coupon_frequency, cashflow_times):
    """Compute yield_to_maturity."""
    import scipy.optimize as so  # 导入SciPy的子模块optimize

    def f(yield_rate):
        coupon = np.ones_like(cashflow_times) * par_value * coupon_rate / coupon_frequency
        NPV_coupon = np.sum(coupon * np.exp(-yield_rate * cashflow_times))
        NPV_par = par_value * np.exp(-yield_rate * cashflow_times[-1])
        value = NPV_coupon + NPV_par
        return value - price

    if coupon_rate == 0:
        y = (np.log(par_value / price)) / cashflow_times
    else:
        y = so.fsolve(f, x0=0.1)
    return y
