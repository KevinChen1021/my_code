"""Function module for impvol_put_newton."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def impvol_put_newton(put_price, spot_price, strike_price, interest_rate, time_to_maturity):
    """Compute impvol_put_newton."""
    def put_bsm(spot_price, strike_price, volatility, interest_rate, time_to_maturity):
        d1 = (log(spot_price / strike_price) + (interest_rate + power(volatility, 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)
        put = strike_price * exp(-interest_rate * time_to_maturity) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)
        return put

    sigma0 = 0.2
    diff = put_price - put_bsm(spot_price, strike_price, sigma0, interest_rate, time_to_maturity)
    i = 0.0001
    while abs(diff) > 0.0001:
        diff = put_price - put_bsm(spot_price, strike_price, sigma0, interest_rate, time_to_maturity)
        if diff > 0:
            sigma0 += i
        else:
            sigma0 -= i
    return sigma0
