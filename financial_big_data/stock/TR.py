"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def TR(Rp, Rf, beta):
    '''定义一个计算特雷诺比率的函数
    Rp: 表示投资组合的年化收益率。
    Rf: 表示无风险利率。
    beta: 表示投资组合的贝塔值'''
    treynor_ratio = (Rp - Rf) / beta  # 特雷诺比率的数学表达式
    return treynor_ratio
