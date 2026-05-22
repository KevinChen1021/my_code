"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def impvol_call_Newton(C, S, K, r, T):
    def call_BSM(S, K, sigma, r, T):
        d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        call = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        return call

    sigma0 = 0.2
    diff = C - call_BSM(S, K, sigma0, r, T)
    i = 0.0001
    while abs(diff) > 0.0001:
        diff = C - call_BSM(S, K, sigma0, r, T)
        if diff > 0:
            sigma0 += i
        else:
            sigma0 -= i
    return sigma0
