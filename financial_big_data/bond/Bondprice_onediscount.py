"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def Bondprice_onediscount(C,M,m,y,t):
    '''定义一个基于单一贴现率计算债券价格的函数。
    C: 代表债券的票面利率，如果输入0则表示零息债券
    M: 代表债券的本金（面值）。
    m: 代表债券利息每年支付的频次。
    y.: 代表单一贴现率。
    t: 代表定价日至后续每一期票息支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    if C==0:
        price=np.exp(-y*t)*M
    else:
        coupon=np.ones_like(t)*(M*C/m)
        NPV_coupon=np.sum(coupon*np.exp(-y*t))
        NPV_par=M*np.exp(-y*t[-1])
        price=NPV_coupon+NPV_par
    return price
