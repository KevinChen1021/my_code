"""Function module for information_ratio."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def information_ratio(portfolio_return, benchmark_return, tracking_error):
    """Compute information_ratio."""
    information_ratio = (portfolio_return - benchmark_return) / tracking_error  # 信息比率的数学表达式
    return information_ratio
