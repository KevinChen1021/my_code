"""Function module for f."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def f(x):
    """Compute f."""
    V, sigma_V = x
    # 公式(14-2)：股权价值方程
    d1 = (np.log(V/debt) + (rate + np.power(sigma_V, 2)/2)*tenor) / (sigma_V * np.sqrt(tenor))
    d2 = d1 - sigma_V * np.sqrt(tenor)
    eq1 = V*norm.cdf(d1) - debt*np.exp(-rate*tenor)*norm.cdf(d2) - equity
    # 公式(14-3)：波动率匹配方程
    eq2 = sigma_Sun * equity - norm.cdf(d1) * sigma_V * V
    return [eq1, eq2]
