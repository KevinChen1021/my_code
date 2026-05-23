"""Function module for bond_convexity."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def bond_convexity(coupon_rate, par_value, coupon_frequency, yield_rate, cashflow_times):
    """Compute bond_convexity."""
    if coupon_rate == 0:
        convexity = np.power(cashflow_times, 2)
    else:
        coupon = np.ones_like(cashflow_times) * par_value * coupon_rate / coupon_frequency
        NPV_coupon = np.sum(coupon * np.exp(-yield_rate * cashflow_times))
        NPV_par = par_value * np.exp(-yield_rate * cashflow_times[-1])
        price = NPV_coupon + NPV_par
        cashflow = coupon
        cashflow[-1] = par_value * (1 + coupon_rate / coupon_frequency)
        weight = cashflow * np.exp(-yield_rate * cashflow_times) / price
        convexity = np.sum(np.power(cashflow_times, 2) * weight)
    return convexity
