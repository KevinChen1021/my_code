"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def YTM(P,C,M,m,t):
    '''定义一个计算针对零息债券到期收益率的函数
    P: 代表观察到的债券市场价格。
    C: 代表债券的票面利率。
    M: 代表债券的本金。
    m: 代表债券利息每年支付的频次。
    t: 代表定价日至后续每一期票息支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    import scipy.optimize as so  #导入SciPy的子模块optimize
    def f(y):  #需要再自定义一个函数
        coupon=np.ones_like(t)*M*C/m  #创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-y*t))  #计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-y*t[-1])  #计算本金在定价日的现值
        value=NPV_coupon+NPV_par  #定价日的债券现金流现值之和
        return value-P  #债券现金流现值之和减去债券市场价格
    if C==0:
        y=(np.log(M/P))/t  #计算零息债券的到期收益率
    else:
        y=so.fsolve(f, x0=0.1)  #针对带票息债券，第2个参数是任意输入的初始值
    return y
