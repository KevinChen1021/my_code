"""Function module for calmar_ratio."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm

from .max_drawdown import max_drawdown


def calmar_ratio(portfolio_return, max_drawdown):
    """Compute calmar_ratio."""
    calmar_ratio = portfolio_return / max_drawdown  # 卡玛比率的数学表达式
    return calmar_ratio
