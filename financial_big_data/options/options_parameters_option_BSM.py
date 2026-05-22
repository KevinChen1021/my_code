"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def option_BSM(S, K, sigma, r, T, opt):
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    if opt == 'call':
        value = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        value = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return value
