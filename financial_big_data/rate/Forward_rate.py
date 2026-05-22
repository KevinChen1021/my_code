"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def Forward_rate(R1, R2, T1, T2):
    '''定义计算远期利率的函数
    R1: 表示期限为T1的即期利率
    R2: 表示期限为T2的即期利率
    T1: 表示零息利率R1的期限长度
    T2: 表示零息利率R2的期限长度'''
    forward = R2 + (R2 - R1) * T1 / (T2 - T1)  # 计算远期利率的表达式
    return forward
