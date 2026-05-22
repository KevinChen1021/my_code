"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def IRS_cashflow(R_flt, R_fix, L, m, position):
    '''定义一个计算利率互换合约存续期内每期支付净息额的函数
    R_flt: 代表利率互换的每期浮动利率，以数组格式输入；
    R_fix: 代表利率互换的固定利率；
    L: 代表利率互换的本金；
    m: 代表利率互换存续期内每年交换利息的频次；
    position: 代表头寸方向，输入position='long'代表多头（支付固定利息、收取浮动利息），输入其他代表空头（支付浮动利息、收取固定利息）。'''
    if position == 'long':
        # 计算利率互换多头时期的净现金流
        cashflow = (R_flt - R_fix) * L / m
    else:
        # 计算利率互换空头时期的净现金流
        cashflow = (R_fix - R_flt) * L / m
    return cashflow
