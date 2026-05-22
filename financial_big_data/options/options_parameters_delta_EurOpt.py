"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def delta_EurOpt(S, K, sigma, r, T, optype, positype):
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    if optype == 'call':
        if positype == 'long':
            delta = norm.cdf(d1)
        else:
            delta = -norm.cdf(d1)
    else:
        if positype == 'long':
            delta = norm.cdf(d1) - 1
        else:
            delta = 1 - norm.cdf(d1)
    return delta
