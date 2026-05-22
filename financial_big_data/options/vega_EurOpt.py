"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def vega_EurOpt(S, K, sigma, r, T):
    '''计算欧式期权Vega的函数'''
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    vega = S * sqrt(T) * exp(-power(d1, 2) / 2) / sqrt(2 * pi)
    return vega
