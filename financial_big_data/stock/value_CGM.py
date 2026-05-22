"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def value_CGM(D,g,r):
    '''定义一个运用不变增长模型计算股票内在价值的函数
    D: 代表企业已支付的最近一期每股股息金额。
    g: 代表企业的股息增长率，并且数值要小于贴现利率。
    r: 代表与企业的风险相匹配的贴现利率（每年复利1次）'''
    if r>g:  # 当贴现利率大于股息增长率
        value = D * (1+g) / (r - g)  # 计算股票内在价值
    else:  # 当贴现利率小于或等于股息增长率
        value = '输入的贴现利率小于或等于股息增长率而导致结果不存在'
    return value
