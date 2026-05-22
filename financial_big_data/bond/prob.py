"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so


def prob(y1,y2,R,T):
    '''定义一个计算违约概率并且计算连续复利的概率的函数
    y1: 代表无风险零息利率，并且是连续复利。
    y2: 代表存在信用风险的债券到期收益率，并且是连续复利。
    R: 代表债券的违约回收率。
    T: 代表债券的期限（年）'''
    A=(np.exp(-y2*T)-R*np.exp(-y1*T))/(1-R)  #式(7-22)中的圆括号内的表达式
    prob=-np.log(A)/T-y1  #计算连续复利的违约概率
    return prob
