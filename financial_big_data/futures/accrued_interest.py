"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def accrued_interest(par, c, m, t1, t2, t3, t4, rule):
    '''定义按照不同计息天数规则计算债券期间应计利息的函数
    par: 债券本金
    c: 债券票面利率
    m: 每年付息频次
    t1: 非参考期间起始日（datetime对象）
    t2: 非参考期间到期日（datetime对象）
    t3: 参考期间起始日（datetime对象）
    t4: 参考期间到期日（datetime对象）
    rule: 计息天数规则（'actual/actual'/'actual/360'/'actual/365'）'''
    d1 = (t2 - t1).days  # 非参考期间天数
    if rule == "actual/actual":
        d2 = (t4 - t3).days  # 参考期间天数
        interest = (d1 / d2) * par * c / m
    elif rule == "actual/360":
        interest = (d1 / 360) * par * c
    else:
        interest = (d1 / 365) * par * c
    return interest
