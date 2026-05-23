"""Function module for value_cgm."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def value_cgm(debt_value,g,interest_rate):
    """Compute value_cgm."""
    if interest_rate>g:  # 当贴现利率大于股息增长率
        value = debt_value * (1+g) / (interest_rate - g)  # 计算股票内在价值
    else:  # 当贴现利率小于或等于股息增长率
        value = '输入的贴现利率小于或等于股息增长率而导致结果不存在'
    return value
