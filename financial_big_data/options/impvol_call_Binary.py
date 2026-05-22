"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def impvol_call_Binary(C, S, K, r, T):
    def call_BSM(S, K, sigma, r, T):
        d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        call = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        return call

    sigma_min = 0.001
    sigma_max = 1.000
    sigma_mid = (sigma_min + sigma_max) / 2
    call_min = call_BSM(S, K, sigma_min, r, T)
    call_max = call_BSM(S, K, sigma_max, r, T)
    call_mid = call_BSM(S, K, sigma_mid, r, T)
    diff = C - call_mid

    if C < call_min or C > call_max:
        print('Error')
    while abs(diff) > 1e-6:
        diff = C - call_BSM(S, K, sigma_mid, r, T)
        sigma_mid = (sigma_min + sigma_max) / 2
        call_mid = call_BSM(S, K, sigma_mid, r, T)
        if C > call_mid:
            sigma_min = sigma_mid
        else:
            sigma_max = sigma_mid
    return sigma_mid
