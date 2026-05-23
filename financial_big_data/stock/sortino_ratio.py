"""Function module for sortino_ratio."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def sortino_ratio(portfolio_return, Rf, downside_deviation):
    """Compute sortino_ratio."""
    sortino_ratio = (portfolio_return - Rf) / downside_deviation  # 索提诺比率的数学表达式
    return sortino_ratio
