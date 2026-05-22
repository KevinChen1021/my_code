"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def N_future(h, Q_A, Q_F):
    '''定义计算套期保值最优合约数量的函数
    h: 最优套期比率
    Q_A: 被套期保值资产的数量（或金额）
    Q_F: 1份期货合约的规模（或金额）'''
    N = h * Q_A / Q_F
    return N
