"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def swap_value(R_fix, R_flt, t, y, m, L, position):
    '''定义一个计算互换合约存续期内利率互换合约价值的函数
    R_fix: 代表合约存续期的固定利率（互换利率）；
    R_flt: 代表距离合约估价日最近的下一期利息交换的浮动利率；
    t: 代表估价日距离各期利息交换日期的期限（年），用数组格式输入；
    y: 代表期限为t并且连续复利的零息利率（贴现利率），用数组格式输入；
    m: 代表利率互换合约每年交换利息的频次；
    L: 代表利率互换合约的本金；
    position: 代表头寸方向，输入position='long'代表多头（支付固定利息、收取浮动利息），输入其他代表空头（支付浮动利息、收取固定利息）。'''
    # 计算固定利率债券价值
    B_fix = (R_fix * sum(exp(-y*t))/m + exp(-y[-1]*t[-1]))*L
    # 计算浮动利率债券价值
    B_flt = (R_flt/m + 1) * exp(-y[0] * t[0]) * L
    if position == 'long':
        # 计算互换利率合约的多头价值
        value = B_flt - B_fix
    else:
        # 计算互换利率合约的空头价值
        value = B_fix - B_flt
    return value
