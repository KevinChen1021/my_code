"""Function module for treynor_ratio."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def treynor_ratio(portfolio_return, Rf, beta):
    """Compute treynor_ratio."""
    treynor_ratio = (portfolio_return - Rf) / beta  # 特雷诺比率的数学表达式
    return treynor_ratio
