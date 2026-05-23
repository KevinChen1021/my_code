"""Function module for bond_price_single_discount."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def bond_price_single_discount(coupon_rate, par_value, coupon_frequency, discount_rate, cashflow_times):
    """Compute bond_price_single_discount."""
    if coupon_rate == 0:
        price = np.exp(-discount_rate * cashflow_times) * par_value
    else:
        coupon = np.ones_like(cashflow_times) * (par_value * coupon_rate / coupon_frequency)
        NPV_coupon = np.sum(coupon * np.exp(-discount_rate * cashflow_times))
        NPV_par = par_value * np.exp(-discount_rate * cashflow_times[-1])
        price = NPV_coupon + NPV_par
    return price
