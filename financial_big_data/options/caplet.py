"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def caplet(L, R, F, Rk, sigma, t1, t2):
    """
    计算利率上限单元价值
    L: 本金
    R: 无风险收益率（连续复利）
    F: 远期利率
    Rk: 上限利率
    sigma: 远期利率年化波动率
    t1: 重置日时间（年）
    t2: 支付日时间（年）
    """
    d1 = (np.log(F/Rk) + 0.5 * np.power(sigma, 2) * t1) / (sigma * np.sqrt(t1))
    d2 = d1 - sigma * np.sqrt(t1)
    tau = t2 - t1  # 期限长度
    value = L * tau * np.exp(-R * t2) * (F * norm.cdf(d1) - Rk * norm.cdf(d2))
    return value
