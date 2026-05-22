"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def FRA_cashflow(L, Rk, Rm, T1, T2, position):
    '''构建计算远期利率协议在参考利率确定日发生现金流的函数
    L: 表示远期利率协议的本金
    Rk: 表示远期利率协议的固定利率
    Rm: 表示在参考利率确定日（T1时点）观察到的[T1,T2]的参考利率
    T1: 表示参考利率确定日，以时间对象格式输入
    T2: 表示远期利率协议到期日，以时间对象格式输入，并且T2大于T1
    position: 表示头寸方向，position='long'表示多头，其他则表示空头'''
    tenor = (T2 - T1).days / 365  # 测算期限（年）
    cashflow_long = (Rm - Rk) * tenor * L / (1 + tenor * Rm)  # 计算多头的现金流
    if position == 'long':
        cashflow = cashflow_long  # 针对多头
    else:
        cashflow = -cashflow_long  # 针对空头
    return cashflow
