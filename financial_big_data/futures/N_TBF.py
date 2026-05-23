"""Function module for n_tbf."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def n_tbf(futures_price, par_value, value, discount_factor, discounted_price):
    '''计算基于久期套期保值的国债期货合约数量的函数
    PF: 期货价格
    par: 1手国债期货合约基础资产对应的国债面值
    value: 被套期保值投资组合当前市值
    Df: 期货合约基础资产在套期保值到期日的麦考利久期
    Dp: 被套期保值投资组合在套期保值到期日的麦考利久期'''
    value_TBF = futures_price * par_value  # 1手国债期货合约的价格
    N = value * discounted_price / (value_TBF * discount_factor)  # 计算合约数量
    return N
