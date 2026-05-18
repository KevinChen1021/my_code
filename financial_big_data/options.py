import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from pandas.plotting import register_matplotlib_converters
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
register_matplotlib_converters()


'''期权市场概览'''

# # 1. 导入并可视化300ETF购12月3500合约价格数据
# option_300ETF = pd.read_excel(
#     r'300ETF购12月3500合约每日价格数据.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# # 可视化
# option_300ETF.plot(figsize=(9,6), title=u'300ETF购12月3500合约的日交易价格走势图',
#                    grid=True, fontsize=13)
# plt.ylabel(u'金额', fontsize=11)
# plt.show()
#
#
# # 2. 导入并可视化沪深300股指沽12月4000合约价格数据
# option_HS300 = pd.read_excel(
#     r'沪深300股指沽12月4000合约每日价格数据.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# # 可视化
# option_HS300.plot(figsize=(9,6), title=u'沪深300股指沽12月4000合约的日交易价格走势图',
#                   grid=True, fontsize=12)
# plt.ylabel(u'金额', fontsize=11)
# plt.show()


'''期权类型与到期盈亏'''
# import numpy as np
# import matplotlib.pyplot as plt
# from pylab import mpl
#
# # 配置中文显示
# mpl.rcParams['font.sans-serif'] = ['FangSong']
# mpl.rcParams['axes.unicode_minus'] = False
#
#
# # 1. 看涨期权到期盈亏可视化
# # 参数设置
# S = np.linspace(4, 7, 200)  # 工商银行A股价格序列
# K_call = 5.3                # 看涨期权行权价格
# C = 0.1                     # 看涨期权费
# N = 10000                   # 每份期权对应资产数量
#
# # 计算盈亏
# profit1_call = N * np.maximum(S - K_call, 0)          # 不考虑期权费的多头收益
# profit2_call = N * np.maximum(S - K_call - C, -C)     # 考虑期权费的多头收益
#
# # 绘图
# plt.figure(figsize=(9,6))
# # 子图1：看涨期权多头盈亏
# plt.subplot(1,2,1)
# plt.plot(S, profit1_call, 'b-', label=u'不考虑期权费的期权多头收益', lw=2.5)
# plt.plot(S, profit2_call, 'b--', label=u'考虑期权费的期权多头收益', lw=2.5)
# plt.xlabel(u'工商银行A股价格', fontsize=13)
# plt.ylabel(u'期权盈亏', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'看涨期权到期日多头的盈亏', fontsize=13)
# plt.legend(fontsize=12)
# plt.grid()
#
# # 子图2：看涨期权空头盈亏
# plt.subplot(1,2,2)
# plt.plot(S, -profit1_call, 'r-', label=u'不考虑期权费的期权空头收益', lw=2.5)
# plt.plot(S, -profit2_call, 'r--', label=u'考虑期权费的期权空头收益', lw=2.5)
# plt.xlabel(u'工商银行A股价格', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'看涨期权到期日空头的盈亏', fontsize=13)
# plt.legend(fontsize=12)
# plt.grid()
# plt.show()
#
#
# # 2. 看跌期权到期盈亏可视化
# # 参数设置
# K_put = 5.1                 # 看跌期权行权价格
# P = 0.2                     # 看跌期权费
#
# # 计算盈亏
# profit1_put = N * np.maximum(K_put - S, 0)            # 不考虑期权费的多头收益
# profit2_put = N * np.maximum(K_put - S - P, -P)       # 考虑期权费的多头收益
#
# # 绘图
# plt.figure(figsize=(9,6))
# # 子图1：看跌期权多头盈亏
# plt.subplot(1,2,1)
# plt.plot(S, profit1_put, 'b-', label=u'不考虑期权费的期权多头收益', lw=2.5)
# plt.plot(S, profit2_put, 'b--', label=u'考虑期权费的期权多头收益', lw=2.5)
# plt.xlabel(u'工商银行A股价格', fontsize=13)
# plt.ylabel(u'期权盈亏', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'看跌期权到期日多头的盈亏', fontsize=13)
# plt.legend(fontsize=12)
# plt.grid()
#
# # 子图2：看跌期权空头盈亏
# plt.subplot(1,2,2)
# plt.plot(S, -profit1_put, 'r-', label=u'不考虑期权费的期权空头收益', lw=2.5)
# plt.plot(S, -profit2_put, 'r--', label=u'考虑期权费的期权空头收益', lw=2.5)
# plt.xlabel(u'工商银行A股价格', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'看跌期权到期日空头的盈亏', fontsize=13)
# plt.legend(fontsize=12)
# plt.grid()
# plt.show()


'''期权平价公式'''

# 3. 定义期权平价公式计算函数
def option_parity(opt, c, p, S, K, r, T):
    '''通过看跌-看涨平价关系式计算欧式看涨、看跌期权价格
    opt: 期权类型（'call'=看涨，其他=看跌）
    c: 看涨期权价格（计算看涨时输入'Na'）
    p: 看跌期权价格（计算看跌时输入'Na'）
    S: 基础资产价格
    K: 行权价格
    r: 连续复利无风险收益率
    T: 期权期限（年）'''
    from numpy import exp
    if opt == 'call':
        value = p + S - K * exp(-r * T)  # 计算看涨期权价格
    else:
        value = c + K * exp(-r * T) - S  # 计算看跌期权价格
    return value
#
#
# # 4. 运用期权平价公式计算期权价格
# # 参数设置
# price_call = 0.15    # 看涨期权报价
# price_put = 0.3      # 看跌期权报价
# S_ICBC = 5.0         # 工商银行A股价格
# K_ICBC = 5.2         # 期权行权价格
# shibor = 0.02601     # 3个月期Shibor
# tenor = 3/12         # 期权期限（年）
#
# # 计算期权价格
# value_call = option_parity(opt='call', c='Na', p=price_put, S=S_ICBC, K=K_ICBC, r=shibor, T=tenor)
# value_put = option_parity(opt='put', c=price_call, p='Na', S=S_ICBC, K=K_ICBC, r=shibor, T=tenor)
#
# # 输出结果
# print('运用看跌-看涨平价关系式得出欧式看涨期权价格', round(value_call, 4))
# print('运用看跌-看涨平价关系式得出欧式看跌期权价格', round(value_put, 4))


'''欧式期权定价——BSM模型'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
from scipy.stats import norm

# 配置中文显示
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


# 1. 定义布莱克-斯科尔斯-默顿（BSM）期权定价函数
def option_BSM(S, K, sigma, r, T, opt):
    '''运用布莱克-斯科尔斯-默顿模型计算欧式期权价格
    S: 期权基础资产价格
    K: 期权行权价格
    sigma: 基础资产收益率的波动率（年化）
    r: 连续复利的无风险收益率
    T: 期权期限（年）
    opt: 期权类型（'call'=看涨期权，其他=看跌期权）'''
    from numpy import log, exp, sqrt
    d1 = (log(S/K) + (r + pow(sigma, 2)/2) * T) / (sigma * sqrt(T))  # 计算参数d1
    d2 = d1 - sigma * sqrt(T)  # 计算参数d2
    if opt == 'call':
        value = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)  # 欧式看涨期权价格
    else:
        value = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)  # 欧式看跌期权价格
    return value


# # 2. 计算工商银行A股对应的期权价格（BSM模型）
# # 参数设置
# S_ICBC = 5.0         # 工商银行A股价格
# K_ICBC = 5.2         # 期权行权价格
# sigma_ICBC = 0.205   # 年化波动率
# shibor = 0.02601     # 3个月期Shibor（无风险收益率）
# tenor = 3/12         # 期权期限（年）
#
# # 计算看涨、看跌期权价格
# call_BSM = option_BSM(S=S_ICBC, K=K_ICBC, sigma=sigma_ICBC, r=shibor, T=tenor, opt='call')
# put_BSM = option_BSM(S=S_ICBC, K=K_ICBC, sigma=sigma_ICBC, r=shibor, T=tenor, opt='put')
#
# # 输出结果
# print('运用布莱克-斯科尔斯-默顿模型得到欧式看涨期权价格', round(call_BSM, 4))
# print('运用布莱克-斯科尔斯-默顿模型得到欧式看跌期权价格', round(put_BSM, 4))
#
#
# # 3. 基础资产价格与期权价格的关系可视化
# S_list = np.linspace(4.0, 6.0, 100)  # 工商银行A股价格序列
# call_list1 = option_BSM(S=S_list, K=K_ICBC, sigma=sigma_ICBC, r=shibor, T=tenor, opt='call')
# put_list1 = option_BSM(S=S_list, K=K_ICBC, sigma=sigma_ICBC, r=shibor, T=tenor, opt='put')
#
# plt.figure(figsize=(9,6))
# plt.plot(S_list, call_list1, 'b-', label=u'欧式看涨期权', lw=2.5)
# plt.plot(S_list, put_list1, 'r-', label=u'欧式看跌期权', lw=2.5)
# plt.xlabel(u'工商银行A股股价', fontsize=13)
# plt.ylabel(u'期权价格', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'工商银行A股股价（基础资产价格）与期权价格的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 4. 行权价格与期权价格的关系可视化
# K_list = np.linspace(4.2, 6.2, 100)  # 行权价格序列
# call_list2 = option_BSM(S=S_ICBC, K=K_list, sigma=sigma_ICBC, r=shibor, T=tenor, opt='call')
# put_list2 = option_BSM(S=S_ICBC, K=K_list, sigma=sigma_ICBC, r=shibor, T=tenor, opt='put')
#
# plt.figure(figsize=(9,6))
# plt.plot(K_list, call_list2, 'b-', label=u'欧式看涨期权', lw=2.5)
# plt.plot(K_list, put_list2, 'r-', label=u'欧式看跌期权', lw=2.5)
# plt.xlabel(u'行权价格', fontsize=13)
# plt.ylabel(u'期权价格', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'行权价格与期权价格的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 5. 波动率与期权价格的关系可视化
# sigma_list = np.linspace(0.01, 0.3, 100)  # 波动率序列
# call_list3 = option_BSM(S=S_ICBC, K=K_ICBC, sigma=sigma_list, r=shibor, T=tenor, opt='call')
# put_list3 = option_BSM(S=S_ICBC, K=K_ICBC, sigma=sigma_list, r=shibor, T=tenor, opt='put')
#
# plt.figure(figsize=(9,6))
# plt.plot(sigma_list, call_list3, 'b-', label=u'欧式看涨期权', lw=2.5)
# plt.plot(sigma_list, put_list3, 'r-', label=u'欧式看跌期权', lw=2.5)
# plt.xlabel(u'波动率', fontsize=13)
# plt.ylabel(u'期权价格', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'基础资产收益率的波动率与期权价格的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 6. 无风险收益率与期权价格的关系可视化
# shibor_list = np.linspace(0.01, 0.10, 100)  # 无风险收益率序列
# call_list4 = option_BSM(S=S_ICBC, K=K_ICBC, sigma=sigma_ICBC, r=shibor_list, T=tenor, opt='call')
# put_list4 = option_BSM(S=S_ICBC, K=K_ICBC, sigma=sigma_ICBC, r=shibor_list, T=tenor, opt='put')
#
# plt.figure(figsize=(9,6))
# plt.plot(shibor_list, call_list4, 'b-', label=u'欧式看涨期权', lw=2.5)
# plt.plot(shibor_list, put_list4, 'r-', label=u'欧式看跌期权', lw=2.5)
# plt.xlabel(u'无风险收益率', fontsize=13)
# plt.ylabel(u'期权价格', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'无风险收益率与期权价格的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 7. 期权期限与期权价格的关系可视化
# tenor_list = np.linspace(0.1, 3.0, 100)  # 期权期限序列
# call_list5 = option_BSM(S=S_ICBC, K=K_ICBC, sigma=sigma_ICBC, r=shibor, T=tenor_list, opt='call')
# put_list5 = option_BSM(S=S_ICBC, K=K_ICBC, sigma=sigma_ICBC, r=shibor, T=tenor_list, opt='put')
#
# plt.figure(figsize=(9,6))
# plt.plot(tenor_list, call_list5, 'b-', label=u'欧式看涨期权', lw=2.5)
# plt.plot(tenor_list, put_list5, 'r-', label=u'欧式看跌期权', lw=2.5)
# plt.xlabel(u'期权期限', fontsize=13)
# plt.ylabel(u'期权价格', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'期权期限与期权价格的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 8. 期权价格与行权收益的对比可视化
# S_list2 = np.linspace(4.7, 6, 200)  # 工商银行A股价格序列
# price_call = option_BSM(S=S_list2, K=K_ICBC, sigma=sigma_ICBC, r=shibor, T=tenor, opt='call')
# price_put = option_BSM(S=S_list2, K=K_ICBC, sigma=sigma_ICBC, r=shibor, T=tenor, opt='put')
# profit_call = np.maximum(S_list2 - K_ICBC, 0)  # 看涨期权行权收益（不考虑期权费）
# profit_put = np.maximum(K_ICBC - S_list2, 0)  # 看跌期权行权收益（不考虑期权费）
#
# plt.figure(figsize=(9,7))
# # 子图1：看涨期权价格与行权收益
# plt.subplot(2,1,1)
# plt.plot(S_list2, price_call, 'b-', label=u'欧式看涨期权价格', lw=2.5)
# plt.plot(S_list2, profit_call, 'r-', label=u'欧式看涨期权行权的收益', lw=2.5)
# plt.ylabel(u'看涨期权价格或盈亏', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
#
# # 子图2：看跌期权价格与行权收益
# plt.subplot(2,1,2)
# plt.plot(S_list2, price_put, 'b-', label=u'欧式看跌期权价格', lw=2.5)
# plt.plot(S_list2, profit_put, 'r-', label=u'欧式看跌期权行权的收益', lw=2.5)
# plt.xlabel(u'股票价格', fontsize=13)
# plt.ylabel(u'看跌期权价格或盈亏', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


'''欧式期权定价——二叉树模型'''
'''one step and two step'''
import numpy as np
from numpy import exp, maximum


# 1. 定义一步二叉树期权定价函数
def BTM_1step(S, K, u, d, r, T, types):
    '''运用一步二叉树模型计算欧式期权价值
    S: 基础资产当前价格
    K: 期权行权价格
    u: 基础资产价格上涨比例
    d: 基础资产价格下跌比例
    r: 连续复利无风险收益率
    T: 期权期限（年）
    types: 期权类型（'call'=看涨，其他=看跌）'''
    p = (exp(r * T) - d) / (u - d)  # 基础资产价格上涨概率
    # 期权到期时的价值
    Cu = maximum(S * u - K, 0)
    Cd = maximum(S * d - K, 0)
    # 初始日期的看涨期权价值
    call = (p * Cu + (1 - p) * Cd) * exp(-r * T)
    # 运用看跌-看涨平价关系计算看跌期权价值
    put = call + K * exp(-r * T) - S

    if types == 'call':
        value = call
    else:
        value = put
    return value


# 2. 定义两步二叉树期权定价函数
def BTM_2step(S, K, u, d, r, T, types):
    '''运用两步二叉树模型计算欧式期权价值
    参数定义同一步二叉树模型'''
    t = T / 2  # 每一步的步长期限（年）
    p = (exp(r * t) - d) / (u - d)  # 基础资产价格上涨概率
    # 期权到期时的价值（两步后的三种状态）
    Cuu = maximum(pow(u, 2) * S - K, 0)
    Cud = maximum(S * u * d - K, 0)
    Cdd = maximum(pow(d, 2) * S - K, 0)
    # 初始日期的看涨期权价值
    call = (pow(p, 2) * Cuu + 2 * p * (1 - p) * Cud + pow(1 - p, 2) * Cdd) * exp(-r * T)
    # 运用看跌-看涨平价关系计算看跌期权价值
    put = call + K * exp(-r * T) - S

    if types == 'call':
        value = call
    else:
        value = put
    return value


# # 3. 一步二叉树模型计算期权价值
# # 参数设置
# S_ICBC = 6  # 工商银行A股股价
# K_ICBC = 5.7  # 期权行权价格
# up = 1.1  # 股价上涨比例
# down = 0.9  # 股价下跌比例
# R = 0.024  # 无风险收益率
# tenor = 1.0  # 期权期限（年）
#
# # 计算看涨、看跌期权价值
# value_call = BTM_1step(S=S_ICBC, K=K_ICBC, u=up, d=down, r=R, T=tenor, types='call')
# value_put = BTM_1step(S=S_ICBC, K=K_ICBC, u=up, d=down, r=R, T=tenor, types='put')
# print('2020年1月3日工商银行股票看涨期权价值', round(value_call, 3))
# print('2020年1月3日工商银行股票看跌期权价值', round(value_put, 3))
#
# # 4. 两步二叉树模型计算期权价值
# tenor_new = 2  # 期权期限（年）
# # 计算看涨、看跌期权价值
# value_call_2Y = BTM_2step(S=S_ICBC, K=K_ICBC, u=up, d=down, r=R, T=tenor_new, types='call')
# value_put_2Y = BTM_2step(S=S_ICBC, K=K_ICBC, u=up, d=down, r=R, T=tenor_new, types='put')
# print('2020年1月3日工商银行股票看涨期权价值', round(value_call_2Y, 4))
# print('2020年1月3日工商银行股票看跌期权价值', round(value_put_2Y, 4))


'''n steps'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from math import factorial
from scipy.stats import norm

# 配置中文显示
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


# 1. 定义N步二叉树期权定价函数
def BTM_Nstep(S, K, sigma, r, T, N, types):
    '''运用N步二叉树模型计算欧式期权价值
    S: 基础资产当前价格
    K: 期权行权价格
    sigma: 基础资产年化波动率
    r: 连续复利无风险收益率
    T: 期权期限（年）
    N: 二叉树步数
    types: 期权类型（'call'=看涨，其他=看跌）'''
    from numpy import exp, maximum, sqrt
    t = T / N  # 每一步的步长期限（年）
    u = exp(sigma * sqrt(t))  # 价格上涨比例
    d = 1 / u  # 价格下跌比例
    p = (exp(r * t) - d) / (u - d)  # 风险中性概率
    N_list = range(0, N + 1)
    A = []

    for j in N_list:
        # 计算到期日某节点的期权价值
        C_Nj = maximum(S * pow(u, j) * pow(d, N - j) - K, 0)
        # 计算到达该节点的路径数量
        Num = factorial(N) / (factorial(j) * factorial(N - j))
        A.append(Num * pow(p, j) * pow(1 - p, N - j) * C_Nj)

    # 计算看涨期权价值
    call = exp(-r * T) * sum(A)
    # 运用看跌-看涨平价关系计算看跌期权价值
    put = call + K * exp(-r * T) - S

    if types == 'call':
        value = call
    else:
        value = put
    return value


# 2. 定义BSM期权定价函数（复用）
def option_BSM(S, K, sigma, r, T, opt):
    from numpy import log, exp, sqrt
    d1 = (log(S / K) + (r + pow(sigma, 2) / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    if opt == 'call':
        value = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        value = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return value


# # 3. 工商银行A股期权定价（N步二叉树）
# ## 导入数据并计算波动率
# P_ICBC = pd.read_excel(
#     r'工商银行A股日收盘价(2017-2019年).xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# R_ICBC = np.log(P_ICBC / P_ICBC.shift(1))
# Sigma_ICBC = np.sqrt(252) * np.std(R_ICBC)
# Sigma_ICBC = float(Sigma_ICBC)
# print('工商银行A股年化波动率', round(Sigma_ICBC, 4))
#
# ## 定价参数
# S_ICBC = 6  # 工商银行A股股价
# K_ICBC = 5.7  # 期权行权价格
# R = 0.024  # 无风险收益率
# tenor = 1.0  # 期权期限（年）
#
# ## 不同步数的二叉树定价
# N_month = 12  # 步长=每月
# N_week = 52  # 步长=每周
# N_day = 252  # 步长=每个交易日
#
# Call_value1 = BTM_Nstep(S=S_ICBC, K=K_ICBC, sigma=Sigma_ICBC, r=R, T=tenor, N=N_month, types='call')
# Call_value2 = BTM_Nstep(S=S_ICBC, K=K_ICBC, sigma=Sigma_ICBC, r=R, T=tenor, N=N_week, types='call')
# Call_value3 = BTM_Nstep(S=S_ICBC, K=K_ICBC, sigma=Sigma_ICBC, r=R, T=tenor, N=N_day, types='call')
#
# print('运用12步二叉树模型（步长等于每月）计算2020年1月3日期权价值', round(Call_value1, 4))
# print('运用52步二叉树模型（步长等于每周）计算2020年1月3日期权价值', round(Call_value2, 4))
# print('运用252步二叉树模型（步长等于每个交易日）计算2020年1月3日期权价值', round(Call_value3, 4))
#
# # 4. 建设银行A股期权定价（BSM+N步二叉树）
# ## 导入数据并计算波动率
# Price_CCB = pd.read_excel(
#     r'C:/Desktop/建设银行A股日收盘价(2018年至2020年8月18日).xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# R_CCB = np.log(Price_CCB / Price_CCB.shift(1))
# Sigma_CCB = np.sqrt(252) * np.std(R_CCB)
# Sigma_CCB = float(Sigma_CCB)
# print('建设银行A股年化波动率', round(Sigma_CCB, 4))
#
# ## 定价参数
# S_CCB = 6.32  # 建设银行A股股价
# T_CCB = 1  # 期权期限（年）
# R_Aug18 = 0.0228  # 无风险收益率
# K_CCB = 6.6  # 期权行权价格
#
# ## BSM模型定价
# value_BSM = option_BSM(S=S_CCB, K=K_CCB, sigma=Sigma_CCB, r=R_Aug18, T=T_CCB, opt='call')
# print('运用BSM模型计算得到建设银行股票看涨期权价值', round(value_BSM, 4))
#
# ## 不同步数的二叉树定价
# N1 = 10
# N2 = 50
# N3 = 250
#
# value_BTM_N1 = BTM_Nstep(S=S_CCB, K=K_CCB, sigma=Sigma_CCB, r=R_Aug18, T=T_CCB, N=N1, types='call')
# value_BTM_N2 = BTM_Nstep(S=S_CCB, K=K_CCB, sigma=Sigma_CCB, r=R_Aug18, T=T_CCB, N=N2, types='call')
# value_BTM_N3 = BTM_Nstep(S=S_CCB, K=K_CCB, sigma=Sigma_CCB, r=R_Aug18, T=T_CCB, N=N3, types='call')
#
# print('运用10步二叉树模型计算得出建设银行股票看涨期权价值', round(value_BTM_N1, 4))
# print('运用50步二叉树模型计算得出建设银行股票看涨期权价值', round(value_BTM_N2, 4))
# print('运用250步二叉树模型计算得出建设银行股票看涨期权价值', round(value_BTM_N3, 4))
#
# # 5. 二叉树模型与BSM模型的收敛性可视化
# N_list = range(1, 151)
# value_BTM_list = np.zeros(len(N_list))
# for i in N_list:
#     value_BTM_list[i - 1] = BTM_Nstep(S=S_CCB, K=K_CCB, sigma=Sigma_CCB, r=R_Aug18, T=T_CCB, N=i, types='call')
#
# value_BSM_list = value_BSM * np.ones(len(N_list))
#
# plt.figure(figsize=(9, 6))
# plt.plot(N_list, value_BTM_list, 'b-', label=u'二叉树模型的结果', lw=2.5)
# plt.plot(N_list, value_BSM_list, 'r-', label=u'BSM模型的结果', lw=2.5)
# plt.xlabel(u'步数', fontsize=13)
# plt.ylabel(u'期权价值', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'二叉树模型与BSM模型之间的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


'''美式期权定价——二叉树模型'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from math import factorial

# 配置中文显示
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


# 1. 定义美式看涨期权N步二叉树定价函数
def American_call(S, K, sigma, r, T, N):
    t = T / N  # 步长期限
    u = np.exp(sigma * np.sqrt(t))  # 价格上涨比例
    d = 1 / u  # 价格下跌比例
    p = (np.exp(r * t) - d) / (u - d)  # 风险中性概率
    call_matrix = np.zeros((N + 1, N + 1))  # 存储节点期权价值的矩阵

    # 计算到期日节点的基础资产价格与期权价值
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(S_end - K, 0)

    # 倒推计算非到期日节点的期权价值
    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)  # 当前节点基础资产价格
            call_strike = np.maximum(Si - K, 0)  # 提前行权收益
            # 不提前行权的期权价值（折现）
            call_nostrike = np.exp(-r * t) * (p * call_matrix[i + 1, j + 1] + (1 - p) * call_matrix[i + 1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)  # 取最大值

    call_begin = call_matrix[0, 0]  # 初始期权价值
    return call_begin


# 2. 定义美式看跌期权N步二叉树定价函数
def American_put(S, K, sigma, r, T, N):
    t = T / N  # 步长期限
    u = np.exp(sigma * np.sqrt(t))  # 价格上涨比例
    d = 1 / u  # 价格下跌比例
    p = (np.exp(r * t) - d) / (u - d)  # 风险中性概率
    put_matrix = np.zeros((N + 1, N + 1))  # 存储节点期权价值的矩阵

    # 计算到期日节点的基础资产价格与期权价值
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(K - S_end, 0)

    # 倒推计算非到期日节点的期权价值
    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)  # 当前节点基础资产价格
            put_strike = np.maximum(K - Si, 0)  # 提前行权收益
            # 不提前行权的期权价值（折现）
            put_nostrike = np.exp(-r * t) * (p * put_matrix[i + 1, j + 1] + (1 - p) * put_matrix[i + 1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)  # 取最大值

    put_begin = put_matrix[0, 0]  # 初始期权价值
    return put_begin


# 3. 定义欧式期权N步二叉树定价函数（复用）
def BTM_Nstep(S, K, sigma, r, T, N, types):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    N_list = range(0, N + 1)
    A = []
    for j in N_list:
        C_Nj = np.maximum(S * np.power(u, j) * np.power(d, N - j) - K, 0) if types == 'call' else np.maximum(
            K - S * np.power(u, j) * np.power(d, N - j), 0)
        Num = factorial(N) / (factorial(j) * factorial(N - j))
        A.append(Num * np.power(p, j) * np.power(1 - p, N - j) * C_Nj)
    option_val = np.exp(-r * T) * sum(A)
    return option_val


# # 4. 中国银行A股期权定价（美式看跌）
# ## 导入数据并计算波动率
# Price_BOC = pd.read_excel(
#     r'中国银行A股日收盘价数据(2017年至2020年2月7日).xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# R_BOC = np.log(Price_BOC / Price_BOC.shift(1))
# Sigma_BOC = np.sqrt(252) * np.std(R_BOC)
# Sigma_BOC = float(Sigma_BOC)
# print('中国银行A股年化波动率', round(Sigma_BOC, 4))
#
# ## 定价参数
# S_BOC = 3.5  # 中国银行A股股价
# K_BOC = 3.8  # 期权行权价格
# T_BOC = 1  # 期权期限（年）
# r_Feb10 = 0.02  # 无风险收益率
#
# ## 不同步数的美式看跌期权定价
# N_2 = 2
# N_12 = 12
# N_52 = 52
# N_252 = 252
#
# Put_2step = American_put(S=S_BOC, K=K_BOC, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_2)
# Put_12step = American_put(S=S_BOC, K=K_BOC, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_12)
# Put_52step = American_put(S=S_BOC, K=K_BOC, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_52)
# Put_252step = American_put(S=S_BOC, K=K_BOC, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252)
#
# print('运用2步二叉树模型计算中国银行A股美式看跌期权价值', round(Put_2step, 4))
# print('运用12步二叉树模型计算中国银行A股美式看跌期权价值', round(Put_12step, 4))
# print('运用52步二叉树模型计算中国银行A股美式看跌期权价值', round(Put_52step, 4))
# print('运用252步二叉树模型计算中国银行A股美式看跌期权价值', round(Put_252step, 4))


'''美式期权and欧式期权的关系'''

# # 5. 不同行权价格下的欧/美式期权价值对比
# K1 = 3.0
# K2 = 3.5
# K3 = 4.0
#
# ## 看涨期权
# Euro_call_K1 = BTM_Nstep(S=S_BOC, K=K1, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252, types='call')
# Amer_call_K1 = American_call(S=S_BOC, K=K1, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252)
# Euro_call_K2 = BTM_Nstep(S=S_BOC, K=K2, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252, types='call')
# Amer_call_K2 = American_call(S=S_BOC, K=K2, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252)
# Euro_call_K3 = BTM_Nstep(S=S_BOC, K=K3, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252, types='call')
# Amer_call_K3 = American_call(S=S_BOC, K=K3, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252)
#
# print('行权价格为3元的欧式看涨期权价值', Euro_call_K1)
# print('行权价格为3元的美式看涨期权价值', Amer_call_K1)
# print('行权价格为3.5元的欧式看涨期权价值', Euro_call_K2)
# print('行权价格为3.5元的美式看涨期权价值', Amer_call_K2)
# print('行权价格为4元的欧式看涨期权价值', Euro_call_K3)
# print('行权价格为4元的美式看涨期权价值', Amer_call_K3)
#
# ## 看跌期权
# Euro_put_K1 = BTM_Nstep(S=S_BOC, K=K1, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252, types='put')
# Amer_put_K1 = American_put(S=S_BOC, K=K1, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252)
# Euro_put_K2 = BTM_Nstep(S=S_BOC, K=K2, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252, types='put')
# Amer_put_K2 = American_put(S=S_BOC, K=K2, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252)
# Euro_put_K3 = BTM_Nstep(S=S_BOC, K=K3, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252, types='put')
# Amer_put_K3 = American_put(S=S_BOC, K=K3, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252)
#
# print('行权价格为3元的欧式看跌期权价值', Euro_put_K1)
# print('行权价格为3元的美式看跌期权价值', Amer_put_K1)
# print('行权价格为3.5元的欧式看跌期权价值', Euro_put_K2)
# print('行权价格为3.5元的美式看跌期权价值', Amer_put_K2)
# print('行权价格为4元的欧式看跌期权价值', Euro_put_K3)
# print('行权价格为4元的美式看跌期权价值', Amer_put_K3)
#
# # 6. 欧/美式看跌期权价值与股价的关系可视化
# S_BOC_list = np.linspace(1.0, 5.0, 200)
# Euro_put_list = np.zeros_like(S_BOC_list)
# Amer_put_list = np.zeros_like(S_BOC_list)
#
# for i in range(len(S_BOC_list)):
#     Euro_put_list[i] = BTM_Nstep(S=S_BOC_list[i], K=K1, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252, types='put')
#     Amer_put_list[i] = American_put(S=S_BOC_list[i], K=K1, sigma=Sigma_BOC, r=r_Feb10, T=T_BOC, N=N_252)
#
# plt.figure(figsize=(9, 6))
# plt.plot(S_BOC_list, Amer_put_list, 'r-', label=u'美式看跌期权', lw=2.5)
# plt.plot(S_BOC_list, Euro_put_list, 'b-', label=u'欧式看跌期权', lw=2.5)
# plt.xlabel(u'中国银行A股股价', fontsize=13)
# plt.ylabel(u'期权价值', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'欧式看跌期权与美式看跌期权的价值关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
# # 7. 美式看跌期权价值与内在价值的关系可视化
# Intrinsic_value = np.maximum(K1 - S_BOC_list, 0)
# plt.figure(figsize=(9, 6))
# plt.plot(S_BOC_list, Amer_put_list, 'r-', label=u'美式看跌期权价值', lw=2.5)
# plt.plot(S_BOC_list, Intrinsic_value, 'g--', label=u'期权内在价值', lw=2.0)
# plt.xlabel(u'中国银行A股股价', fontsize=13)
# plt.ylabel(u'期权价值', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'美式看跌期权价值与期权内在价值的关系图', fontsize=13)
# plt.legend(fontsize=13, loc=9)
# plt.grid()
# plt.show()
#
# # 8. 欧式看跌期权价值与内在价值的关系可视化
# plt.figure(figsize=(9, 6))
# plt.plot(S_BOC_list, Euro_put_list, 'b-', label=u'欧式看跌期权价值', lw=2.5)
# plt.plot(S_BOC_list, Intrinsic_value, 'g--', label=u'期权内在价值', lw=2.5)
# plt.xlabel(u'中国银行A股股价', fontsize=13)
# plt.ylabel(u'期权价值', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'欧式看跌期权与期权内在价值的关系图', fontsize=13)
# plt.legend(fontsize=13, loc=9)
# plt.grid()
# plt.show()