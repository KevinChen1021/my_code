"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def impvol_put_Binary(P, S, K, r, T):
    def put_BSM(S, K, sigma, r, T):
        d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        put = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put

    sigma_min = 0.001
    sigma_max = 1.000
    sigma_mid = (sigma_min + sigma_max) / 2
    put_min = put_BSM(S, K, sigma_min, r, T)
    put_max = put_BSM(S, K, sigma_max, r, T)
    put_mid = put_BSM(S, K, sigma_mid, r, T)
    diff = P - put_mid

    if P < put_min or P > put_max:
        print('Error')
    while abs(diff) > 1e-6:
        diff = P - put_BSM(S, K, sigma_mid, r, T)
        sigma_mid = (sigma_min + sigma_max) / 2
        put_mid = put_BSM(S, K, sigma_mid, r, T)
        if P > put_mid:
            sigma_min = sigma_mid
        else:
            sigma_max = sigma_mid
    return sigma_mid
