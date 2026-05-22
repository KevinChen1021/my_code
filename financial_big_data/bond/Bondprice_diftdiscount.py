"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def Bondprice_diftdiscount(C,M,m,y,t):
    '''定义一个基于不同期限现贴现率计算债券价格的函数。
    C: 代表债券的票面利率，如果输入0则表示零息债券。
    M: 代表债券的本金。
    m: 代表不同期限的贴现率，用数组格式输入；零息债券可直接输入数字。
    y: 代表定价日至后续每一期票息支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    if C==0:
        price=np.exp(-y*t)*M  #针对零息债券
    else:
        coupon=np.ones_like(y)*M*C/m  #创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-y*t))  #计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-y[-1]*t[-1])  #计算本金在定价日的现值
        price=NPV_coupon+NPV_par  #计算定价日的债券价格
    return price
