import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


'''利息测算'''
# # 1. 不同复利频次下的存款本息和计算
# principle = 1e7  # 存款本金
# r_A = 0.055      # A银行定期存款利率
# T = 3            # 存款期限（年）
#
# # 计算不同复利频次的本息和
# FV_annual = principle * np.power(1 + r_A, T)               # 每年复利1次
# FV_semiannual = principle * np.power(1 + r_A/2, T*2)       # 每半年复利1次
# FV_quarter = principle * np.power(1 + r_A/4, T*4)         # 每季度复利1次
# FV_month = principle * np.power(1 + r_A/12, T*12)         # 每月复利1次
# FV_week = principle * np.power(1 + r_A/52, T*52)          # 每周复利1次
# FV_day = principle * np.power(1 + r_A/365, T*365)         # 每天复利1次
# FV_continuous = principle * np.exp(r_A * T)               # 连续复利
#
# # 输出结果
# print('利率每年复利1次的到期存款本息和', round(FV_annual, 2))
# print('利率每半年复利1次的到期存款本息和', round(FV_semiannual, 2))
# print('利率每季度复利1次的到期存款本息和', round(FV_quarter, 2))
# print('利率每月复利1次的到期存款本息和', round(FV_month, 2))
# print('利率每周复利1次的到期存款本息和', round(FV_week, 2))
# print('利率每天复利1次的到期存款本息和', round(FV_day, 2))
# print('利率连续复利的到期存款本息和', round(FV_continuous, 2))
#
#
# # 2. 不同银行存款利率的等价连续复利计算
# r_B = 0.0555  # B银行存款利率
# m_B = 2       # B银行复利频次
# # B银行等价连续复利
# r_B_conti = m_B * np.log(1 + r_B / m_B)
# print('B银行存款利率对应的等价连续复利利率', round(r_B_conti, 6))
#
# m_A = 52      # A银行每周复利频次
# # A银行等价连续复利
# r_A_conti = m_A * np.log(1 + r_A / m_A)
# print('A银行存款利率对应的等价连续复利利率', round(r_A_conti, 6))
#
# # 比较B银行与A银行的等价连续复利
# print('B银行对应的等价连续复利利率是否高于A银行的利率:', r_B_conti > r_A_conti)
#
#
# # 3. 连续复利与按季度复利的等价转换
# r_C_conti = 0.0548  # C银行连续复利利率
# m_A_new = 4         # 按季度复利的频次
# # 计算C银行连续复利对应的按季度复利利率
# r_C = m_A_new * (np.exp(r_C_conti / m_A_new) - 1)
# print('C银行连续复利利率对应等价的按季度复利1次的利率', round(r_C, 6))
#
# # 比较C银行等价利率与A银行利率
# print('C银行对应的等价按季度复利的利率是否高于A银行的利率:', r_C > r_A)
# print('C银行对应的等价按季度复利的利率是否低于A银行的利率:', r_C < r_A)


'''远期利率测算'''
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from pylab import mpl
#
# # 配置中文显示
# mpl.rcParams['font.sans-serif'] = ['FangSong']
# mpl.rcParams['axes.unicode_minus'] = False
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
#
#
# # 1. 导入日本国债利率数据
# spot = pd.read_excel(
#     r'日本国债利率数据.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )


# 2. 定义远期利率计算函数
def Forward_rate(R1, R2, T1, T2):
    '''定义计算远期利率的函数
    R1: 表示期限为T1的即期利率
    R2: 表示期限为T2的即期利率
    T1: 表示零息利率R1的期限长度
    T2: 表示零息利率R2的期限长度'''
    forward = R2 + (R2 - R1) * T1 / (T2 - T1)  # 计算远期利率的表达式
    return forward
#
#
# # 3. 计算各时间点的即期利率与远期利率
# T_list = np.arange(1, 11)  # 1到10年的期限数组
#
# # 2020年9月末
# spot_3Q2020 = np.array(spot.loc['2020-09-30'])
# forward_3Q2020 = Forward_rate(
#     R1=spot_3Q2020[:-1], R2=spot_3Q2020[1:],
#     T1=T_list[:-1], T2=T_list[1:]
# )
# forward_3Q2020 = np.append(spot_3Q2020[0], forward_3Q2020)  # 拼接第1年即期利率
#
# # 2020年12月末
# spot_4Q2020 = np.array(spot.loc['2020-12-30'])
# forward_4Q2020 = Forward_rate(
#     R1=spot_4Q2020[:-1], R2=spot_4Q2020[1:],
#     T1=T_list[:-1], T2=T_list[1:]
# )
# forward_4Q2020 = np.append(spot_4Q2020[0], forward_4Q2020)
#
# # 2021年3月末
# spot_1Q2021 = np.array(spot.loc['2021-03-31'])
# forward_1Q2021 = Forward_rate(
#     R1=spot_1Q2021[:-1], R2=spot_1Q2021[1:],
#     T1=T_list[:-1], T2=T_list[1:]
# )
# forward_1Q2021 = np.append(spot_1Q2021[0], forward_1Q2021)
#
# # 2021年6月末
# spot_2Q2021 = np.array(spot.loc['2021-06-30'])
# forward_2Q2021 = Forward_rate(
#     R1=spot_2Q2021[:-1], R2=spot_2Q2021[1:],
#     T1=T_list[:-1], T2=T_list[1:]
# )
# forward_2Q2021 = np.append(spot_2Q2021[0], forward_2Q2021)
#
#
# # 4. 可视化2020年9月末、12月末的即期与远期利率
# plt.figure(figsize=(11,6))
#
# # 子图1：2020年9月末
# plt.subplot(1,2,1)
# plt.plot(T_list, spot_3Q2020, 'r-', label=u'即期利率曲线', lw=2.5)
# plt.plot(T_list, spot_3Q2020, 'bo', label=u'即期利率')
# plt.plot(T_list, forward_3Q2020, 'c-', label=u'远期利率曲线', lw=2.5)
# plt.plot(T_list, forward_3Q2020, 'mo', label=u'远期利率')
# plt.xticks(fontsize=13)
# plt.xlabel(u'期限（年）', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'利率', fontsize=13)
# plt.title(u'2020年9月末日本国债即期与远期利率', fontsize=14)
# plt.legend(fontsize=13, loc=2)
# plt.grid()
#
# # 子图2：2020年12月末（共享y轴）
# plt.subplot(1,2,2, sharey=plt.gca())
# plt.plot(T_list, spot_4Q2020, 'r-', label=u'即期利率曲线', lw=2.5)
# plt.plot(T_list, spot_4Q2020, 'bo', label=u'即期利率')
# plt.plot(T_list, forward_4Q2020, 'c-', label=u'远期利率曲线', lw=2.5)
# plt.plot(T_list, forward_4Q2020, 'mo', label=u'远期利率')
# plt.xticks(fontsize=13)
# plt.xlabel(u'期限（年）', fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'2020年12月末日本国债即期与远期利率', fontsize=14)
# plt.legend(fontsize=13, loc=2)
# plt.grid()
#
# plt.show()
#
#
# # 5. 可视化2021年3月末、6月末的即期与远期利率
# plt.figure(figsize=(11,6))
#
# # 子图1：2021年3月末
# plt.subplot(1,2,1)
# plt.plot(T_list, spot_1Q2021, 'r-', label=u'即期利率曲线', lw=2.5)
# plt.plot(T_list, spot_1Q2021, 'bo', label=u'即期利率')
# plt.plot(T_list, forward_1Q2021, 'c-', label=u'远期利率曲线', lw=2.5)
# plt.plot(T_list, forward_1Q2021, 'mo', label=u'远期利率')
# plt.xticks(fontsize=13)
# plt.xlabel(u'期限（年）', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'利率', fontsize=13)
# plt.title(u'2021年3月末即期与远期利率', fontsize=14)
# plt.legend(fontsize=13, loc=2)
# plt.grid()
#
# # 子图2：2021年6月末（共享y轴）
# plt.subplot(1,2,2, sharey=plt.gca())
# plt.plot(T_list, spot_2Q2021, 'r-', label=u'即期利率曲线', lw=2.5)
# plt.plot(T_list, spot_2Q2021, 'bo', label=u'即期利率')
# plt.plot(T_list, forward_2Q2021, 'c-', label=u'远期利率曲线', lw=2.5)
# plt.plot(T_list, forward_2Q2021, 'mo', label=u'远期利率')
# plt.xticks(fontsize=13)
# plt.xlabel(u'期限（年）', fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'2021年6月末即期与远期利率', fontsize=14)
# plt.legend(fontsize=13, loc=2)
# plt.grid()
#
# plt.show()


'''FRA现金流'''
# import numpy as np
# import matplotlib.pyplot as plt
# import datetime as dt
#
# 1. 定义远期利率协议（FRA）现金流计算函数
def FRA_cashflow(L, Rk, Rm, T1, T2, position):
    '''构建计算远期利率协议在参考利率确定日发生现金流的函数
    L: 表示远期利率协议的本金
    Rk: 表示远期利率协议的固定利率
    Rm: 表示在参考利率确定日（T1时点）观察到的[T1,T2]的参考利率
    T1: 表示参考利率确定日，以时间对象格式输入
    T2: 表示远期利率协议到期日，以时间对象格式输入，并且T2大于T1
    position: 表示头寸方向，position='long'表示多头，其他则表示空头'''
    tenor = (T2 - T1).days / 365  # 测算期限（年）
    cashflow_long = (Rm - Rk) * tenor * L / (1 + tenor * Rm)  # 计算多头的现金流
    if position == 'long':
        cashflow = cashflow_long  # 针对多头
    else:
        cashflow = -cashflow_long  # 针对空头
    return cashflow
#
#
# # 2. 输入FRA参数并计算现金流
# # 时间参数
# t0 = dt.datetime(2021, 7, 1)  # 现金流计算日
# t1 = dt.datetime(2021, 9, 30) # 第1份FRA到期日
# t2 = dt.datetime(2021, 12, 31)# 第2份FRA到期日
#
# # 本金与利率参数
# L1 = 5.6e7    # 第1份FRA本金
# L2 = 8.3e7    # 第2份FRA本金
# R1_fixed = -0.0045  # 第1份FRA固定利率
# R2_fixed = -0.0036  # 第2份FRA固定利率
# Euribor_3M = -0.0054  # 3个月期Euribor
# Euribor_6M = -0.005130 # 6个月期Euribor
#
# # 计算单份FRA现金流
# CF1_short = FRA_cashflow(L=L1, Rk=R1_fixed, Rm=Euribor_3M, T1=t0, T2=t1, position='short')
# CF1_long = FRA_cashflow(L=L1, Rk=R1_fixed, Rm=Euribor_3M, T1=t0, T2=t1, position='long')
# CF2_short = FRA_cashflow(L=L2, Rk=R2_fixed, Rm=Euribor_6M, T1=t0, T2=t2, position='short')
# CF2_long = FRA_cashflow(L=L2, Rk=R2_fixed, Rm=Euribor_6M, T1=t0, T2=t2, position='long')
#
# # 输出单份FRA现金流
# print('2021年7月1日第1份远期利率协议空头（E银行）现金流', round(CF1_short, 2))
# print('2021年7月1日第1份远期利率协议多头（F公司）现金流', round(CF1_long, 2))
# print('2021年7月1日第2份远期利率协议空头（E银行）现金流', round(CF2_short, 2))
# print('2021年7月1日第2份远期利率协议多头（F公司）现金流', round(CF2_long, 2))
#
# # 计算两份FRA现金流总和
# CF_short = CF1_short + CF2_short
# CF_long = CF1_long + CF2_long
# print('2021年7月1日两份远期利率协议空头（E银行）现金流之和', round(CF_short, 2))
# print('2021年7月1日两份远期利率协议多头（F公司）现金流之和', round(CF_long, 2))
#
#
# # 3. 模拟参考利率对FRA现金流的影响
# Euribor_list = np.linspace(-0.01, 0.002, 200)  # 参考利率模拟数组
#
# # 计算多组现金流
# CF1_short_list = FRA_cashflow(L=L1, Rk=R1_fixed, Rm=Euribor_list, T1=t0, T2=t1, position='short')
# CF1_long_list = FRA_cashflow(L=L1, Rk=R1_fixed, Rm=Euribor_list, T1=t0, T2=t1, position='long')
# CF2_short_list = FRA_cashflow(L=L2, Rk=R2_fixed, Rm=Euribor_list, T1=t0, T2=t2, position='short')
# CF2_long_list = FRA_cashflow(L=L2, Rk=R2_fixed, Rm=Euribor_list, T1=t0, T2=t2, position='long')
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(Euribor_list, CF1_short_list, 'b--', label=u'第1份协议空头', lw=2.5)
# plt.plot(Euribor_list, CF1_long_list, 'r--', label=u'第1份协议多头', lw=2.5)
# plt.plot(Euribor_list, CF2_short_list, 'm--', label=u'第2份协议空头', lw=2.5)
# plt.plot(Euribor_list, CF2_long_list, 'c--', label=u'第2份协议多头', lw=2.5)
# plt.plot(Euribor_list, CF1_short_list+CF2_short_list, 'g-', label=u'合计两份协议空头', lw=2.5)
# plt.plot(Euribor_list, CF1_long_list+CF2_long_list, 'y-', label=u'合计两份协议多头', lw=2.5)
#
# plt.xticks(fontsize=13)
# plt.xlabel(u'参考利率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'现金流', fontsize=13)
# plt.title(u'参考利率的不同取值对远期利率协议现金流的影响', fontsize=13)
# plt.legend(fontsize=13, loc=9)
# plt.grid()
# plt.show()


'''FRA定价'''
import numpy as np
import scipy.interpolate as sci
import datetime as dt

# （需提前定义Forward_rate函数）
def Forward_rate(R1, R2, T1, T2):
    forward = R2 + (R2 - R1) * T1 / (T2 - T1)
    return forward

# 1. 定义远期利率协议（FRA）价值计算函数
def Value_FRA(L, Rk, Rf, R, T0, T1, T2, position):
    '''定义一个计算远期利率协议价值的函数
    L: 表示远期利率协议的本金
    Rk: 表示远期利率协议中的固定利率
    Rf: 表示当前观察到的未来[T1,T2]期间的远期参考利率
    R: 表示期限长度为T2-T0的无风险利率（连续复利）
    T0: 表示合约的估值日，用时间对象格式输入
    T1: 表示参考利率确定日（T1），格式与T0一致
    T2: 表示合约到期日（T2），格式与T0一致，并且T2大于T1
    position: 表示头寸方向，position='long'表示多头，其他表示空头'''
    from numpy import exp
    tenor1 = (T2 - T1).days / 365  # 远期参考利率的期限（年）
    tenor2 = (T2 - T0).days / 365  # 无风险利率贴现的期限（年）
    value_long = L * (Rf - Rk) * tenor1 * exp(-R * tenor2)  # 远期利率协议多头的估值
    if position == 'long':
        value = value_long  # 针对多头
    else:
        value = -value_long  # 针对空头
    return value

#
# # 2. 插值法测算Libor远期利率
# # 已有Libor数据与期限
# Libor_list1 = [0.000734, 0.000785, 0.000825, 0.000953, 0.001196, 0.001496, 0.002279]
# tenor_list1 = [1/365, 7/365, 1/12, 2/12, 3/12, 6/12, 1]
#
# # 构建三阶样条插值函数
# f1 = sci.interp1d(x=tenor_list1, y=Libor_list1, kind='cubic')
#
# # 新增期限列表
# tenor_list2 = [1/365, 7/365, 1/12, 2/12, 3/12, 4/12, 6/12, 7/12, 1]
# Libor_list2 = f1(tenor_list2)  # 测算新的Libor数据
#
# # 提取4个月、7个月期Libor
# Libor_4M = Libor_list2[5]
# Libor_7M = Libor_list2[-2]
#
# # 计算3个月期Libor远期利率
# Libor_3M_forward = Forward_rate(R1=Libor_4M, R2=Libor_7M, T1=tenor_list2[5], T2=tenor_list2[-2])
# print('8月31日计算得到12月31日的3个月期Libor远期利率', round(Libor_3M_forward, 6))
#
#
# # 3. 插值法测算美国国债收益率
# # 已有收益率数据与期限
# yield_list1 = [0.0003, 0.0004, 0.0006, 0.0007, 0.0020, 0.0040, 0.0077]
# tenor_list3 = [1/12, 3/12, 6/12, 1, 2, 3, 5]
#
# # 构建三阶样条插值函数
# f2 = sci.interp1d(x=tenor_list3, y=yield_list1, kind='cubic')
#
# # 新增期限列表
# tenor_list4 = [1/12, 3/12, 6/12, 7/12, 1, 2, 3, 5]
# yield_list2 = f2(tenor_list4)  # 测算新的收益率数据
#
# # 提取7个月期美国国债收益率
# yield_7M = yield_list2[3]
#
#
# # 4. 计算FRA价值
# # 时间参数
# t0 = dt.datetime(2021, 8, 31)  # 估值日
# t1 = dt.datetime(2021, 12, 31) # 浮动利率确定日
# t2 = dt.datetime(2022, 3, 31)  # 协议到期日
#
# # FRA参数
# R_fixed = 0.0043  # 固定利率
# par = 6.8e7       # 面值
#
# # 计算FRA多头价值
# Value_long = Value_FRA(
#     L=par, Rk=R_fixed, Rf=Libor_3M_forward, R=yield_7M,
#     T0=t0, T1=t1, T2=t2, position='long'
# )
# print('2021年8月31日远期利率协议多头的价值（美元）', round(Value_long, 2))


'''不同币种的汇兑'''
# 1. 定义货币兑换金额计算函数
def exchange(M, N, Ea, Eb, curr_A, curr_B, direction):
    '''定义一个计算汇兑金额的函数，并且两种货币分别是A货币和B货币
    M: 表示汇兑前的金额，如果计算汇兑后的金额则输入M='Na'
    N: 表示汇兑后的金额，如果计算汇兑前的金额则输入N='Na'
    Ea: 表示银行的汇率卖出价，标价方式是以若干单位A货币表示1单位B货币
    Eb: 表示银行的汇率买入价，标价方式与Ea相同
    curr_A: 表示A货币的名称，比如curr_A='人民币'表示币种是人民币
    curr_B: 表示B货币的名称，比如curr_B='美元'表示币种是美元
    direction: 表示货币兑换方向，direction='A to B'表示企业向银行用A货币兑换B货币，其他就表示企业向银行用B货币兑换为A货币'''
    if direction == 'A to B':
        # 企业向银行用A货币兑换为B货币
        if N == 'Na':
            # 计算汇兑后的金额
            value = M / Ea
            currency = curr_B
        else:
            # 计算汇兑前的金额
            value = N * Ea
            currency = curr_A
    else:
        # 企业向银行用B货币兑换为A货币
        if N == 'Na':
            # 计算汇兑后的金额
            value = M * Eb
            currency = curr_A
        else:
            # 计算汇兑前的金额
            value = N / Eb
            currency = curr_B
    return [value, currency]


# # 2. 计算美元兑换人民币的金额
# M_USD = 1.3e7  # 汇兑前的美元金额
# USD_RMB_bid = 6.4693  # 美元兑人民币的银行买入价
# USD_RMB_ask = 6.4967  # 美元兑人民币的银行卖出价
#
# value1 = exchange(
#     M=M_USD, N='Na', Ea=USD_RMB_ask, Eb=USD_RMB_bid,
#     curr_A='人民币', curr_B='美元', direction='B to A'
# )
# print('计算2021年8月8日兑换后的金额和币种', value1)
#
#
# # 3. 计算欧元兑换人民币的金额
# M_EUR = 2.1e7  # 汇兑前的欧元金额
# EUR_RMB_bid = 7.6146  # 欧元兑人民币的银行买入价
# EUR_RMB_ask = 7.6708  # 欧元兑人民币的银行卖出价
#
# value2 = exchange(
#     M=M_EUR, N='Na', Ea=EUR_RMB_ask, Eb=EUR_RMB_bid,
#     curr_A='人民币', curr_B='欧元', direction='B to A'
# )
# print('计算2021年8月16日兑换后的金额和币种', value2)
#
#
# # 4. 计算英镑购汇的人民币金额
# N_GBP = 1.05e7  # 汇兑后的英镑金额
# GBP_RMB_bid = 8.8682  # 英镑兑人民币的银行买入价
# GBP_RMB_ask = 8.9335  # 英镑兑人民币的银行卖出价
#
# value3 = exchange(
#     M='Na', N=N_GBP, Ea=GBP_RMB_ask, Eb=GBP_RMB_bid,
#     curr_A='人民币', curr_B='英镑', direction='A to B'
# )
# print('计算2021年9月2日用于英镑购汇的金额和币种', value3)
#
#
# # 5. 计算瑞士法郎购汇的人民币金额
# N_CHF = 3.2e7  # 汇兑后的瑞士法郎金额
# CHF_RMB_bid = 6.8995  # 瑞士法郎兑人民币的银行买入价
# CHF_RMB_ask = 6.9479  # 瑞士法郎兑人民币的银行卖出价
#
# value4 = exchange(
#     M='Na', N=N_CHF, Ea=CHF_RMB_ask, Eb=CHF_RMB_bid,
#     curr_A='人民币', curr_B='瑞士法郎', direction='A to B'
# )
# print('计算2021年9月19日用于瑞士法郎购汇的金额和币种', value4)


'''三角套利'''
# 1. 定义汇率三角套利计算函数
def tri_arbitrage(L, E1a, E1b, E2a, E2b, E3a, E3b, A, B, C):
    '''定义一个计算汇率三角套利收益并显示套利路径的函数，
    并且包括A货币、B货币以及C货币共计3种货币
    L: 代表以A货币计价的初始套利本金
    E1a: 代表A货币兑换B货币的汇率卖出价，标价是以若干单位A货币表示1单位B货币
    E1b: 代表A货币兑换B货币的汇率买入价，标价方式与E1a相同
    E2a: 代表B货币兑换C货币的汇率卖出价，标价是以若干单位B货币表示1单位C货币
    E2b: 代表B货币兑换C货币的汇率买入价，标价方式与E2a相同
    E3a: 代表A货币兑换C货币的汇率卖出价，标价是以若干单位A货币表示1单位C货币
    E3b: 代表A货币兑换C货币的汇率买入价，标价方式与E3a相同
    A: 代表A货币的名称，例如A='人民币'代表A货币是人民币
    B: 代表B货币的名称，例如B='美元'代表B货币是美元
    C: 代表C货币的名称，例如C='欧元'代表C货币是欧元'''
    if E3b / (E1a * E2a) > 1:
        # 套利路径1存在套利机会
        profit = (E3b / (E1a * E2a) - 1) * L
        path = ['套利路径: ', A, '→', B, '→', C, '→', A]
    elif E1b * E2b / E3a > 1:
        # 套利路径2存在套利机会
        profit = (E1b * E2b / E3a - 1) * L
        path = ['套利路径: ', A, '→', C, '→', B, '→', A]
    else:
        # 不存在套利机会
        profit = 0
        path = ['不存在套利机会']
    return [profit, path]

#
# # 2. 初始汇率下的三角套利计算
# value = 2e8  # 初始用于套利的人民币金额
# # 汇率参数（2021年9月23日）
# GBP_RMB_bid = 8.7509   # 英镑兑人民币的买入价
# GBP_RMB_ask = 8.8021   # 英镑兑人民币的卖出价
# CAD_GBP_bid = 0.5715   # 加元兑英镑的买入价
# CAD_GBP_ask = 0.5746   # 加元兑英镑的卖出价
# CAD_RMB_bid = 5.0437   # 加元兑人民币的买入价
# CAD_RMB_ask = 5.0570   # 加元兑人民币的卖出价
#
# result1 = tri_arbitrage(
#     L=value, E1a=GBP_RMB_ask, E1b=GBP_RMB_bid,
#     E2a=CAD_GBP_ask, E2b=CAD_GBP_bid,
#     E3a=CAD_RMB_ask, E3b=CAD_RMB_bid,
#     A='人民币', B='英镑', C='加元'
# )
# print("初始汇率下的套利结果：", result1)
#
#
# # 3. 调整汇率后的三角套利计算
# GBP_RMB_new = 8.7721  # 英镑兑人民币的新卖出价
# result2 = tri_arbitrage(
#     L=value, E1a=GBP_RMB_new, E1b=GBP_RMB_bid,
#     E2a=CAD_GBP_ask, E2b=CAD_GBP_bid,
#     E3a=CAD_RMB_ask, E3b=CAD_RMB_bid,
#     A='人民币', B='英镑', C='加元'
# )
# print("调整汇率后的套利结果：", result2)


'''远期利率测算'''
import datetime as dt

# 1. 定义远期汇率计算函数
def FX_forward(Ea, Eb, r_A, r_B, T0, T1, types):
    '''定义一个计算远期汇率的函数，并且两种货币分别是A货币和B货币
    Ea: 代表A货币兑换B货币的即期汇率卖出价，以若干单位A货币表示1单位B货币
    Eb: 代表A货币兑换B货币的即期汇率买入价，标价方式与Ea一致
    r_A: 代表A货币的无风险利率，并且每年复利1次
    r_B: 代表B货币的无风险利率，复利频次与r_A保持一致
    T0: 代表远期汇率的定价日，以datetime格式输入
    T1: 代表远期汇率的到期日（交割日），输入格式与T0一致
    types: 代表远期汇率价格类型，types='卖出价'代表远期汇率的卖出价，其他则代表买入价'''
    T = (T1 - T0).days / 365  # 计算定价日至到期日的期限（年）
    if types == '卖出价':
        # 针对远期汇率的卖出价
        forward = Ea * (1 + r_A * T) / (1 + r_B * T)
    else:
        # 针对远期汇率的买入价
        forward = Eb * (1 + r_A * T) / (1 + r_B * T)
    return forward

#
# # 2. 计算2021年12月31日到期的远期汇率卖出价
# # 即期汇率参数（2021年9月28日）
# E1_ask = 6.4706  # 美元兑人民币即期卖出价
# E2_ask = 8.8807  # 英镑兑人民币即期卖出价
# E3_ask = 7.5799  # 欧元兑人民币即期卖出价
# E1_bid = 6.4461  # 美元兑人民币即期买入价
# E2_bid = 8.8214  # 英镑兑人民币即期买入价
# E3_bid = 7.5293  # 欧元兑人民币即期买入价
#
# # 无风险利率参数（3个月期）
# Shibor_3M = 0.024170
# Libor_USD_3M = 0.001315
# Libor_GBP_3M = 0.000850
# Euribor_3M = -0.005430
#
# # 时间参数
# T_pricing = dt.datetime(2021, 9, 28)  # 定价日
# T_mature = dt.datetime(2021, 12, 31)  # 到期日
#
# # 计算各货币对的远期汇率卖出价
# F1_ask = FX_forward(
#     Ea=E1_ask, Eb=E1_bid, r_A=Shibor_3M, r_B=Libor_USD_3M,
#     T0=T_pricing, T1=T_mature, types='卖出价'
# )
# F2_ask = FX_forward(
#     Ea=E2_ask, Eb=E2_bid, r_A=Shibor_3M, r_B=Libor_GBP_3M,
#     T0=T_pricing, T1=T_mature, types='卖出价'
# )
# F3_ask = FX_forward(
#     Ea=E3_ask, Eb=E3_bid, r_A=Shibor_3M, r_B=Euribor_3M,
#     T0=T_pricing, T1=T_mature, types='卖出价'
# )
#
# # 输出结果
# print('2021年12月31日到期的美元兑人民币远期汇率卖出价', round(F1_ask, 4))
# print('2021年12月31日到期的英镑兑人民币远期汇率卖出价', round(F2_ask, 4))
# print('2021年12月31日到期的欧元兑人民币远期汇率卖出价', round(F3_ask, 4))
#
#
# # 3. 计算不同到期日的远期汇率买入价
# # 无风险利率参数（6个月期、1年期）
# Shibor_6M = 0.024850
# Shibor_1Y = 0.027130
# Libor_GBP_6M = 0.001568
# Euribor_1Y = -0.004890
#
# # 到期日参数
# T_GBP = dt.datetime(2022, 3, 30)  # 英镑远期到期日
# T_Eur = dt.datetime(2022, 9, 26)  # 欧元远期到期日
#
# # 计算远期汇率买入价
# F_GBP_bid = FX_forward(
#     Ea=E2_ask, Eb=E2_bid, r_A=Shibor_6M, r_B=Libor_GBP_6M,
#     T0=T_pricing, T1=T_GBP, types='买入价'
# )
# F_Eur_bid = FX_forward(
#     Ea=E3_ask, Eb=E3_bid, r_A=Shibor_1Y, r_B=Euribor_1Y,
#     T0=T_pricing, T1=T_Eur, types='买入价'
# )
#
# # 输出结果
# print('2022年3月30日到期的英镑兑人民币远期汇率买入价', round(F_GBP_bid, 4))
# print('2022年9月26日到期的欧元兑人民币远期汇率买入价', round(F_Eur_bid, 4))


'''抵补套利'''
# 1. 定义抵补套利收益计算函数
def cov_arbitrage(Ea, Eb, Fa, Fb, L_A, L_B, R_A, R_B, T, A, B):
    '''定义一个计算抵补套利收益并给出套利路径的函数，两种货币分别是A货币和B货币
    Ea: 代表A货币兑换B货币的即期汇率卖出价，以若干单位A货币表示1单位B货币
    Eb: 代表A货币兑换B货币的即期汇率买入价，标价方式与Ea相同
    Fa: 代表A货币兑换B货币的远期汇率卖出价，标价方式与Ea相同
    Fb: 代表A货币兑换B货币的远期汇率买入价，标价方式与Ea相同
    L_A: 套利初始时刻借入的A货币本金
    L_B: 套利初始时刻借入的B货币本金
    R_A: 代表A货币的利率（收益率），并且每年复利1次
    R_B: 代表B货币的利率（收益率），并且每年复利1次
    T: 套利的期限长度，单位是年
    A: 代表A货币的名称，例如A='人民币'代表A货币是人民币
    B: 代表B货币的名称，例如B='美元'代表B货币是美元'''
    if Fb * (1 + R_B * T) / (Ea * (1 + R_A * T)) > 1:
        # 期初借入A货币、期末偿还A货币的套利路径成功
        profit = (Fb * (1 + R_B * T) / Ea - (1 + R_A * T)) * L_A
        sequence = [
            '套利路径如下',
            '第1步，初始借入的货币：', A,
            '第2步，按即期汇率兑换后并投资的货币：', B,
            '第3步，在投资结束时按远期汇率兑换后的货币：', A,
            '第4步，偿还初始借入的本金和利息'
        ]
    elif Eb * (1 + R_A * T) / (Fa * (1 + R_B * T)) > 1:
        # 期初借入B货币、期末偿还B货币的套利路径成功
        profit = (Eb * (1 + R_A * T) / Fa - (1 + R_B * T)) * L_B
        sequence = [
            '套利路径如下',
            '第1步，初始借入的货币：', B,
            '第2步，按即期汇率兑换后并投资的货币：', A,
            '第3步，在投资结束时按远期汇率兑换后的货币：', B,
            '第4步，偿还初始借入的本金和利息'
        ]
    else:
        # 不存在套利机会
        profit = 'Na'
        sequence = '套利机会不存在'
    return [profit, sequence]


# # 2. 输入6个月期抵补套利参数
# # 汇率参数
# ## 欧元兑人民币
# E1_ask = 7.4841
# E1_bid = 7.4294
# F1_6M_ask = 7.6446
# F1_6M_bid = 7.5552
# ## 100日元兑人民币
# E2_ask = 5.7160
# E2_bid = 5.6742
# F2_6M_ask = 5.8204
# F2_6M_bid = 5.7529
# ## 港元兑人民币
# E3_ask = 0.8311
# E3_bid = 0.8278
# F3_6M_ask = 0.8464
# F3_6M_bid = 0.8368
#
# # 利率参数（6个月期）
# Shibor_6M = 0.024920
# Euribor_6M = -0.005230
# Tibor_6M = 0.001264
# Hibor_6M = 0.002170
#
# # 本金参数
# L_RMB = 7e8
# L_EUR = 1e8
# L_JPY = 1e10
# L_HKD = 8e8
#
# # 期限
# T1 = 0.5
#
#
# # 3. 计算6个月期各货币对的抵补套利
# result1_6M = cov_arbitrage(
#     Ea=E1_ask, Eb=E1_bid, Fa=F1_6M_ask, Fb=F1_6M_bid,
#     L_A=L_RMB, L_B=L_EUR, R_A=Shibor_6M, R_B=Euribor_6M,
#     T=T1, A='人民币', B='欧元'
# )
# result2_6M = cov_arbitrage(
#     Ea=E2_ask, Eb=E2_bid, Fa=F2_6M_ask, Fb=F2_6M_bid,
#     L_A=L_RMB, L_B=L_JPY, R_A=Shibor_6M, R_B=Tibor_6M,
#     T=T1, A='人民币', B='日元'
# )
# result3_6M = cov_arbitrage(
#     Ea=E3_ask, Eb=E3_bid, Fa=F3_6M_ask, Fb=F3_6M_bid,
#     L_A=L_RMB, L_B=L_HKD, R_A=Shibor_6M, R_B=Hibor_6M,
#     T=T1, A='人民币', B='港元'
# )
# print("欧元兑人民币6个月期抵补套利结果：", result1_6M)
# print("日元兑人民币6个月期抵补套利结果：", result2_6M)
# print("港元兑人民币6个月期抵补套利结果：", result3_6M)
#
#
# # 4. 输入1年期抵补套利参数
# # 远期汇率参数（1年期）
# F1_1Y_ask = 7.7740
# F1_1Y_bid = 7.6800
# F2_1Y_ask = 5.9084
# F2_1Y_bid = 5.8375
# F3_1Y_ask = 0.8573
# F3_1Y_bid = 0.8488
#
# # 利率参数（1年期）
# Shibor_1Y = 0.027160
# Euribor_1Y = -0.004760
# Tibor_1Y = -0.001564
# Hibor_1Y = 0.003215
#
# # 期限
# T2 = 1
#
#
# # 5. 计算1年期各货币对的抵补套利
# result1_1Y = cov_arbitrage(
#     Ea=E1_ask, Eb=E1_bid, Fa=F1_1Y_ask, Fb=F1_1Y_bid,
#     L_A=L_RMB, L_B=L_EUR, R_A=Shibor_1Y, R_B=Euribor_1Y,
#     T=T2, A='人民币', B='欧元'
# )
# result2_1Y = cov_arbitrage(
#     Ea=E2_ask, Eb=E2_bid, Fa=F2_1Y_ask, Fb=F2_1Y_bid,
#     L_A=L_RMB, L_B=L_JPY, R_A=Shibor_1Y, R_B=Tibor_1Y,
#     T=T2, A='人民币', B='日元'
# )
# result3_1Y = cov_arbitrage(
#     Ea=E3_ask, Eb=E3_bid, Fa=F3_1Y_ask, Fb=F3_1Y_bid,
#     L_A=L_RMB, L_B=L_HKD, R_A=Shibor_1Y, R_B=Hibor_1Y,
#     T=T2, A='人民币', B='港元'
# )
# print("欧元兑人民币1年期抵补套利结果：", result1_1Y)
# print("日元兑人民币1年期抵补套利结果：", result2_1Y)
# print("港元兑人民币1年期抵补套利结果：", result3_1Y)
#
#
# # 6. 调整港元利率后的1年期抵补套利
# R_HKD_1Y = Hibor_1Y + 0.01
# result4_1Y = cov_arbitrage(
#     Ea=E3_ask, Eb=E3_bid, Fa=F3_1Y_ask, Fb=F3_1Y_bid,
#     L_A=L_RMB, L_B=L_HKD, R_A=Shibor_1Y, R_B=R_HKD_1Y,
#     T=T2, A='人民币', B='港元'
# )
# print('运用港元兑人民币汇率开展的抵补套利收益', round(result4_1Y[0], 2))
# print('运用港元兑人民币汇率开展的抵补套利路径', result4_1Y[1])


'''远期外汇合约'''
import numpy as np
from numpy import exp
import datetime as dt


# 1. 定义远期外汇合约价值计算函数
def Value_FXforward(F0, F1, E, L_A, L_B, R_A, R_B, T_price, T_end, vc, position):
    '''定义一个计算远期外汇合约价值的函数，两种货币分别是A货币和B货币
    F0: 代表合约约定的远期汇率，以若干单位A货币表示1单位B货币
    F1: 代表合约定价日的远期汇率，标价方式与F0相同
    E: 代表合约定价日的即期汇率，标价方式与F0相同
    L_A: 代表以A货币计价的合约本金，L_A='Na'代表合约本金不是以A货币计价的
    L_B: 代表以B货币计价的合约本金，L_B='Na'代表合约本金不是以B货币计价的
    R_A: 代表A货币的无风险利率（连续复利）
    R_B: 代表B货币的无风险利率（连续复利）
    T_price: 代表合约定价日的日期，用时间对象格式输入
    T_end: 代表合约到期日的日期，输入格式与T_price相同
    vc: 代表合约价值的计价币种，vc='A'代表选择A货币，其他则代表选择B货币
    position: 代表头寸方向，position='long'代表多头，其他代表空头'''
    t = (T_end - T_price).days / 365  # 计算合约的剩余期限（年）

    if position == 'long':
        # 针对合约多头
        if L_B == 'Na':
            # 合约本金以A货币计价
            if vc == 'A':
                value = E * (L_A / F1 - L_A / F0) * exp(-R_B * t)
            else:
                value = (L_A / F1 - L_A / F0) * exp(-R_B * t)
        else:
            # 合约本金以B货币计价
            if vc == 'A':
                value = (L_B * F1 - L_B * F0) * exp(-R_A * t)
            else:
                value = (L_B * F1 - L_B * F0) * exp(-R_A * t) / E
    else:
        # 针对合约空头
        if L_B == 'Na':
            # 合约本金以A货币计价
            if vc == 'A':
                value = E * (L_A / F0 - L_A / F1) * exp(-R_B * t)
            else:
                value = (L_A / F0 - L_A / F1) * exp(-R_B * t)
        else:
            # 合约本金以B货币计价
            if vc == 'A':
                value = (L_B * F0 - L_B * F1) * exp(-R_A * t)
            else:
                value = (L_B * F0 - L_B * F1) * exp(-R_A * t) / E
    return value


# # 2. 2021年10月15日的远期外汇合约估值
# # 时间参数
# T1 = dt.datetime(2021, 10, 15)  # 定价日
# T_mature = dt.datetime(2022, 1, 20)  # 到期日
#
# # 本金参数
# L_USD = 2.5e7  # 美元本金（第1笔合约）
# L_TWD = 3.8e8  # 新台币本金（第2笔合约）
# L_GBP = 1.9e7  # 英镑本金（第3笔合约）
#
# # 汇率参数
# ## 初始远期汇率（2021年7月20日）
# F0_USD_TWD = 27.950
# F0_EUR_TWD = 33.423
# F0_GBP_TWD = 38.485
# ## 定价日远期汇率（2021年10月15日）
# F1_USD_TWD = 27.957
# F1_EUR_TWD = 32.828
# F1_GBP_TWD = 38.700
# ## 定价日即期汇率（2021年10月15日）
# E1_USD_TWD = 27.980
# E1_EUR_TWD = 32.750
# E1_GBP_TWD = 38.670
#
# # 无风险利率参数（2021年10月15日）
# Taibor1 = 0.0048044
# Libor1_USD = 0.001236
# Libor1_EUR = -0.005706
# Libor1_GBP = 0.001344
#
# # 计算各合约价值
# V1_USD_TWD = Value_FXforward(
#     F0=F0_USD_TWD, F1=F1_USD_TWD, E=E1_USD_TWD,
#     L_A='Na', L_B=L_USD, R_A=Taibor1, R_B=Libor1_USD,
#     T_price=T1, T_end=T_mature, vc='A', position='long'
# )
# V1_EUR_TWD = Value_FXforward(
#     F0=F0_EUR_TWD, F1=F1_EUR_TWD, E=E1_EUR_TWD,
#     L_A=L_TWD, L_B='Na', R_A=Taibor1, R_B=Libor1_EUR,
#     T_price=T1, T_end=T_mature, vc='A', position='long'
# )
# V1_GBP_TWD = Value_FXforward(
#     F0=F0_GBP_TWD, F1=F1_GBP_TWD, E=E1_GBP_TWD,
#     L_A='Na', L_B=L_GBP, R_A=Taibor1, R_B=Libor1_GBP,
#     T_price=T1, T_end=T_mature, vc='A', position='short'
# )
#
# # 输出结果
# print('2021年10月15日V银行针对第1笔外汇远期合约的估值（新台币）', round(V1_USD_TWD, 2))
# print('2021年10月15日V银行针对第2笔外汇远期合约的估值（新台币）', round(V1_EUR_TWD, 2))
# print('2021年10月15日V银行针对第3笔外汇远期合约的估值（新台币）', round(V1_GBP_TWD, 2))
#
# # 3. 2021年10月26日的远期外汇合约估值
# # 时间参数
# T2 = dt.datetime(2021, 10, 26)  # 定价日
#
# # 汇率参数
# ## 定价日远期汇率（2021年10月26日）
# F2_USD_TWD = 27.755
# F2_EUR_TWD = 32.576
# F2_GBP_TWD = 38.570
# ## 定价日即期汇率（2021年10月26日）
# E2_USD_TWD = 27.780
# E2_EUR_TWD = 32.490
# E2_GBP_TWD = 38.540
#
# # 无风险利率参数（2021年10月26日）
# Taibor2 = 0.0048044
# Libor2_USD = 0.001359
# Libor2_EUR = -0.005606
# Libor2_GBP = 0.002040
#
# # 计算各合约价值
# V2_USD_TWD = Value_FXforward(
#     F0=F0_USD_TWD, F1=F2_USD_TWD, E=E2_USD_TWD,
#     L_A='Na', L_B=L_USD, R_A=Taibor2, R_B=Libor2_USD,
#     T_price=T2, T_end=T_mature, vc='B', position='short'
# )
# V2_EUR_TWD = Value_FXforward(
#     F0=F0_EUR_TWD, F1=F2_EUR_TWD, E=E2_EUR_TWD,
#     L_A=L_TWD, L_B='Na', R_A=Taibor2, R_B=Libor2_EUR,
#     T_price=T2, T_end=T_mature, vc='B', position='short'
# )
# V2_GBP_TWD = Value_FXforward(
#     F0=F0_GBP_TWD, F1=F2_GBP_TWD, E=E2_GBP_TWD,
#     L_A='Na', L_B=L_GBP, R_A=Taibor2, R_B=Libor2_GBP,
#     T_price=T2, T_end=T_mature, vc='B', position='long'
# )
#
# # 输出结果
# print('2021年10月26日W企业针对第1笔外汇远期合约的估值（美元）', round(V2_USD_TWD, 2))
# print('2021年10月26日W企业针对第2笔外汇远期合约的估值（欧元）', round(V2_EUR_TWD, 2))
# print('2021年10月26日W企业针对第3笔外汇远期合约的估值（英镑）', round(V2_GBP_TWD, 2))