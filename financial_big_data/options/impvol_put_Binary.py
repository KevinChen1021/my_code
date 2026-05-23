"""Function module for impvol_put_binary."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def impvol_put_binary(put_price, spot_price, strike_price, interest_rate, time_to_maturity):
    """Compute impvol_put_binary."""
    def put_bsm(spot_price, strike_price, volatility, interest_rate, time_to_maturity):
        d1 = (log(spot_price / strike_price) + (interest_rate + power(volatility, 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)
        put = strike_price * exp(-interest_rate * time_to_maturity) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)
        return put

    sigma_min = 0.001
    sigma_max = 1.000
    sigma_mid = (sigma_min + sigma_max) / 2
    put_min = put_bsm(spot_price, strike_price, sigma_min, interest_rate, time_to_maturity)
    put_max = put_bsm(spot_price, strike_price, sigma_max, interest_rate, time_to_maturity)
    put_mid = put_bsm(spot_price, strike_price, sigma_mid, interest_rate, time_to_maturity)
    diff = put_price - put_mid

    if put_price < put_min or put_price > put_max:
        print('Error')
    while abs(diff) > 1e-6:
        diff = put_price - put_bsm(spot_price, strike_price, sigma_mid, interest_rate, time_to_maturity)
        sigma_mid = (sigma_min + sigma_max) / 2
        put_mid = put_bsm(spot_price, strike_price, sigma_mid, interest_rate, time_to_maturity)
        if put_price > put_mid:
            sigma_min = sigma_mid
        else:
            sigma_max = sigma_mid
    return sigma_mid
