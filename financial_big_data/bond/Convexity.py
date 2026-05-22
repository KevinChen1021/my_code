"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def Convexity(C,M,m,y,t):
    '''定义一个计算债券凸性的函数
    C: 代表债券的票面利率。
    M: 代表债券的面值。
    m: 代表债券票息每年支付的频次。
    y: 代表债券的到期收益率（连续复利）。
    t: 代表定价日至后续每一期现金流支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    if C==0:
        convexity=np.power(t,2)  #针对零息债券，计算零息债券的凸性
    else:
        coupon=np.ones_like(t)*M*C/m  #创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-y*t))  #计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-y*t[-1])  #计算本金在定价日的现值
        price=NPV_coupon+NPV_par  #计算定价日的债券价格
        cashflow=coupon  #先将现金流设定等于票息
        cashflow[-1]=M*(1+C/m)  #数组最后的元素等于票息与本金之和
        weight=cashflow*np.exp(-y*t)/price  #计算每期现金流时间的权重
        convexity=np.sum(np.power(t,2)*weight)  #计算带票息债券的凸性
    return convexity
