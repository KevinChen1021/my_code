"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def Mod_Duration(C,M,m1,m2,y,t):
    '''定义一个计算债券修正久期的函数
    C: 代表债券的票面利率。
    M: 代表债券的面值。
    m1: 代表债券票息每年支付的频次。
    m2: 代表债券到期收益率每年复利频次，通常m2等于m1。
    y: 代表每年复利m2次的到期收益率。
    t: 代表定价日至后续每一期现金流支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    if C==0:
        Macaulay_duration=t  #针对零息债券，计算零息债券的麦考利久期
    else:
        r=m2*np.log(1+y/m2)  #计算等价的连续复利的到期收益率
        coupon=np.ones_like(t)*M*C/m1  #创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-r*t))  #计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-r*t[-1])  #计算本金在定价日的现值
        price=NPV_coupon+NPV_par  #计算定价日的债券价格
        cashflow=coupon  #先将现金流设定等于票息
        cashflow[-1]=M*(1+C/m1)  #数组最后的元素等于票息与本金之和
        weight=cashflow*np.exp(-r*t)/price  #计算时间的权重
        Macaulay_duration=np.sum(t*weight)  #计算带票息债券的麦考利久期
    Modified_duration=Macaulay_duration/(1+y/m2)  #计算债券的修正久期
    return Modified_duration
