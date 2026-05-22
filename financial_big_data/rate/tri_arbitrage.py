"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def tri_arbitrage(L, E1a, E1b, E2a, E2b, E3a, E3b, A, B, C):
    '''定义一个计算汇率三角套利收益并显示套利路径的函数，
    并且包括A货币、B货币以及C货币共计3种货币
    L: 代表以A货币计价的初始套利本金
    E1a: 代表A货币兑换B货币的汇率卖出价，标价是以若干单位A货币表示1单位B货币
    E1b: 代表A货币兑换B货币的汇率买入价，标价方式与E1a相同
    E2a: 代表B货币兑换C货币的汇率卖出价，标价是以若干单位B货币表示1单位C货币
    E2b: 代表B货币兑换C货币的汇率买入价，标价方式与E2a相同
    E3a: 代表A货币兑换C货币的汇率卖出价，标价是以若干单位A货币表示1单位C货币
    E3b: 代表A货币兑换C货币的汇率买入价，标价方式与E3a相同
    A: 代表A货币的名称，例如A='人民币'代表A货币是人民币
    B: 代表B货币的名称，例如B='美元'代表B货币是美元
    C: 代表C货币的名称，例如C='欧元'代表C货币是欧元'''
    if E3b / (E1a * E2a) > 1:
        # 套利路径1存在套利机会
        profit = (E3b / (E1a * E2a) - 1) * L
        path = ['套利路径: ', A, '→', B, '→', C, '→', A]
    elif E1b * E2b / E3a > 1:
        # 套利路径2存在套利机会
        profit = (E1b * E2b / E3a - 1) * L
        path = ['套利路径: ', A, '→', C, '→', B, '→', A]
    else:
        # 不存在套利机会
        profit = 0
        path = ['不存在套利机会']
    return [profit, path]
