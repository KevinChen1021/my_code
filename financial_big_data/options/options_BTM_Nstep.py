"""Function module for binomial_tree_model_n_step."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def binomial_tree_model_n_step(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps, option_type):
    """Compute binomial_tree_model_n_step."""
    t = time_to_maturity / steps
    u = np.exp(volatility * np.sqrt(t))
    d = 1 / u
    p = (np.exp(interest_rate * t) - d) / (u - d)
    N_list = range(0, steps + 1)
    A = []
    for j in N_list:
        C_Nj = np.maximum(spot_price * np.power(u, j) * np.power(d, steps - j) - strike_price, 0) if option_type == 'call' else np.maximum(
            strike_price - spot_price * np.power(u, j) * np.power(d, steps - j), 0)
        Num = factorial(steps) / (factorial(j) * factorial(steps - j))
        A.append(Num * np.power(p, j) * np.power(1 - p, steps - j) * C_Nj)
    option_val = np.exp(-interest_rate * time_to_maturity) * sum(A)
    return option_val
