"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def FX_forward(Ea, Eb, r_A, r_B, T0, T1, types):
    '''定义一个计算远期汇率的函数，并且两种货币分别是A货币和B货币
    Ea: 代表A货币兑换B货币的即期汇率卖出价，以若干单位A货币表示1单位B货币
    Eb: 代表A货币兑换B货币的即期汇率买入价，标价方式与Ea一致
    r_A: 代表A货币的无风险利率，并且每年复利1次
    r_B: 代表B货币的无风险利率，复利频次与r_A保持一致
    T0: 代表远期汇率的定价日，以datetime格式输入
    T1: 代表远期汇率的到期日（交割日），输入格式与T0一致
    types: 代表远期汇率价格类型，types='卖出价'代表远期汇率的卖出价，其他则代表买入价'''
    T = (T1 - T0).days / 365  # 计算定价日至到期日的期限（年）
    if types == '卖出价':
        # 针对远期汇率的卖出价
        forward = Ea * (1 + r_A * T) / (1 + r_B * T)
    else:
        # 针对远期汇率的买入价
        forward = Eb * (1 + r_A * T) / (1 + r_B * T)
    return forward
