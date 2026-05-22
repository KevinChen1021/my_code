"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm

from .swap_value import swap_value


def CCS_value(types, La, Lb, Ra, Rb, ya, yb, E, m, t, trader):
    '''定义一个计算货币互换合约价值的函数
    types: 代表货币互换类型，输入types='双固定利率货币互换'表示计算双固定利率货币互换，
           输入types='双浮动利率货币互换'表示计算双浮动利率货币互换，输入其他则表示计算固定对浮动货币互换；
           并约定针对固定对浮动货币互换，固定利率针对A货币本金，浮动利率针对B货币本金；
    La: 代表A货币本金；
    Lb: 代表B货币本金；
    Ra: 代表针对A货币本金的利率；
    Rb: 代表针对B货币本金的利率；
    ya: 代表在合约定价日针对A货币本金并对应不同期限、连续复利的零息利率，用数组格式输入；
    yb: 代表在合约定价日针对B货币本金并对应不同期限、连续复利的零息利率，用数组格式输入；
    E: 代表合约定价日的即期汇率，标价方式是1单位B货币对A货币的数量；
    m: 代表每年交换利息的频次；
    t: 代表合约定价日距离剩余每期利息交换日的期限长度，用数组格式输入；
    trader: 代表交易方，输入trader='A'表示A交易方，输入其他则表示B交易方。'''
    if types == '双固定利率货币互换':
        # 计算对应A货币本金的固定利率债券价值
        Bond_A = (Ra * np.sum(exp(-ya * t)) / m + exp(-ya[-1] * t[-1])) * La
        # 计算对应B货币本金的固定利率债券价值
        Bond_B = (Rb * np.sum(exp(-yb * t)) / m + exp(-yb[-1] * t[-1])) * Lb
        if trader == 'A':
            # 计算货币互换合约的价值（以A货币计价）
            swap_value = Bond_A - Bond_B * E
        else:
            # 计算货币互换合约的价值（以B货币计价）
            swap_value = Bond_B - Bond_A / E
    elif types == '双浮动利率货币互换':
        # 计算对应A货币本金的浮动利率债券价值
        Bond_A = (Ra / m + 1) * exp(-ya[0] * t[0]) * La
        # 计算对应B货币本金的浮动利率债券价值
        Bond_B = (Rb / m + 1) * exp(-yb[0] * t[0]) * Lb
        if trader == 'A':
            swap_value = Bond_A - Bond_B * E
        else:
            swap_value = Bond_B - Bond_A / E
    else:
        # 固定对浮动货币互换：A货币固定，B货币浮动
        Bond_A = (Ra * np.sum(exp(-ya * t)) / m + exp(-ya[-1] * t[-1])) * La
        Bond_B = (Rb / m + 1) * exp(-yb[0] * t[0]) * Lb
        if trader == 'A':
            swap_value = Bond_A - Bond_B * E
        else:
            swap_value = Bond_B - Bond_A / E
    return swap_value
