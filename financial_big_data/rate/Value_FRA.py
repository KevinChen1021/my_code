"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def Value_FRA(L, Rk, Rf, R, T0, T1, T2, position):
    '''定义一个计算远期利率协议价值的函数
    L: 表示远期利率协议的本金
    Rk: 表示远期利率协议中的固定利率
    Rf: 表示当前观察到的未来[T1,T2]期间的远期参考利率
    R: 表示期限长度为T2-T0的无风险利率（连续复利）
    T0: 表示合约的估值日，用时间对象格式输入
    T1: 表示参考利率确定日（T1），格式与T0一致
    T2: 表示合约到期日（T2），格式与T0一致，并且T2大于T1
    position: 表示头寸方向，position='long'表示多头，其他表示空头'''
    from numpy import exp
    tenor1 = (T2 - T1).days / 365  # 远期参考利率的期限（年）
    tenor2 = (T2 - T0).days / 365  # 无风险利率贴现的期限（年）
    value_long = L * (Rf - Rk) * tenor1 * exp(-R * tenor2)  # 远期利率协议多头的估值
    if position == 'long':
        value = value_long  # 针对多头
    else:
        value = -value_long  # 针对空头
    return value
