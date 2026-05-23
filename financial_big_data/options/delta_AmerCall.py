"""Function module for delta_amer_call."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def delta_amer_call(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps, position_type):
    """Compute delta_amer_call."""
    t = time_to_maturity / steps
    u = np.exp(volatility * np.sqrt(t))
    d = 1 / u
    p = (np.exp(interest_rate * t) - d) / (u - d)
    call_matrix = np.zeros((steps + 1, steps + 1))
    N_list = np.arange(0, steps + 1)
    S_end = spot_price * np.power(u, steps - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(S_end - strike_price, 0)

    i_list = list(range(0, steps))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = spot_price * np.power(u, i - j) * np.power(d, j)
            call_strike = np.maximum(Si - strike_price, 0)
            call_nostrike = np.exp(-interest_rate * t) * (p * call_matrix[i + 1, j + 1] + (1 - p) * call_matrix[i + 1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)

    Delta = (call_matrix[0, 1] - call_matrix[1, 1]) / (spot_price * u - spot_price * d)
    if position_type == 'long':
        result = Delta
    else:
        result = -Delta
    return result
