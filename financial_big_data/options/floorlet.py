"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def floorlet(L, R, F, Rk, sigma, t1, t2):
    """
    计算利率下限单元价值
    参数同caplet
    """
    d1 = (np.log(F/Rk) + np.power(sigma, 2) * t1/2) / (sigma * np.sqrt(t1))
    d2 = d1 - sigma * np.sqrt(t1)
    tau = t2 - t1
    value = L * tau * np.exp(-R * t2) * (Rk * norm.cdf(-d2) - F * norm.cdf(-d1))
    return value
