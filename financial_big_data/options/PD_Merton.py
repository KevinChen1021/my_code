"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def PD_Merton(E, D, V, sigma, r, T):
    """运用默顿模型计算企业违约概率"""
    d1 = (np.log(V/D) + (r + np.power(sigma, 2)/2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    PD = norm.cdf(-d2)
    return PD
