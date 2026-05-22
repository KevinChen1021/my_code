"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def value_2SGM(D,g1,g2,T,r):
    '''定义一个运用二阶段增长模型计算股票内在价值的函数
    D: 代表企业已支付的最近一期每股股息金额。
    g1: 代表企业在第1个阶段的股息增长率。
    g2: 代表企业在第2个阶段的股息增长率，并且数值要小于贴现利率。
    T: 代表企业第1个阶段的期限，单位是年。
    r: 代表与企业的风险相匹配的贴现利率（每年复利1次）'''
    if r > g2:  # 贴现利率大于第2个阶段的股息增长率
        T_list = np.arange(1, T+1)  # 创建从1到T的整数数列
        # 计算第1个阶段股息贴现之和
        V1 = D * np.sum(np.power(1+g1, T_list) / np.power(1+r, T_list))
        # 计算第2个阶段股息贴现之和
        V2 = D * np.power(1+g1, T) * (1+g2) / (np.power(1+r, T) * (r - g2))
        value = V1 + V2  # 计算股票的内在价值
    else:  # 贴现利率小于或等于第2个阶段的股息增长率
        value = '输入的贴现利率小于或等于第2个阶段的股息增长率而导致结果不存在'
    return value
