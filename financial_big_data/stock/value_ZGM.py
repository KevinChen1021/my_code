"""Function module for value_zgm."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def value_zgm(debt_value,interest_rate):
    """Compute value_zgm."""
    value = debt_value / interest_rate  # 计算股票的内在价值
    return value
