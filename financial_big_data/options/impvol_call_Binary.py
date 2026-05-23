"""Function module for impvol_call_binary."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def impvol_call_binary(call_price, spot_price, strike_price, interest_rate, time_to_maturity):
    """Compute impvol_call_binary."""
    def call_bsm(spot_price, strike_price, volatility, interest_rate, time_to_maturity):
        d1 = (log(spot_price / strike_price) + (interest_rate + power(volatility, 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)
        call = spot_price * norm.cdf(d1) - strike_price * exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
        return call

    sigma_min = 0.001
    sigma_max = 1.000
    sigma_mid = (sigma_min + sigma_max) / 2
    call_min = call_bsm(spot_price, strike_price, sigma_min, interest_rate, time_to_maturity)
    call_max = call_bsm(spot_price, strike_price, sigma_max, interest_rate, time_to_maturity)
    call_mid = call_bsm(spot_price, strike_price, sigma_mid, interest_rate, time_to_maturity)
    diff = call_price - call_mid

    if call_price < call_min or call_price > call_max:
        print('Error')
    while abs(diff) > 1e-6:
        diff = call_price - call_bsm(spot_price, strike_price, sigma_mid, interest_rate, time_to_maturity)
        sigma_mid = (sigma_min + sigma_max) / 2
        call_mid = call_bsm(spot_price, strike_price, sigma_mid, interest_rate, time_to_maturity)
        if call_price > call_mid:
            sigma_min = sigma_mid
        else:
            sigma_max = sigma_mid
    return sigma_mid
