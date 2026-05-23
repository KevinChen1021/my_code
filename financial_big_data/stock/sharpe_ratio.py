"""Function module for sharpe_ratio."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def sharpe_ratio(portfolio_return, Rf, portfolio_variance):
    """Compute sharpe_ratio."""
    sharp_ratio = (portfolio_return - Rf) / portfolio_variance  # 计算夏普比率的公式
    return sharp_ratio
