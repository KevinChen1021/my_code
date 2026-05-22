"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def stack_roll(F_open, F_close, M, N, position):
    '''定义计算滚动套期保值期间期货组合盈亏的函数
    F_open: 代表期货的开仓时的期货价格，以数组格式输入
    F_close: 代表期货合约平仓时的期货价格，以数组格式输入
    M: 代表合约乘数
    N: 代表持有期货合约的数量
    position: 代表期货合约的头寸方向，输入position='long'表示多头头寸，输入其他则表示空头头寸'''
    if position == 'long':
        # 多头套期保值，计算每次期货合约移仓的盈亏
        profit_list = (F_close - F_open) * M * N
    else:
        # 空头套期保值，计算每次期货合约移仓的盈亏
        profit_list = (F_open - F_close) * M * N
    # 计算套期保值期间期货合约的盈亏合计
    profit_sum = np.sum(profit_list)
    return profit_sum
