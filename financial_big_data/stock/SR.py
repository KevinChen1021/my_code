"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def SR(Rp, Rf, Vp):
    '''定义一个计算夏普比率的函数
    Rp: 代表投资组合的年化收益率。
    Rf: 代表无风险利率。
    Vp: 代表投资组合的年化波动率'''
    sharp_ratio = (Rp - Rf) / Vp  # 计算夏普比率的公式
    return sharp_ratio
