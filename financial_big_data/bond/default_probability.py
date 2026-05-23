"""Function module for default_probability."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def default_probability(risk_free_rate, risky_yield, recovery_rate, maturity_years):
    """Compute default_probability."""
    A = (np.exp(-risky_yield * maturity_years) - recovery_rate * np.exp(-risk_free_rate * maturity_years)) / (1 - recovery_rate)
    default_prob = -np.log(A) / maturity_years - risk_free_rate
    return default_prob
