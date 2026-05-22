"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def exchange(M, N, Ea, Eb, curr_A, curr_B, direction):
    '''定义一个计算汇兑金额的函数，并且两种货币分别是A货币和B货币
    M: 表示汇兑前的金额，如果计算汇兑后的金额则输入M='Na'
    N: 表示汇兑后的金额，如果计算汇兑前的金额则输入N='Na'
    Ea: 表示银行的汇率卖出价，标价方式是以若干单位A货币表示1单位B货币
    Eb: 表示银行的汇率买入价，标价方式与Ea相同
    curr_A: 表示A货币的名称，比如curr_A='人民币'表示币种是人民币
    curr_B: 表示B货币的名称，比如curr_B='美元'表示币种是美元
    direction: 表示货币兑换方向，direction='A to B'表示企业向银行用A货币兑换B货币，其他就表示企业向银行用B货币兑换为A货币'''
    if direction == 'A to B':
        # 企业向银行用A货币兑换为B货币
        if N == 'Na':
            # 计算汇兑后的金额
            value = M / Ea
            currency = curr_B
        else:
            # 计算汇兑前的金额
            value = N * Ea
            currency = curr_A
    else:
        # 企业向银行用B货币兑换为A货币
        if N == 'Na':
            # 计算汇兑后的金额
            value = M * Eb
            currency = curr_A
        else:
            # 计算汇兑前的金额
            value = N / Eb
            currency = curr_B
    return [value, currency]
