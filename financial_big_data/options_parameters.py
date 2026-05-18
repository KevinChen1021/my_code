import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from pandas.plotting import register_matplotlib_converters
from scipy.stats import norm
from numpy import log, exp, sqrt, power
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
register_matplotlib_converters()


'''Delta'''
# 1. 定义欧式期权Delta计算函数
def delta_EurOpt(S, K, sigma, r, T, optype, positype):
    '''计算欧式期权Delta的函数
    S: 基础资产价格
    K: 行权价格
    sigma: 年化波动率
    r: 连续复利无风险收益率
    T: 期权期限（年）
    optype: 期权类型（'call'=看涨，其他=看跌）
    positype: 头寸方向（'long'=多头，其他=空头）'''
    d1 = (log(S/K) + (r + power(sigma, 2)/2)*T) / (sigma * sqrt(T))
    if optype == 'call':
        if positype == 'long':
            delta = norm.cdf(d1)
        else:
            delta = -norm.cdf(d1)
    else:
        if positype == 'long':
            delta = norm.cdf(d1) - 1
        else:
            delta = 1 - norm.cdf(d1)
    return delta


# 2. 定义BSM期权定价函数
def option_BSM(S, K, sigma, r, T, opt):
    '''运用布莱克-斯科尔斯-默顿模型计算欧式期权价格'''
    d1 = (log(S/K) + (r + power(sigma, 2)/2)*T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    if opt == 'call':
        value = S * norm.cdf(d1) - K * exp(-r*T) * norm.cdf(d2)
    else:
        value = K * exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return value


# # 3. 农业银行期权Delta计算
# # 参数设置
# S_ABC = 3.27         # 农业银行股价
# K_ABC = 3.6          # 行权价格
# sigma_ABC = 0.19     # 年化波动率
# shibor_6M = 0.02377  # 6个月期Shibor
# T_ABC = 0.5          # 期权期限（年）
#
# # 计算不同类型期权的Delta
# delta_EurOpt1 = delta_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='call', positype='long')
# delta_EurOpt2 = delta_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='call', positype='short')
# delta_EurOpt3 = delta_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='put', positype='long')
# delta_EurOpt4 = delta_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='put', positype='short')
#
# print('农业银行A股欧式看涨期权多头的Delta', round(delta_EurOpt1, 4))
# print('农业银行A股欧式看涨期权空头的Delta', round(delta_EurOpt2, 4))
# print('农业银行A股欧式看跌期权多头的Delta', round(delta_EurOpt3, 4))
# print('农业银行A股欧式看跌期权空头的Delta', round(delta_EurOpt4, 4))
#
#
# # 4. BSM价格与Delta近似价格的对比
# S_list1 = np.linspace(2.5, 4.5, 200)
# value_list = option_BSM(S=S_list1, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, opt='call')
# value_one = option_BSM(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, opt='call')
# value_approx1 = value_one + delta_EurOpt1 * (S_list1 - S_ABC)
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(S_list1, value_list, 'b-', label=u'运用BSM模型计算得到的看涨期权价格', lw=2.5)
# plt.plot(S_list1, value_approx1, 'r-', label=u'运用Delta计算得到的看涨期权近似价格', lw=2.5)
# plt.plot(S_ABC, value_one, 'o', label=u'股价等于3.27元/股对应的期权价格', lw=2.5)
# plt.xlabel(u'股票价格', fontsize=13)
# plt.ylabel(u'期权价格', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'运用BSM模型计算得到的期权价格与运用Delta计算得到的近似期权价格的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 5. 股票价格与欧式期权多头Delta的关系
# S_list2 = np.linspace(1.0, 6.0, 200)
# Delta_EurCall = delta_EurOpt(S=S_list2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='call', positype='long')
# Delta_EurPut = delta_EurOpt(S=S_list2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='put', positype='long')
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(S_list2, Delta_EurCall, 'b-', label=u'欧式看涨期权多头', lw=2.5)
# plt.plot(S_list2, Delta_EurPut, 'r-', label=u'欧式看跌期权多头', lw=2.5)
# plt.xlabel(u'股票价格', fontsize=13)
# plt.ylabel(u'Delta', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'股票价格与欧式期权多头Delta', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 6. 期权期限与欧式看涨期权多头Delta的关系
# S1 = 4.0  # 实值看涨期权股价
# S2 = 3.6  # 平值看涨期权股价
# S3 = 3.0  # 虚值看涨期权股价
# T_list = np.linspace(0.1, 5.0, 200)
#
# Delta_list1 = delta_EurOpt(S=S1, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list, optype='call', positype='long')
# Delta_list2 = delta_EurOpt(S=S2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list, optype='call', positype='long')
# Delta_list3 = delta_EurOpt(S=S3, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list, optype='call', positype='long')
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(T_list, Delta_list1, 'b-', label=u'实值看涨期权多头', lw=2.5)
# plt.plot(T_list, Delta_list2, 'r-', label=u'平值看涨期权多头', lw=2.5)
# plt.plot(T_list, Delta_list3, 'g-', label=u'虚值看涨期权多头', lw=2.5)
# plt.xlabel(u'期权期限', fontsize=13)
# plt.ylabel(u'Delta', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'期权期限与欧式看涨期权多头Delta的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


'''Delta hedging'''
import datetime as dt


# # 1. Delta对冲股票数量计算
# N_put = 1e6  # 看跌期权多头头寸
# delta_EurOpt3 = delta_EurOpt(S=3.27, K=3.6, sigma=0.19, r=0.02377, T=0.5, optype='put', positype='long')
# N_ABC = int(np.abs(delta_EurOpt3 * N_put))
# print('2020年7月16日买入基于期权Delta对冲的农业银行A股数量', N_ABC)
#
# # 2. 静态对冲策略下的投资组合盈亏
# # 时间与参数设置
# T0 = dt.datetime(2020, 7, 16)
# T1 = dt.datetime(2020, 8, 31)
# T2 = dt.datetime(2021, 1, 16)
# T_new = (T2 - T1).days / 365
# S_Aug31 = 3.21
# shibor_Aug31 = 0.02636
#
# # 计算期权价格
# put_Jul16 = option_BSM(S=3.27, K=3.6, sigma=0.19, r=0.02377, T=0.5, opt='put')
# put_Aug31 = option_BSM(S=S_Aug31, K=3.6, sigma=0.19, r=shibor_Aug31, T=T_new, opt='put')
# print('2020年7月16日农业银行A股欧式看跌期权价格', round(put_Jul16, 4))
# print('2020年8月31日农业银行A股欧式看跌期权价格', round(put_Aug31, 4))
#
# # 计算静态对冲盈亏
# port_chagvalue = N_ABC * (S_Aug31 - 3.27) + N_put * (put_Aug31 - put_Jul16)
# print('静态对冲策略下2020年8月31日投资组合的累积盈亏', round(port_chagvalue, 2))
#
# # 3. 动态Delta中性调整
# delta_Aug31 = delta_EurOpt(S=S_Aug31, K=3.6, sigma=0.19, r=shibor_Aug31, T=T_new, optype='put', positype='long')
# print('2020年8月31日农业银行A股欧式看跌期权Delta', round(delta_Aug31, 4))
#
# N_ABC_new = int(np.abs(delta_Aug31 * N_put))
# print('2020年8月31日保持Delta中性而用于对冲的农业银行A股股票数量', N_ABC_new)
#
# N_ABC_change = N_ABC_new - N_ABC
# print('2020年8月31日保持Delta中性而发生的股票数量变化', N_ABC_change)


# 4. 美式期权Delta计算函数
def delta_AmerCall(S, K, sigma, r, T, N, positype):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    call_matrix = np.zeros((N + 1, N + 1))
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(S_end - K, 0)

    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)
            call_strike = np.maximum(Si - K, 0)
            call_nostrike = np.exp(-r * t) * (p * call_matrix[i + 1, j + 1] + (1 - p) * call_matrix[i + 1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)

    Delta = (call_matrix[0, 1] - call_matrix[1, 1]) / (S * u - S * d)
    if positype == 'long':
        result = Delta
    else:
        result = -Delta
    return result


def delta_AmerPut(S, K, sigma, r, T, N, positype):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    put_matrix = np.zeros((N + 1, N + 1))
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(K - S_end, 0)

    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)
            put_strike = np.maximum(K - Si, 0)
            put_nostrike = np.exp(-r * t) * (p * put_matrix[i + 1, j + 1] + (1 - p) * put_matrix[i + 1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)

    Delta = (put_matrix[0, 1] - put_matrix[1, 1]) / (S * u - S * d)
    if positype == 'long':
        result = Delta
    else:
        result = -Delta
    return result

#
# # 5. 美式期权Delta计算
# step = 100
# delta_AmerOpt1 = delta_AmerCall(S=3.27, K=3.6, sigma=0.19, r=0.02377, T=0.5, N=step, positype='long')
# delta_AmerOpt2 = delta_AmerCall(S=3.27, K=3.6, sigma=0.19, r=0.02377, T=0.5, N=step, positype='short')
# delta_AmerOpt3 = delta_AmerPut(S=3.27, K=3.6, sigma=0.19, r=0.02377, T=0.5, N=step, positype='long')
# delta_AmerOpt4 = delta_AmerPut(S=3.27, K=3.6, sigma=0.19, r=0.02377, T=0.5, N=step, positype='short')
#
# print('农业银行A股美式看涨期权多头的Delta', round(delta_AmerOpt1, 4))
# print('农业银行A股美式看涨期权空头的Delta', round(delta_AmerOpt2, 4))
# print('农业银行A股美式看跌期权多头的Delta', round(delta_AmerOpt3, 4))
# print('农业银行A股美式看跌期权空头的Delta', round(delta_AmerOpt4, 4))


'''Gamma'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
from numpy import log, exp, sqrt, power, pi


# 复用之前定义的函数
def delta_EurOpt(S, K, sigma, r, T, optype, positype):
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    if optype == 'call':
        if positype == 'long':
            delta = norm.cdf(d1)
        else:
            delta = -norm.cdf(d1)
    else:
        if positype == 'long':
            delta = norm.cdf(d1) - 1
        else:
            delta = 1 - norm.cdf(d1)
    return delta


def option_BSM(S, K, sigma, r, T, opt):
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    if opt == 'call':
        value = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        value = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return value


# 1. 定义欧式期权Gamma计算函数
def gamma_EurOpt(S, K, sigma, r, T):
    '''计算欧式期权Gamma的函数'''
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    gamma = exp(-power(d1, 2) / 2) / (S * sigma * sqrt(2 * pi * T))
    return gamma


# # 2. 农业银行期权Gamma计算
# S_ABC = 3.27
# K_ABC = 3.6
# sigma_ABC = 0.19
# shibor_6M = 0.02377
# T_ABC = 0.5
#
# gamma_Eur = gamma_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC)
# print('农业银行A股欧式期权的Gamma', round(gamma_Eur, 4))
#
# # 3. Delta+Gamma近似期权价格与BSM价格对比
# S_list1 = np.linspace(2.5, 4.5, 200)
# value_list = option_BSM(S=S_list1, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, opt='call')
# value_one = option_BSM(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, opt='call')
# delta_EurOpt1 = delta_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='call', positype='long')
# value_approx1 = value_one + delta_EurOpt1 * (S_list1 - S_ABC)
# value_approx2 = value_one + delta_EurOpt1 * (S_list1 - S_ABC) + 0.5 * gamma_Eur * power(S_list1 - S_ABC, 2)
#
# plt.figure(figsize=(9, 6))
# plt.plot(S_list1, value_list, 'b-', label=u'运用BSM模型计算的看涨期权价格', lw=2.5)
# plt.plot(S_list1, value_approx1, 'r-', label=u'仅用Delta计算的看涨期权近似价格', lw=2.5)
# plt.plot(S_list1, value_approx2, 'o-', label=u'用Delta和Gamma计算的看涨期权近似价格', lw=2.5)
# plt.plot(S_ABC, value_one, 'o', label=u'股价等于3.27元/股对应的期权价格', lw=2.5)
# plt.xlabel(u'股票价格', fontsize=13)
# plt.ylabel(u'期权价格', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'运用BSM模型、仅用Delta以及用Delta和Gamma计算的期权价格', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
# # 4. 股票价格与期权Gamma的关系
# S_list2 = np.linspace(1.0, 6.0, 200)
# gamma_list = gamma_EurOpt(S=S_list2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC)
#
# plt.figure(figsize=(9, 6))
# plt.plot(S_list2, gamma_list, 'b-', lw=2.5)
# plt.xlabel(u'股票价格', fontsize=13)
# plt.ylabel('Gamma', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'股票价格与期权Gamma的关系图', fontsize=13)
# plt.grid()
# plt.show()
#
# # 5. 期权期限与不同状态看涨期权Gamma的关系
# S1 = 4.0
# S2 = 3.6
# S3 = 3.0
# T_list = np.linspace(0.1, 5.0, 200)
#
# gamma_list1 = gamma_EurOpt(S=S1, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list)
# gamma_list2 = gamma_EurOpt(S=S2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list)
# gamma_list3 = gamma_EurOpt(S=S3, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list)
#
# plt.figure(figsize=(9, 6))
# plt.plot(T_list, gamma_list1, 'b-', label=u'实值看涨期权', lw=2.5)
# plt.plot(T_list, gamma_list2, 'r-', label=u'平值看涨期权', lw=2.5)
# plt.plot(T_list, gamma_list3, 'g-', label=u'虚值看涨期权', lw=2.5)
# plt.xlabel(u'期权期限', fontsize=13)
# plt.ylabel('Gamma', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'期权期限与期权Gamma的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


# 6. 美式期权Gamma计算函数
def gamma_AmerCall(S, K, sigma, r, T, N):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    call_matrix = np.zeros((N + 1, N + 1))
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(S_end - K, 0)

    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)
            call_strike = np.maximum(Si - K, 0)
            call_nostrike = np.exp(-r * t) * (p * call_matrix[i + 1, j + 1] + (1 - p) * call_matrix[i + 1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)

    Delta1 = (call_matrix[0, 2] - call_matrix[1, 2]) / (S * np.power(u, 2) - S)
    Delta2 = (call_matrix[1, 2] - call_matrix[2, 2]) / (S - S * np.power(d, 2))
    Gamma = (Delta1 - Delta2) / (S * np.power(u, 2) - S * np.power(d, 2))
    return Gamma


def gamma_AmerPut(S, K, sigma, r, T, N):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    put_matrix = np.zeros((N + 1, N + 1))
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(K - S_end, 0)

    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)
            put_strike = np.maximum(K - Si, 0)
            put_nostrike = np.exp(-r * t) * (p * put_matrix[i + 1, j + 1] + (1 - p) * put_matrix[i + 1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)

    Delta1 = (put_matrix[0, 2] - put_matrix[1, 2]) / (S * np.power(u, 2) - S)
    Delta2 = (put_matrix[1, 2] - put_matrix[2, 2]) / (S - S * np.power(d, 2))
    Gamma = (Delta1 - Delta2) / (S * np.power(u, 2) - S * np.power(d, 2))
    return Gamma

#
# # 7. 美式期权Gamma计算
# step = 100
# gamma_AmerOpt1 = gamma_AmerCall(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, N=step)
# gamma_AmerOpt2 = gamma_AmerPut(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, N=step)
#
# print('农业银行A股美式看涨期权的Gamma', round(gamma_AmerOpt1, 4))
# print('农业银行A股美式看跌期权的Gamma', round(gamma_AmerOpt2, 4))


'''Theta'''
# 1. 定义欧式期权Theta计算函数
def theta_EurOpt(S, K, sigma, r, T, optype):
    '''计算欧式期权Theta的函数'''
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    # 计算看涨期权Theta
    theta_call = (S * sigma * exp(-power(d1, 2) / 2)) / (2 * sqrt(2 * pi * T)) - r * K * exp(-r * T) * norm.cdf(d2)
    # 计算看跌期权Theta（看涨+看跌平价关系）
    theta_put = theta_call + r * K * np.exp(-r * T)

    if optype == 'call':
        theta = theta_call
    else:
        theta = theta_put
    return theta

#
# # 2. 农业银行期权Theta计算（欧式）
# S_ABC = 3.27
# K_ABC = 3.6
# sigma_ABC = 0.19
# shibor_6M = 0.02377
# T_ABC = 0.5
# day1 = 365  # 日历天数
# day2 = 252  # 交易天数
#
# theta_EurCall = theta_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='call')
# theta_EurPut = theta_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='put')
#
# print('农业银行A股欧式看涨期权Theta', round(theta_EurCall, 6))
# print('农业银行A股欧式看涨期权每日历天Theta', round(theta_EurCall / day1, 6))
# print('农业银行A股欧式看涨期权每交易日Theta', round(theta_EurCall / day2, 6))
# print('农业银行A股欧式看跌期权Theta', round(theta_EurPut, 6))
# print('农业银行A股欧式看跌期权每日历天Theta', round(theta_EurPut / day1, 6))
# print('农业银行A股欧式看跌期权每交易日Theta', round(theta_EurPut / day2, 6))

# # 3. 股票价格与欧式期权Theta的关系可视化
# S_list2 = np.linspace(1.0, 6.0, 200)
# theta_EurCall_list = theta_EurOpt(S=S_list2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='call')
# theta_EurPut_list = theta_EurOpt(S=S_list2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='put')
#
# plt.figure(figsize=(9, 6))
# plt.plot(S_list2, theta_EurCall_list, 'b-', label=u'欧式看涨期权', lw=2.5)
# plt.plot(S_list2, theta_EurPut_list, 'r-', label=u'欧式看跌期权', lw=2.5)
# plt.xlabel(u'股票价格', fontsize=13)
# plt.ylabel('Theta', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'股票价格与期权Theta的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
# # 4. 期权期限与不同状态看涨期权Theta的关系可视化
# S1 = 4.0  # 实值
# S2 = 3.6  # 平值
# S3 = 3.0  # 虚值
# T_list = np.linspace(0.1, 5.0, 200)
#
# theta_list1 = theta_EurOpt(S=S1, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list, optype='call')
# theta_list2 = theta_EurOpt(S=S2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list, optype='call')
# theta_list3 = theta_EurOpt(S=S3, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list, optype='call')
#
# plt.figure(figsize=(9, 6))
# plt.plot(T_list, theta_list1, 'b-', label=u'实值看涨期权', lw=2.5)
# plt.plot(T_list, theta_list2, 'r-', label=u'平值看涨期权', lw=2.5)
# plt.plot(T_list, theta_list3, 'g-', label=u'虚值看涨期权', lw=2.5)
# plt.xlabel(u'期权期限', fontsize=13)
# plt.ylabel('Theta', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'期权期限与期权Theta的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid(True)
# plt.show()


# 5. 定义美式看涨期权Theta计算函数（N步二叉树）
def theta_AmerCall(S, K, sigma, r, T, N):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    call_matrix = np.zeros((N + 1, N + 1))
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(S_end - K, 0)

    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)
            call_strike = np.maximum(Si - K, 0)
            call_nostrike = np.exp(-r * t) * (p * call_matrix[i + 1, j + 1] + (1 - p) * call_matrix[i + 1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)

    Theta = (call_matrix[1, 2] - call_matrix[0, 0]) / (2 * t)
    return Theta


# 6. 定义美式看跌期权Theta计算函数（N步二叉树）
def theta_AmerPut(S, K, sigma, r, T, N):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    put_matrix = np.zeros((N + 1, N + 1))
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(K - S_end, 0)

    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)
            put_strike = np.maximum(K - Si, 0)
            put_nostrike = np.exp(-r * t) * (p * put_matrix[i + 1, j + 1] + (1 - p) * put_matrix[i + 1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)

    Theta = (put_matrix[1, 2] - put_matrix[0, 0]) / (2 * t)
    return Theta


# # 7. 农业银行期权Theta计算（美式）
# step = 100
# theta_AmerOpt1 = theta_AmerCall(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, N=step)
# theta_AmerOpt2 = theta_AmerPut(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, N=step)
#
# print('农业银行A股美式看涨期权的Theta', round(theta_AmerOpt1, 4))
# print('农业银行A股美式看跌期权的Theta', round(theta_AmerOpt2, 4))


'''Vega'''
# 1. 定义欧式期权Vega计算函数
def vega_EurOpt(S, K, sigma, r, T):
    '''计算欧式期权Vega的函数'''
    d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    vega = S * sqrt(T) * exp(-power(d1, 2) / 2) / sqrt(2 * pi)
    return vega


# # 2. 农业银行期权Vega计算（欧式）
# S_ABC = 3.27
# K_ABC = 3.6
# sigma_ABC = 0.19
# shibor_6M = 0.02377
# T_ABC = 0.5
#
# vega_Eur = vega_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC)
# print('农业银行A股欧式期权的Vega', round(vega_Eur, 4))
#
# # 波动率变动对应的期权价格变动
# sigma_chg = 0.01
# value_chg = vega_Eur * sigma_chg
# print('波动率增加1%导致期权价格变动额', round(value_chg, 4))
#
# # 3. 股票价格与欧式期权Vega的关系可视化
# S_list2 = np.linspace(1.0, 6.0, 200)
# vega_list = vega_EurOpt(S=S_list2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC)
#
# plt.figure(figsize=(9, 6))
# plt.plot(S_list2, vega_list, 'b-', lw=2.5)
# plt.xlabel(u'股票价格', fontsize=13)
# plt.ylabel(u'Vega', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'股票价格与期权Vega的关系图', fontsize=13)
# plt.grid()
# plt.show()

# # 4. 期权期限与不同状态看涨期权Vega的关系可视化
# S1 = 4.0  # 实值
# S2 = 3.6  # 平值
# S3 = 3.0  # 虚值
# T_list = np.linspace(0.1, 5.0, 200)
#
# vega_list1 = vega_EurOpt(S=S1, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list)
# vega_list2 = vega_EurOpt(S=S2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list)
# vega_list3 = vega_EurOpt(S=S3, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list)
#
# plt.figure(figsize=(9, 6))
# plt.plot(T_list, vega_list1, 'b-', label=u'实值看涨期权', lw=2.5)
# plt.plot(T_list, vega_list2, 'r-', label=u'平值看涨期权', lw=2.5)
# plt.plot(T_list, vega_list3, 'g-', label=u'虚值看涨期权', lw=2.5)
# plt.xlabel(u'期权期限', fontsize=13)
# plt.ylabel(u'Vega', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'期权期限与期权Vega的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


# 5. 定义美式看涨期权Vega计算函数（N步二叉树）
def vega_AmerCall(S, K, sigma, r, T, N):
    def American_call(S, K, sigma, r, T, N):
        t = T / N
        u = np.exp(sigma * np.sqrt(t))
        d = 1 / u
        p = (np.exp(r * t) - d) / (u - d)
        call_matrix = np.zeros((N + 1, N + 1))
        N_list = np.arange(0, N + 1)
        S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
        call_matrix[:, -1] = np.maximum(S_end - K, 0)

        i_list = list(range(0, N))
        i_list.reverse()
        for i in i_list:
            j_list = np.arange(i + 1)
            for j in j_list:
                Si = S * np.power(u, i - j) * np.power(d, j)
                call_strike = np.maximum(Si - K, 0)
                call_nostrike = np.exp(-r * t) * (p * call_matrix[i + 1, j + 1] + (1 - p) * call_matrix[i + 1, j])
                call_matrix[i, j] = np.maximum(call_strike, call_nostrike)
        return call_matrix[0, 0]

    Value1 = American_call(S, K, sigma, r, T, N)
    Value2 = American_call(S, K, sigma + 0.0001, r, T, N)
    vega = (Value2 - Value1) / 0.0001
    return vega


# 6. 定义美式看跌期权Vega计算函数（N步二叉树）
def vega_AmerPut(S, K, sigma, r, T, N):
    def American_put(S, K, sigma, r, T, N):
        t = T / N
        u = np.exp(sigma * np.sqrt(t))
        d = 1 / u
        p = (np.exp(r * t) - d) / (u - d)
        put_matrix = np.zeros((N + 1, N + 1))
        N_list = np.arange(0, N + 1)
        S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
        put_matrix[:, -1] = np.maximum(K - S_end, 0)

        i_list = list(range(0, N))
        i_list.reverse()
        for i in i_list:
            j_list = np.arange(i + 1)
            for j in j_list:
                Si = S * np.power(u, i - j) * np.power(d, j)
                put_strike = np.maximum(K - Si, 0)
                put_nostrike = np.exp(-r * t) * (p * put_matrix[i + 1, j + 1] + (1 - p) * put_matrix[i + 1, j])
                put_matrix[i, j] = np.maximum(put_strike, put_nostrike)
        return put_matrix[0, 0]

    Value1 = American_put(S, K, sigma, r, T, N)
    Value2 = American_put(S, K, sigma + 0.0001, r, T, N)
    vega = (Value2 - Value1) / 0.0001
    return vega


# # 7. 农业银行期权Vega计算（美式）
# step = 100
# vega_AmerOpt1 = vega_AmerCall(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, N=step)
# vega_AmerOpt2 = vega_AmerPut(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, N=step)
#
# print('农业银行A股美式看涨期权的Vega', round(vega_AmerOpt1, 4))
# print('农业银行A股美式看跌期权的Vega', round(vega_AmerOpt2, 4))


'''Rho'''
# 1. 定义欧式期权Rho计算函数
def rho_EurOpt(S, K, sigma, r, T, optype):
    '''计算欧式期权Rho的函数'''
    d2 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    if optype == 'call':
        rho = K * T * exp(-r * T) * norm.cdf(d2)
    else:
        rho = -K * T * exp(-r * T) * norm.cdf(-d2)
    return rho


# # 2. 农业银行期权Rho计算（欧式）
# S_ABC = 3.27
# K_ABC = 3.6
# sigma_ABC = 0.19
# shibor_6M = 0.02377
# T_ABC = 0.5
#
# rho_EurCall = rho_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='call')
# rho_EurPut = rho_EurOpt(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='put')
#
# print('农业银行A股欧式看涨期权的Rho', round(rho_EurCall, 4))
# print('农业银行A股欧式看跌期权的Rho', round(rho_EurPut, 4))
#
# # 无风险收益率变动对应的期权价格变动
# r_chg = 0.001
# call_chg = rho_EurCall * r_chg
# put_chg = rho_EurPut * r_chg
# print('无风险收益率上涨10个基点导致欧式看涨期权价格变化', round(call_chg, 4))
# print('无风险收益率上涨10个基点导致欧式看跌期权价格变化', round(put_chg, 4))
#
# # 3. 股票价格与欧式期权Rho的关系可视化
# S_list2 = np.linspace(1.0, 6.0, 200)
# rho_EurCall_list = rho_EurOpt(S=S_list2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='call')
# rho_EurPut_list = rho_EurOpt(S=S_list2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, optype='put')
#
# plt.figure(figsize=(9, 6))
# plt.plot(S_list2, rho_EurCall_list, 'b-', label=u'欧式看涨期权', lw=2.5)
# plt.plot(S_list2, rho_EurPut_list, 'r-', label=u'欧式看跌期权', lw=2.5)
# plt.xlabel(u'股票价格', fontsize=13)
# plt.ylabel('Rho', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'股票价格与期权Rho的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
# # 4. 期权期限与不同状态看涨期权Rho的关系可视化
# S1 = 4.0  # 实值
# S2 = 3.6  # 平值
# S3 = 3.0  # 虚值
# T_list = np.linspace(0.1, 5.0, 200)
#
# rho_list1 = rho_EurOpt(S=S1, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list, optype='call')
# rho_list2 = rho_EurOpt(S=S2, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list, optype='call')
# rho_list3 = rho_EurOpt(S=S3, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_list, optype='call')
#
# plt.figure(figsize=(9, 6))
# plt.plot(T_list, rho_list1, 'b-', label=u'实值看涨期权', lw=2.5)
# plt.plot(T_list, rho_list2, 'r-', label=u'平值看涨期权', lw=2.5)
# plt.plot(T_list, rho_list3, 'g-', label=u'虚值看涨期权', lw=2.5)
# plt.xlabel(u'期权期限', fontsize=13)
# plt.ylabel('Rho', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'期权期限与期权Rho的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


# 5. 定义美式看涨期权Rho计算函数（N步二叉树）
def rho_AmerCall(S, K, sigma, r, T, N):
    def American_call(S, K, sigma, r, T, N):
        t = T / N
        u = np.exp(sigma * np.sqrt(t))
        d = 1 / u
        p = (np.exp(r * t) - d) / (u - d)
        call_matrix = np.zeros((N + 1, N + 1))
        N_list = np.arange(0, N + 1)
        S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
        call_matrix[:, -1] = np.maximum(S_end - K, 0)

        i_list = list(range(0, N))
        i_list.reverse()
        for i in i_list:
            j_list = np.arange(i + 1)
            for j in j_list:
                Si = S * np.power(u, i - j) * np.power(d, j)
                call_strike = np.maximum(Si - K, 0)
                call_nostrike = np.exp(-r * t) * (p * call_matrix[i + 1, j + 1] + (1 - p) * call_matrix[i + 1, j])
                call_matrix[i, j] = np.maximum(call_strike, call_nostrike)
        return call_matrix[0, 0]

    Value1 = American_call(S, K, sigma, r, T, N)
    Value2 = American_call(S, K, sigma, r + 0.0001, T, N)
    rho = (Value2 - Value1) / 0.0001
    return rho


# 6. 定义美式看跌期权Rho计算函数（N步二叉树）
def rho_AmerPut(S, K, sigma, r, T, N):
    def American_put(S, K, sigma, r, T, N):
        t = T / N
        u = np.exp(sigma * np.sqrt(t))
        d = 1 / u
        p = (np.exp(r * t) - d) / (u - d)
        put_matrix = np.zeros((N + 1, N + 1))
        N_list = np.arange(0, N + 1)
        S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
        put_matrix[:, -1] = np.maximum(K - S_end, 0)

        i_list = list(range(0, N))
        i_list.reverse()
        for i in i_list:
            j_list = np.arange(i + 1)
            for j in j_list:
                Si = S * np.power(u, i - j) * np.power(d, j)
                put_strike = np.maximum(K - Si, 0)
                put_nostrike = np.exp(-r * t) * (p * put_matrix[i + 1, j + 1] + (1 - p) * put_matrix[i + 1, j])
                put_matrix[i, j] = np.maximum(put_strike, put_nostrike)
        return put_matrix[0, 0]

    Value1 = American_put(S, K, sigma, r, T, N)
    Value2 = American_put(S, K, sigma, r + 0.0001, T, N)
    rho = (Value2 - Value1) / 0.0001
    return rho

#
# # 7. 农业银行期权Rho计算（美式）
# step = 100
# rho_AmerOpt1 = rho_AmerCall(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, N=step)
# rho_AmerOpt2 = rho_AmerPut(S=S_ABC, K=K_ABC, sigma=sigma_ABC, r=shibor_6M, T=T_ABC, N=step)
#
# print('农业银行A股美式看涨期权的Rho', round(rho_AmerOpt1, 4))
# print('农业银行A股美式看跌期权的Rho', round(rho_AmerOpt2, 4))


'''implied volatility'''
# 1. 牛顿迭代法计算欧式看涨期权隐含波动率
def impvol_call_Newton(C, S, K, r, T):
    def call_BSM(S, K, sigma, r, T):
        d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        call = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        return call

    sigma0 = 0.2
    diff = C - call_BSM(S, K, sigma0, r, T)
    i = 0.0001
    while abs(diff) > 0.0001:
        diff = C - call_BSM(S, K, sigma0, r, T)
        if diff > 0:
            sigma0 += i
        else:
            sigma0 -= i
    return sigma0


# 2. 牛顿迭代法计算欧式看跌期权隐含波动率
def impvol_put_Newton(P, S, K, r, T):
    def put_BSM(S, K, sigma, r, T):
        d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        put = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put

    sigma0 = 0.2
    diff = P - put_BSM(S, K, sigma0, r, T)
    i = 0.0001
    while abs(diff) > 0.0001:
        diff = P - put_BSM(S, K, sigma0, r, T)
        if diff > 0:
            sigma0 += i
        else:
            sigma0 -= i
    return sigma0


# 3. 二分查找法计算欧式看涨期权隐含波动率
def impvol_call_Binary(C, S, K, r, T):
    def call_BSM(S, K, sigma, r, T):
        d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        call = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        return call

    sigma_min = 0.001
    sigma_max = 1.000
    sigma_mid = (sigma_min + sigma_max) / 2
    call_min = call_BSM(S, K, sigma_min, r, T)
    call_max = call_BSM(S, K, sigma_max, r, T)
    call_mid = call_BSM(S, K, sigma_mid, r, T)
    diff = C - call_mid

    if C < call_min or C > call_max:
        print('Error')
    while abs(diff) > 1e-6:
        diff = C - call_BSM(S, K, sigma_mid, r, T)
        sigma_mid = (sigma_min + sigma_max) / 2
        call_mid = call_BSM(S, K, sigma_mid, r, T)
        if C > call_mid:
            sigma_min = sigma_mid
        else:
            sigma_max = sigma_mid
    return sigma_mid


# 4. 二分查找法计算欧式看跌期权隐含波动率
def impvol_put_Binary(P, S, K, r, T):
    def put_BSM(S, K, sigma, r, T):
        d1 = (log(S / K) + (r + power(sigma, 2) / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        put = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put

    sigma_min = 0.001
    sigma_max = 1.000
    sigma_mid = (sigma_min + sigma_max) / 2
    put_min = put_BSM(S, K, sigma_min, r, T)
    put_max = put_BSM(S, K, sigma_max, r, T)
    put_mid = put_BSM(S, K, sigma_mid, r, T)
    diff = P - put_mid

    if P < put_min or P > put_max:
        print('Error')
    while abs(diff) > 1e-6:
        diff = P - put_BSM(S, K, sigma_mid, r, T)
        sigma_mid = (sigma_min + sigma_max) / 2
        put_mid = put_BSM(S, K, sigma_mid, r, T)
        if P > put_mid:
            sigma_min = sigma_mid
        else:
            sigma_max = sigma_mid
    return sigma_mid


# # 5. 50ETF期权隐含波动率计算（牛顿迭代法）
# T0 = dt.datetime(2020, 9, 1)
# T1 = dt.datetime(2021, 3, 24)
# tenor = (T1 - T0).days / 365
#
# price_call = 0.2826
# price_put = 0.1975
# price_50ETF = 3.406
# shibor_6M = 0.02847
# K_50ETF = 3.3
#
# sigma_call1 = impvol_call_Newton(C=price_call, S=price_50ETF, K=K_50ETF, r=shibor_6M, T=tenor)
# print('50ETF购3月3300期权合约的隐含波动率（牛顿迭代法）', round(sigma_call1, 4))
#
# sigma_put = impvol_put_Newton(P=price_put, S=price_50ETF, K=K_50ETF, r=shibor_6M, T=tenor)
# print('50ETF沽3月3300期权合约的隐含波动率（牛顿迭代法）', round(sigma_put, 4))
#
# # 6. 50ETF期权隐含波动率计算（二分查找法）
# sigma_call2 = impvol_call_Binary(C=price_call, S=price_50ETF, K=K_50ETF, r=shibor_6M, T=tenor)
# print('50ETF购3月3300期权合约的隐含波动率（二分查找法）', round(sigma_call2, 4))
#
# sigma_put2 = impvol_put_Binary(P=price_put, S=price_50ETF, K=K_50ETF, r=shibor_6M, T=tenor)
# print('50ETF沽3月3300期权合约的隐含波动率（二分查找法）', round(sigma_put2, 4))
#
# # 7. 上证50ETF认沽期权隐含波动率曲面（行权价格维度）
# S_Dec31 = 3.635
# R_Dec31 = 0.02838
# T2 = dt.datetime(2020, 12, 31)
# T3 = dt.datetime(2021, 6, 23)
# tenor1 = (T3 - T2).days / 365
#
# Put_list = np.array([0.0202, 0.0306, 0.0458, 0.0671, 0.0951, 0.1300, 0.1738, 0.2253, 0.2845, 0.3540, 0.4236])
# K_list1 = np.array([3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000, 3.7000, 3.8000, 3.9000, 4.0000])
# n1 = len(K_list1)
# sigma_list1 = np.zeros_like(Put_list)
#
# for i in np.arange(n1):
#     sigma_list1[i] = impvol_put_Newton(P=Put_list[i], S=S_Dec31, K=K_list1[i], r=R_Dec31, T=tenor1)
#
# plt.figure(figsize=(9, 6))
# plt.plot(K_list1, sigma_list1, 'b-', lw=2.5)
# plt.xlabel(u'期权的行权价格', fontsize=13)
# plt.ylabel('隐含波动率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'期权的行权价格与上证50ETF认沽期权隐含波动率', fontsize=13)
# plt.grid()
# plt.show()
#
# # 8. 沪深300ETF认购期权隐含波动率曲面（行权价格维度）
# S_Sep30 = 4.5848
# R_Sep30 = 0.02691
# T4 = dt.datetime(2020, 9, 30)
# T5 = dt.datetime(2021, 3, 24)
# tenor2 = (T5 - T4).days / 365
#
# Call_list = np.array([0.4660, 0.4068, 0.3529, 0.3056, 0.2657, 0.2267, 0.1977, 0.1707, 0.1477, 0.1019])
# K_list2 = np.array([4.2000, 4.3000, 4.4000, 4.5000, 4.6000, 4.7000, 4.8000, 4.9000, 5.0000, 5.2500])
# n2 = len(K_list2)
# sigma_list2 = np.zeros_like(Call_list)
#
# for i in np.arange(n2):
#     sigma_list2[i] = impvol_call_Binary(C=Call_list[i], S=S_Sep30, K=K_list2[i], r=R_Sep30, T=tenor2)
#
# plt.figure(figsize=(9, 6))
# plt.plot(K_list2, sigma_list2, 'r-', lw=2.5)
# plt.xlabel(u'期权的行权价格', fontsize=13)
# plt.ylabel('隐含波动率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'期权的行权价格与沪深300ETF认购期权隐含波动率', fontsize=13)
# plt.grid()
# plt.show()