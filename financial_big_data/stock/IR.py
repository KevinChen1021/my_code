"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def IR(Rp, Rb, TE):
    '''定义一个计算信息比率的函数
    Rp: 表示投资组合的年化收益率。
    Rb: 表示基准组合的年化收益率。
    TE: 表示跟踪误差'''
    information_ratio = (Rp - Rb) / TE  # 信息比率的数学表达式
    return information_ratio
