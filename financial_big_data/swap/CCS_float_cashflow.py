"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def CCS_float_cashflow(La, Lb, Ra_flt, Rb_flt, m, T, trader, par):
    '''定义一个计算双方浮动利率货币互换在存续期间每期现金流的函数
    La: 代表在合约初始日A交易方支付的一种货币本金（合约到期日A交易方收回的货币本金）；
    Lb: 代表在合约初始日A交易方支付的另一种货币本金（合约到期日A交易方收回的货币本金）；
    Ra_flt: 代表基于本金La的浮动利率，以数组格式输入；
    Rb_flt: 代表基于本金Lb的浮动利率，以数组格式输入；
    m: 代表货币互换合约每年交换利息的频次；
    T: 代表货币互换合约的期限（年）；
    trader: 代表合约的交易方，输入trader='A'表示计算A交易方的期间现金流，输入其他则计算B交易方的期间现金流；
    par: 代表计算现金流所依据的本金，输入par='La'表示基于本金La，输入其他则基于本金Lb。'''
    cashflow = np.zeros(m*T + 1)  # 创建存放每期现金流的初始数组
    if par == 'La':
        # 依据本金La计算现金流
        cashflow[0] = La  # A交易方第1期的现金流
        cashflow[1:-1] = Ra_flt[:-1] * La / m  # A交易方第2期至倒数第2期的现金流
        cashflow[-1] = (Ra_flt[-1] / m + 1) * La  # A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow  # 针对B交易方
    else:
        # 依据本金Lb计算现金流
        cashflow[0] = Lb  # A交易方第1期的现金流
        cashflow[1:-1] = -Rb_flt[:-1] * Lb / m  # A交易方第2期至倒数第2期的现金流
        cashflow[-1] = -(Rb_flt[-1] / m + 1) * Lb  # A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow
