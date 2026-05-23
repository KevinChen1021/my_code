"""Function module for value_2_sgm."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def value_2_sgm(debt_value,g1,g2,time_to_maturity,interest_rate):
    """Compute value_2_sgm."""
    if interest_rate > g2:  # 贴现利率大于第2个阶段的股息增长率
        T_list = np.arange(1, time_to_maturity+1)  # 创建从1到T的整数数列
        # 计算第1个阶段股息贴现之和
        V1 = debt_value * np.sum(np.power(1+g1, T_list) / np.power(1+interest_rate, T_list))
        # 计算第2个阶段股息贴现之和
        V2 = debt_value * np.power(1+g1, time_to_maturity) * (1+g2) / (np.power(1+interest_rate, time_to_maturity) * (interest_rate - g2))
        value = V1 + V2  # 计算股票的内在价值
    else:  # 贴现利率小于或等于第2个阶段的股息增长率
        value = '输入的贴现利率小于或等于第2个阶段的股息增长率而导致结果不存在'
    return value
