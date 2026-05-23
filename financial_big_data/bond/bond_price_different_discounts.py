"""Function module for bond_price_different_discounts."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def bond_price_different_discounts(coupon_rate, par_value, coupon_frequency, discount_rates, cashflow_times):
    """Compute bond_price_different_discounts."""
    if coupon_rate == 0:
        price = np.exp(-discount_rates * cashflow_times) * par_value
    else:
        coupon = np.ones_like(discount_rates) * par_value * coupon_rate / coupon_frequency
        NPV_coupon = np.sum(coupon * np.exp(-discount_rates * cashflow_times))
        NPV_par = par_value * np.exp(-discount_rates[-1] * cashflow_times[-1])
        price = NPV_coupon + NPV_par
    return price
