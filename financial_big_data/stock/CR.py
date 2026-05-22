"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm

from .MDD import MDD


def CR(Rp, MDD):
    '''定义一个计算卡玛比率的函数
    Rp: 表示投资组合的年化收益率。
    MDD: 表示投资组合的最大回撤率'''
    calmar_ratio = Rp / MDD  # 卡玛比率的数学表达式
    return calmar_ratio
