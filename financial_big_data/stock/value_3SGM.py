"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import statsmodels.api as sm


def value_3SGM(D, ga, gb, Tb, Tr, r):
    '''定义一个运用三阶段增长模型计算股票内在价值的函数
    D: 代表企业已支付的最近一期每股股息金额。
    ga: 代表企业在第1个阶段的股息增长率。
    gb: 代表企业在第3个阶段的股息增长率，并且数值要小于贴现利率。
    Tb: 代表企业第1个阶段与第2个阶段的期限之和（年）。
    Tr: 代表企业第1个阶段的期限（年）。
    r: 代表与企业的风险相匹配的贴现利率（每年复利1次）'''
    # 为了更好理解代码的编写逻辑，分为以下4个步骤
    # 第1步：计算第1个阶段股息贴现之和
    if r > gb:  # 贴现利率大于第3个阶段的股息增长率
        Ta_list = np.arange(1, Tr + 1)  # 创建从1到Ta的自然数组
        D_stagel = D * np.power(1 + ga, Ta_list)  # 计算第1个阶段每期股息金额的数组
        V1 = np.sum(D_stagel / np.power(1 + r, Ta_list))  # 计算第1个阶段股息贴现之和

        # 第2步：计算第2个阶段股息贴现之和
        Tb_list = np.arange(Tr + 1, Tb + 1)  # 创建从Ta+1到Tb的自然数组
        D_r = D_stagel[-1]  # 第1个阶段最后一期股息
        D_stage2 = []  # 创建存放第2个阶段每期股息的空列表
        for i in range(len(Tb_list)):
            gt = ga - (ga - gb) * (Tb_list[i] - Tr) / (Tb - Tr)  # 依次计算第2个阶段每期股息增长率
            D_t = D_r * np.power(1 + gt, 1)  # 依次计算第2个阶段每期股息金额
            D_stage2.append(D_t)  # 将计算得到的每期股息添加至列表尾部
            D_r = D_t  # 将列表转换为数组格式
        V2 = np.sum(np.array(D_stage2) / np.power(1 + r, Tb_list))  # 计算第2个阶段股息贴现之和

        # 第3步：计算第3个阶段股息贴现之和
        D_Tb = D_stage2[-1]  # 第2个阶段最后一期股息
        V3 = D_Tb * (1 + gb) / (np.power(1 + r, Tb) * (r - gb))  # 计算第3个阶段股息贴现之和

        # 第4步：计算股票的内在价值
        value = V1 + V2 + V3  # 计算股票的内在价值
    else:  # 贴现利率小于或等于第3个阶段的股息增长率
        value = '输入的贴现利率小于或等于第3个阶段的股息增长率而导致结果不存在'
    return value
