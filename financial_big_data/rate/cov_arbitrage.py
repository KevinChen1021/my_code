"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def cov_arbitrage(Ea, Eb, Fa, Fb, L_A, L_B, R_A, R_B, T, A, B):
    '''定义一个计算抵补套利收益并给出套利路径的函数，两种货币分别是A货币和B货币
    Ea: 代表A货币兑换B货币的即期汇率卖出价，以若干单位A货币表示1单位B货币
    Eb: 代表A货币兑换B货币的即期汇率买入价，标价方式与Ea相同
    Fa: 代表A货币兑换B货币的远期汇率卖出价，标价方式与Ea相同
    Fb: 代表A货币兑换B货币的远期汇率买入价，标价方式与Ea相同
    L_A: 套利初始时刻借入的A货币本金
    L_B: 套利初始时刻借入的B货币本金
    R_A: 代表A货币的利率（收益率），并且每年复利1次
    R_B: 代表B货币的利率（收益率），并且每年复利1次
    T: 套利的期限长度，单位是年
    A: 代表A货币的名称，例如A='人民币'代表A货币是人民币
    B: 代表B货币的名称，例如B='美元'代表B货币是美元'''
    if Fb * (1 + R_B * T) / (Ea * (1 + R_A * T)) > 1:
        # 期初借入A货币、期末偿还A货币的套利路径成功
        profit = (Fb * (1 + R_B * T) / Ea - (1 + R_A * T)) * L_A
        sequence = [
            '套利路径如下',
            '第1步，初始借入的货币：', A,
            '第2步，按即期汇率兑换后并投资的货币：', B,
            '第3步，在投资结束时按远期汇率兑换后的货币：', A,
            '第4步，偿还初始借入的本金和利息'
        ]
    elif Eb * (1 + R_A * T) / (Fa * (1 + R_B * T)) > 1:
        # 期初借入B货币、期末偿还B货币的套利路径成功
        profit = (Eb * (1 + R_A * T) / Fa - (1 + R_B * T)) * L_B
        sequence = [
            '套利路径如下',
            '第1步，初始借入的货币：', B,
            '第2步，按即期汇率兑换后并投资的货币：', A,
            '第3步，在投资结束时按远期汇率兑换后的货币：', B,
            '第4步，偿还初始借入的本金和利息'
        ]
    else:
        # 不存在套利机会
        profit = 'Na'
        sequence = '套利机会不存在'
    return [profit, sequence]
