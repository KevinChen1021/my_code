"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def Value_FXforward(F0, F1, E, L_A, L_B, R_A, R_B, T_price, T_end, vc, position):
    '''定义一个计算远期外汇合约价值的函数，两种货币分别是A货币和B货币
    F0: 代表合约约定的远期汇率，以若干单位A货币表示1单位B货币
    F1: 代表合约定价日的远期汇率，标价方式与F0相同
    E: 代表合约定价日的即期汇率，标价方式与F0相同
    L_A: 代表以A货币计价的合约本金，L_A='Na'代表合约本金不是以A货币计价的
    L_B: 代表以B货币计价的合约本金，L_B='Na'代表合约本金不是以B货币计价的
    R_A: 代表A货币的无风险利率（连续复利）
    R_B: 代表B货币的无风险利率（连续复利）
    T_price: 代表合约定价日的日期，用时间对象格式输入
    T_end: 代表合约到期日的日期，输入格式与T_price相同
    vc: 代表合约价值的计价币种，vc='A'代表选择A货币，其他则代表选择B货币
    position: 代表头寸方向，position='long'代表多头，其他代表空头'''
    t = (T_end - T_price).days / 365  # 计算合约的剩余期限（年）

    if position == 'long':
        # 针对合约多头
        if L_B == 'Na':
            # 合约本金以A货币计价
            if vc == 'A':
                value = E * (L_A / F1 - L_A / F0) * exp(-R_B * t)
            else:
                value = (L_A / F1 - L_A / F0) * exp(-R_B * t)
        else:
            # 合约本金以B货币计价
            if vc == 'A':
                value = (L_B * F1 - L_B * F0) * exp(-R_A * t)
            else:
                value = (L_B * F1 - L_B * F0) * exp(-R_A * t) / E
    else:
        # 针对合约空头
        if L_B == 'Na':
            # 合约本金以A货币计价
            if vc == 'A':
                value = E * (L_A / F0 - L_A / F1) * exp(-R_B * t)
            else:
                value = (L_A / F0 - L_A / F1) * exp(-R_B * t)
        else:
            # 合约本金以B货币计价
            if vc == 'A':
                value = (L_B * F0 - L_B * F1) * exp(-R_A * t)
            else:
                value = (L_B * F0 - L_B * F1) * exp(-R_A * t) / E
    return value
