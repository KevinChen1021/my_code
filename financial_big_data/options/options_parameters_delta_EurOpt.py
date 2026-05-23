"""Function module for delta_eur_opt."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def delta_eur_opt(spot_price, strike_price, volatility, interest_rate, time_to_maturity, option_type, position_type):
    """Compute delta_eur_opt."""
    d1 = (log(spot_price / strike_price) + (interest_rate + power(volatility, 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
    if option_type == 'call':
        if position_type == 'long':
            delta = norm.cdf(d1)
        else:
            delta = -norm.cdf(d1)
    else:
        if position_type == 'long':
            delta = norm.cdf(d1) - 1
        else:
            delta = 1 - norm.cdf(d1)
    return delta
