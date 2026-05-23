"""Function module for max_drawdown."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def max_drawdown(data):
    """Compute max_drawdown."""
    n = len(data)  # 计算期间的交易天数
    DD = np.zeros((n-1, n-1))  # 创建n-1行、n-1列数组，用于存放回撤率数据
    for i in range(n-1):
        Pi = data.iloc[i+1]  # 第i个交易日的基金净值
        for j in range(i+1, n):
            Pj = data.iloc[j]  # 被套的第j个交易日的基金净值
            DD[i, j-1] = (Pi - Pj) / Pi  # 依次计算并存放期间的每个回撤率数据
    Max_DD = np.max(DD)  # 计算基金净值的最大回撤率
    return Max_DD
