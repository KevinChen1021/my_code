"""Function module for g."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def g(x):
    """Compute g."""
    V, sigma_V = x
    d1 = (np.log(V/debt_new) + (rate_new + np.power(sigma_V, 2)/2)*tenor) / (sigma_V * np.sqrt(tenor))
    d2 = d1 - sigma_V * np.sqrt(tenor)
    eq1 = V*norm.cdf(d1) - debt_new*np.exp(-rate_new*tenor)*norm.cdf(d2) - equity_new
    eq2 = sigma_new * equity_new - norm.cdf(d1) * sigma_V * V
    return [eq1, eq2]
