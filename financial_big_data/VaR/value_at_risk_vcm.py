"""Function module for value_at_risk_vcm."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.stats as st


def value_at_risk_vcm(Value, portfolio_return, portfolio_variance, confidence_level, steps):
    """
    方差-协方差法计算风险价值
    Value: 投资组合市值
    Rp: 组合日平均收益率
    Vp: 组合日波动率
    X: 置信水平
    N: 持有期（天）
    """
    z = abs(st.norm.ppf(q=1 - confidence_level))  # 正态分布分位数（取绝对值）
    VaR_1day = Value * (z * portfolio_variance - portfolio_return)  # 1天VaR
    VaR_Nday = np.sqrt(steps) * VaR_1day  # N天VaR（时间平方根法则）
    return VaR_Nday
