"""Function module for gamma_amer_call."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def gamma_amer_call(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps):
    """Compute gamma_amer_call."""
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

    Delta1 = (call_matrix[0, 2] - call_matrix[1, 2]) / (spot_price * np.power(u, 2) - spot_price)
    Delta2 = (call_matrix[1, 2] - call_matrix[2, 2]) / (spot_price - spot_price * np.power(d, 2))
    Gamma = (Delta1 - Delta2) / (spot_price * np.power(u, 2) - spot_price * np.power(d, 2))
    return Gamma
