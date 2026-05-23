"""Function module for delta_amer_put."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def delta_amer_put(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps, position_type):
    """Compute delta_amer_put."""
    t = time_to_maturity / steps
    u = np.exp(volatility * np.sqrt(t))
    d = 1 / u
    p = (np.exp(interest_rate * t) - d) / (u - d)
    put_matrix = np.zeros((steps + 1, steps + 1))
    N_list = np.arange(0, steps + 1)
    S_end = spot_price * np.power(u, steps - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(strike_price - S_end, 0)

    i_list = list(range(0, steps))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = spot_price * np.power(u, i - j) * np.power(d, j)
            put_strike = np.maximum(strike_price - Si, 0)
            put_nostrike = np.exp(-interest_rate * t) * (p * put_matrix[i + 1, j + 1] + (1 - p) * put_matrix[i + 1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)

    Delta = (put_matrix[0, 1] - put_matrix[1, 1]) / (spot_price * u - spot_price * d)
    if position_type == 'long':
        result = Delta
    else:
        result = -Delta
    return result
