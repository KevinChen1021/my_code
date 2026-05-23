"""Function module for macaulay_duration."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def macaulay_duration(coupon_rate, par_value, coupon_frequency, yield_rate, cashflow_times):
    """Compute macaulay_duration."""
    if coupon_rate == 0:
        duration = cashflow_times
    else:
        coupon = np.ones_like(cashflow_times) * par_value * coupon_rate / coupon_frequency
        NPV_coupon = np.sum(coupon * np.exp(-yield_rate * cashflow_times))
        NPV_par = par_value * np.exp(-yield_rate * cashflow_times[-1])
        bond_value = NPV_coupon + NPV_par
        cashflow = coupon
        cashflow[-1] = par_value * (1 + coupon_rate / coupon_frequency)
        weight = cashflow * np.exp(-yield_rate * cashflow_times) / bond_value
        duration = np.sum(cashflow_times * weight)
    return duration
