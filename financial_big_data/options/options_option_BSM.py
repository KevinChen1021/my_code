"""Function module for black_scholes_option_price."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def black_scholes_option_price(spot_price, strike_price, volatility, interest_rate, time_to_maturity, option_type):
    """Compute black_scholes_option_price."""
    from numpy import log, exp, sqrt
    d1 = (log(spot_price / strike_price) + (interest_rate + pow(volatility, 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
    d2 = d1 - volatility * sqrt(time_to_maturity)
    if option_type == 'call':
        value = spot_price * norm.cdf(d1) - strike_price * exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
    else:
        value = strike_price * exp(-interest_rate * time_to_maturity) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)
    return value
