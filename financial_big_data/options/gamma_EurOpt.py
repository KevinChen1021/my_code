"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def gamma_EurOpt(S, K, sigma, r, T):
    '''计算欧式期权Gamma的函数'''
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    gamma = exp(-power(d1, 2) / 2) / (S * sigma * sqrt(2 * pi * T))
    return gamma
