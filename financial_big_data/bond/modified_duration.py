"""Function module for modified_duration."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def modified_duration(coupon_rate, par_value, coupon_frequency, compounding_frequency, yield_rate, cashflow_times):
    """Compute modified_duration."""
    if coupon_rate == 0:
        macaulay_duration = cashflow_times
    else:
        r = compounding_frequency * np.log(1 + yield_rate / compounding_frequency)
        coupon = np.ones_like(cashflow_times) * par_value * coupon_rate / coupon_frequency
        NPV_coupon = np.sum(coupon * np.exp(-r * cashflow_times))
        NPV_par = par_value * np.exp(-r * cashflow_times[-1])
        price = NPV_coupon + NPV_par
        cashflow = coupon
        cashflow[-1] = par_value * (1 + coupon_rate / coupon_frequency)
        weight = cashflow * np.exp(-r * cashflow_times) / price
        macaulay_duration = np.sum(cashflow_times * weight)
    modified_duration_value = macaulay_duration / (1 + yield_rate / compounding_frequency)
    return modified_duration_value
