"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def SOR(Rp, Rf, Vd):
    '''定义一个计算索提诺比率的函数
    Rp: 表示投资组合的年化收益率。
    Rf: 表示无风险利率。
    Vd: 表示投资组合的年化下行标准差'''
    sortino_ratio = (Rp - Rf) / Vd  # 索提诺比率的数学表达式
    return sortino_ratio
