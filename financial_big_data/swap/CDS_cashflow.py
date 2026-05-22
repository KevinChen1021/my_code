"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def CDS_cashflow(S, m, t1, t2, L, recovery, trader, event):
    '''定义一个计算信用违约互换期间现金流的函数
    S: 代表信用违约互换的价差（用于计算信用保护费用）；
    m: 代表信用违约互换每年支付的频次，并且不超过2次；
    t1: 代表合约的期限（年）；
    t2: 代表合约初始日距离信用事件发生日的期限长度（年），信用事件未发生则输入t2='Na'；
    L: 代表合约的本金；
    recovery: 代表信用事件发生时的回收率，信用事件未发生则输入recovery='Na'；
    trader: 代表交易方，输入trader='buyer'表示买方，输入其他则表示卖方；
    event: 代表信用事件，输入event='N'表示合约存续期内信用事件未发生，输入其他则表示合约存续期内信用事件发生。'''
    # 步骤1：合约到期未发生信用事件时计算现金流
    if event == 'N':
        n = int(t1 * m)  # 计算期间现金流支付的次数
        cashflow = S * t1 * np.ones(n) / m  # 合约期间支付的信用保护费用金额的现金流
        if trader == 'buyer':
            CF = -cashflow  # 针对信用保护买方的期间现金流
        else:
            CF = cashflow  # 针对信用保护卖方的期间现金流
    # 步骤2：合约存续期内发生信用事件且每年支付1次
    else:
        default_pay = (1 - recovery) * L  # 信用事件发生时买方支付的赔偿性支付
        if m == 1:
            n = int(t2 * m)  # 计算期间现金流支付的次数
            cashflow = (S * t2 * np.ones(n)) / m  # 计算期间的现金流（最后一个元素后面要调整）
            spread_end = (t2 - int(t2)) * S * L  # 合约最后一期（信用事件发生日）支付的信用保护费用
            cashflow[-1] = spread_end - default_pay  # 合约最后一期的现金流
            if trader == 'buyer':
                CF = cashflow
            else:
                CF = cashflow
    # 步骤3：合约存续期内发生信用事件且每年支付2次
        else:
            if t2 - int(t2) < 0.5:  # 信用事件发生在前半年
                n = int(t2 * m)
                cashflow = (S * t2 * np.ones(n)) / m
                spread_end = (t2 - int(t2)) * S * L
                cashflow[-1] = spread_end - default_pay
            else:  # 信用事件发生在后半年
                n = (int(t2) + 1) * m
                cashflow = (S * t2 * np.ones(n)) / m + 0.5 * S * L
                spread_end = (t2 - int(t2) - 0.5) * S * L
                cashflow[-1] = spread_end - default_pay
            if trader == 'buyer':
                CF = -cashflow
            else:
                CF = cashflow
        return CF
