"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def rho_EurOpt(S, K, sigma, r, T, optype):
    '''计算欧式期权Rho的函数'''
    d2 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    if optype == 'call':
        rho = K * T * exp(-r * T) * norm.cdf(d2)
    else:
        rho = -K * T * exp(-r * T) * norm.cdf(-d2)
    return rho
