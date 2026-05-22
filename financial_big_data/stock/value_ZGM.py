"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def value_ZGM(D,r):
    '''定义一个运用零增长模型计算股票内在价值的函数
    D: 代表企业已支付的最近一期每股股息金额。
    r: 代表与企业的风险相匹配的贴现利率（每年复利1次）'''
    value = D / r  # 计算股票的内在价值
    return value
