"""Function module for impvol_call_newton."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def impvol_call_newton(call_price, spot_price, strike_price, interest_rate, time_to_maturity):
    """Compute impvol_call_newton."""
    def call_bsm(spot_price, strike_price, volatility, interest_rate, time_to_maturity):
        d1 = (log(spot_price / strike_price) + (interest_rate + power(volatility, 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)
        call = spot_price * norm.cdf(d1) - strike_price * exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
        return call

    sigma0 = 0.2
    diff = call_price - call_bsm(spot_price, strike_price, sigma0, interest_rate, time_to_maturity)
    i = 0.0001
    while abs(diff) > 0.0001:
        diff = call_price - call_bsm(spot_price, strike_price, sigma0, interest_rate, time_to_maturity)
        if diff > 0:
            sigma0 += i
        else:
            sigma0 -= i
    return sigma0
