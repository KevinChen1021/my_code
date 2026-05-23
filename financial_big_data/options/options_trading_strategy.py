import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
from pylab import mpl
from pandas.plotting import register_matplotlib_converters
from math import ceil
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
register_matplotlib_converters()


'''Principal-Protected Notes，PPN 合成保本票据'''
# # 1. 保本票据构建（基础示例）
# par_ppn = 100  # 保本票据本金
# par_bond = 100  # 无风险零息债券面值
# price_bond = 96  # 无风险零息债券价格
# price_call = 0.4  # 欧式看涨期权报价
# K = 5.0  # 期权行权价格
#
# N_bond = par_ppn / par_bond  # 购买的无风险零息债券数量
# N_call = (par_ppn - N_bond*price_bond) / price_call  # 购买的欧式看涨期权数量
# print('构建1份保本票据需要购买的无风险零息债券数量', N_bond)
# print('构建1份保本票据需要购买的欧式看涨期权数量', N_call)
#
#
# # 2. 保本票据收益率与股价的关系可视化
# price_z_list = np.linspace(3, 7, 120)  # 期权到期时Z股票价格序列
# profit_call = np.maximum(price_z_list - K, 0)  # 欧式看涨期权到期收益
# profit_ppn = N_bond*par_bond + N_call*profit_call - par_ppn  # 保本票据到期收益金额
# return_ppn = profit_ppn / par_ppn  # 保本票据到期收益率
#
# plt.figure(figsize=(9,6))
# plt.plot(price_z_list, return_ppn, 'r-', lw=2.5)
# plt.xlabel(u'Z股票价格', fontsize=13)
# plt.ylabel(u'保本票据收益率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'Z股票价格与保本票据收益率的关系图', fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 3. 实际保本票据构建（18四川01债券+300ETF期权）
# par_PPN = 1e8  # 保本票据的面值
# par_SC = 100  # 18四川01债券的面值
# coupon = 0.0373  # 18四川01债券的票面利率
# price_SC = 102.2682  # 2020年8月24日18四川01债券的价格
# price_opt = 0.2230  # 2020年8月24日沪深300ETF认购期权的价格
# price_300ETF = 4.8207  # 2020年8月24日沪深300ETF基金的净值
# K_300ETF = 5.0  # 期权行权价格
# price_HS300 = 4755.85  # 2020年8月24日沪深300指数的收盘价
# N1 = 10  # 债券的交易单位（10张）
# N2 = 10000  # 每张期权合约单位（10000份沪深300ETF基金）
#
#
# # 4. 计算债券与期权数量
# cashflow_SC = par_SC*(1+coupon)  # 18四川01债券到期日本息
# N_SC = N1 * ceil(par_PPN / (N1*cashflow_SC))  # 购买债券数量（10张的整数倍）
# print('购买18四川01债券数量（张）', N_SC)
#
# N_opt = (par_PPN - price_SC*N_SC) / (price_opt*N2)  # 计算期权合约数量
# N_opt = int(N_opt)  # 确保期权合约数量是整数
# print('购买300ETF购3月5000期权合约数量（张）', N_opt)
#
# cash = par_PPN - price_SC*N_SC - N_opt*price_opt*N2  # 剩余现金
# print('保本票据本金未用于购买债券和期权的剩余现金', round(cash, 2))
#
# K_HS300 = K_300ETF * price_HS300 / price_300ETF  # 对应期权行权价格的沪深300指数点位
# print('恰好等于期权行权价格的沪深300指数点位', round(K_HS300, 2))
#
#
# # 5. 不同指数涨幅下的保本票据收益率
# HS300_chg = np.array([0.05, 0.1, 0.2, 0.3])  # 沪深300指数涨幅数组
# profit_opt = N_opt*N2 * np.maximum(price_300ETF*(1+HS300_chg) - K_300ETF, 0)  # 期权收益
# profit_PPN = cashflow_SC*N_SC + cash + profit_opt - par_PPN  # 保本票据收益金额
# R_PPN = profit_PPN / par_PPN  # 保本票据收益率
#
# print('到期日沪深300指数上涨5%时保本票据收益率', round(R_PPN[0], 6))
# print('到期日沪深300指数上涨10%时保本票据收益率', round(R_PPN[1], 6))
# print('到期日沪深300指数上涨20%时保本票据收益率', round(R_PPN[2], 6))
# print('到期日沪深300指数上涨30%时保本票据收益率', round(R_PPN[3], 6))
#
#
# # 6. 沪深300指数与保本票据收益率的关系可视化
# HS300_list = np.linspace(4000, 7000, 500)  # 保本票据到期时沪深300指数序列
# price_300ETF_list = HS300_list * (price_300ETF / price_HS300)  # 沪深300ETF基金净值数组
# profit_opt_list = N_opt*N2 * np.maximum(price_300ETF_list - K_300ETF, 0)  # 期权收益金额数组
# profit_PPN_list = cashflow_SC*N_SC + cash + profit_opt_list - par_PPN  # 保本票据收益金额数组
# R_PPN_list = profit_opt_list / par_PPN  # 保本票据收益率数组
#
# plt.figure(figsize=(9,6))
# plt.plot(HS300_list, R_PPN_list, 'r-', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'保本票据收益率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与保本票据收益率的关系图', fontsize=13)
# plt.grid()
# plt.show()


'''single options and single underlying'''
# # 1. 买入备兑看涨期权策略（2020年6月1日构建）
# C = 0.2065  # 看涨期权价格
# K = 4.0  # 看涨期权行权价格
# S0_ETF = 4.0364  # 沪深300ETF基金净值
# S0_index = 3971.34  # 沪深300指数收盘价
#
# St_index = np.linspace(3000, 5000, 500)  # 期权到期日沪深300指数序列
# St_ETF = S0_ETF * St_index / S0_index  # 对应ETF净值
# N_ETF = 10000  # ETF基金空头头寸数量
# N_call = 1  # 认购期权多头头寸数量
# N_underlying = 10000  # 1张期权对应基金份数
#
# # 计算各部分收益
# profit_ETF_short = -N_ETF * (St_ETF - S0_ETF)  # ETF空头收益
# profit_call_long = N_call * N_underlying * (np.maximum(St_ETF - K, 0) - C)  # 认购期权多头收益
# profit_covcall_long = profit_ETF_short + profit_call_long  # 备兑看涨策略收益
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(St_index, profit_ETF_short, 'b--', label=u'沪深300ETF基金空头', lw=2.5)
# plt.plot(St_index, profit_call_long, 'g--', label=u'沪深300ETF认购期权多头', lw=2.5)
# plt.plot(St_index, profit_covcall_long, 'r-', label=u'买入备兑看涨期权策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与买入备兑看涨期权收益的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 2. 卖出备兑看涨期权策略（2020年7月1日构建）
# C = 0.201  # 看涨期权价格
# K = 4.3  # 看涨期权行权价格
# S0_ETF = 4.3429  # ETF基金净值
# S0_index = 4247.78  # 沪深300指数收盘价
#
# St_index = np.linspace(3500, 5500, 500)  # 期权到期日指数序列
# St_ETF = S0_ETF * St_index / S0_index  # 对应ETF净值
#
# # 计算各部分收益
# profit_ETF_long = N_ETF * (St_ETF - S0_ETF)  # ETF多头收益
# profit_call_short = -N_call * N_underlying * (np.maximum(St_ETF - K, 0) - C)  # 认购期权空头收益
# profit_covcall_short = profit_ETF_long + profit_call_short  # 卖出备兑看涨策略收益
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(St_index, profit_ETF_long, 'b--', label=u'沪深300ETF基金多头', lw=2.5)
# plt.plot(St_index, profit_call_short, 'g--', label=u'沪深300ETF认购期权空头', lw=2.5)
# plt.plot(St_index, profit_covcall_short, 'r-', label=u'卖出备兑看涨期权策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与卖出备兑看涨期权收益的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 3. 买入保护看跌期权策略（2020年8月3日构建）
# P = 0.4416  # 看跌期权价格
# K = 4.9  # 看跌期权行权价格
# S0_ETF = 4.9168  # ETF基金净值
# S0_index = 4771.31  # 沪深300指数收盘价
#
# St_index = np.linspace(4000, 6000, 500)  # 期权到期日指数序列
# St_ETF = S0_ETF * St_index / S0_index  # 对应ETF净值
# N_put = 1  # 认沽期权多头头寸数量
#
# # 计算各部分收益
# profit_ETF_long = N_ETF * (St_ETF - S0_ETF)  # ETF多头收益
# profit_put_long = N_put * N_underlying * (np.maximum(K - St_ETF, 0) - P)  # 认沽期权多头收益
# profit_protput_long = profit_ETF_long + profit_put_long  # 保护看跌策略收益
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(St_index, profit_ETF_long, 'b--', label=u'沪深300ETF基金多头', lw=2.5)
# plt.plot(St_index, profit_put_long, 'g--', label=u'沪深300ETF认沽期权多头', lw=2.5)
# plt.plot(St_index, profit_protput_long, 'r-', label=u'买入保护看跌期权策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与买入保护看跌期权收益的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 4. 卖出保护看跌期权策略（2020年9月1日构建）
# P = 0.4211  # 看跌期权价格
# K = 5.0  # 看跌期权行权价格
# S0_ETF = 4.9966  # ETF基金净值
# S0_index = 4842.12  # 沪深300指数收盘价
#
# St_index = np.linspace(3800, 5800, 500)  # 期权到期日指数序列
# St_ETF = S0_ETF * St_index / S0_index  # 对应ETF净值
#
# # 计算各部分收益
# profit_ETF_short = -N_ETF * (St_ETF - S0_ETF)  # ETF空头收益
# profit_put_short = -N_put * N_underlying * (np.maximum(K - St_ETF, 0) - P)  # 认沽期权空头收益
# profit_protput_short = profit_ETF_short + profit_put_short  # 卖出保护看跌策略收益
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(St_index, profit_ETF_short, 'b--', label=u'沪深300ETF基金空头', lw=2.5)
# plt.plot(St_index, profit_put_short, 'g--', label=u'沪深300ETF认沽期权空头', lw=2.5)
# plt.plot(St_index, profit_protput_short, 'r-', label=u'卖出保护看跌期权策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与卖出保护看跌期权收益的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 5. 期权策略期间收益分析（导入外部数据）
# price = pd.read_excel(r'C:\Desktop\沪深300ETF期权价格与沪深300ETF基金净值(2019年12月至2020年6月).xlsx',
#                       sheet_name="Sheet1", header=0, index_col=0)
# price.index = pd.DatetimeIndex(price.index)  # 转换索引为datetime格式
#
# # 提取初始价格
# P0_call = price['看涨期权'].iloc[0]
# P0_put = price['看跌期权'].iloc[0]
# P0_ETF = price['沪深300ETF'].iloc[0]
#
# # 计算期间收益
# profit_call = N_call * N_underlying * (price['看涨期权'] - P0_call)  # 看涨期权期间收益
# profit_put = N_put * N_underlying * (price['看跌期权'] - P0_put)  # 看跌期权期间收益
# profit_ETF = N_ETF * (price['沪深300ETF'] - P0_ETF)  # ETF基金期间收益
#
# # 各策略期间收益
# profit_covcall_long = -profit_ETF + profit_call  # 买入备兑看涨
# profit_covcall_short = -profit_covcall_long  # 卖出备兑看涨
# profit_protput_long = profit_put + profit_ETF  # 买入保护看跌
# profit_protput_short = -profit_protput_long  # 卖出保护看跌
#
# # 可视化（子图）
# plt.figure(figsize=(9,9))
# # 子图1：备兑看涨策略
# plt.subplot(2,1,1)
# plt.plot(profit_covcall_long, 'g-', label=u'买入备兑看涨期权策略', lw=2.0)
# plt.plot(profit_covcall_short, 'c-', label=u'卖出备兑看涨期权策略', lw=2.0)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
#
# # 子图2：保护看跌策略
# plt.subplot(2,1,2)
# plt.plot(profit_protput_long, 'm-', label=u'买入保护看跌期权策略', lw=2.0)
# plt.plot(profit_protput_short, 'y-', label=u'卖出保护看跌期权策略', lw=2.0)
# plt.xlabel(u'日期', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
#
# plt.show()


'''spread trading strategy'''
# # 1. 牛市价差策略（看涨期权组合）
# K1 = 4500  # 较低行权价格
# K2 = 5000  # 较高行权价格
# C1 = 474.4  # 较低行权价格看涨期权价格
# C2 = 293.0  # 较高行权价格看涨期权价格
# S0 = 4762.76  # 策略构建日指数收盘价
# St = np.linspace(3500, 6500, 500)  # 期权到期日指数序列
# N1 = 1  # 较低行权价格期权多头数量
# N2 = 1  # 较高行权价格期权空头数量
# M = 100  # 合约乘数（每点100元）
#
# # 计算收益
# profit_C1_long = N1 * M * (maximum(St - K1, 0) - C1)  # 较低行权看涨期权多头收益
# profit_C2_short = N2 * M * (C2 - maximum(St - K2, 0))  # 较高行权看涨期权空头收益
# profit_bullspread = profit_C1_long + profit_C2_short  # 牛市价差策略收益
#
# # 可视化
# plt.figure(figsize=(9, 6))
# plt.plot(St, profit_C1_long, 'b--', label=u'较低行权价格沪深300股指认购期权多头', lw=2.5)
# plt.plot(St, profit_C2_short, 'g--', label=u'较高行权价格沪深300股指认购期权空头', lw=2.5)
# plt.plot(St, profit_bullspread, 'r-', label=u'牛市价差策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与牛市价差策略收益的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
# # 2. 牛市价差策略（看跌期权组合）
# K1 = 4400  # 较低行权价格
# K2 = 5200  # 较高行权价格
# P1 = 290.0  # 较低行权价格看跌期权价格
# P2 = 873.8  # 较高行权价格看跌期权价格
# S0 = 4812.76  # 策略构建日指数收盘价
# St = np.linspace(3000, 6000, 500)  # 期权到期日指数序列
#
# # 计算收益
# profit_P1_long = N1 * M * (maximum(K1 - St, 0) - P1)  # 较低行权看跌期权多头收益
# profit_P2_short = N2 * M * (P2 - maximum(K2 - St, 0))  # 较高行权看跌期权空头收益
# profit_bullspread = profit_P1_long + profit_P2_short  # 牛市价差策略收益
#
# # 可视化
# plt.figure(figsize=(9, 6))
# plt.plot(St, profit_P1_long, 'b--', label=u'较低行权价格沪深300股指认沽期权多头', lw=2.5)
# plt.plot(St, profit_P2_short, 'g--', label=u'较高行权价格沪深300股指认沽期权空头', lw=2.5)
# plt.plot(St, profit_bullspread, 'r-', label=u'牛市价差策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与牛市价差策略收益的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
# # 3. 熊市价差策略（看跌期权组合）
# K1 = 4500  # 较低行权价格
# K2 = 5400  # 较高行权价格
# P1 = 237.0  # 较低行权价格看跌期权价格
# P2 = 818.2  # 较高行权价格看跌期权价格
# S0 = 4844.27  # 策略构建日指数收盘价
# St = np.linspace(3400, 6400, 500)  # 期权到期日指数序列
#
# # 计算收益
# profit_P1_short = N1 * M * (P1 - maximum(K1 - St, 0))  # 较低行权看跌期权空头收益
# profit_P2_long = N2 * M * (maximum(K2 - St, 0) - P2)  # 较高行权看跌期权多头收益
# profit_bearspread = profit_P1_short + profit_P2_long  # 熊市价差策略收益
#
# # 可视化
# plt.figure(figsize=(9, 6))
# plt.plot(St, profit_P1_short, 'b--', label=u'较低行权价格沪深300股指认沽期权空头', lw=2.5)
# plt.plot(St, profit_P2_long, 'g--', label=u'较高行权价格沪深300股指认沽期权多头', lw=2.5)
# plt.plot(St, profit_bearspread, 'r-', label=u'熊市价差策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与熊市价差策略收益的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
# # 4. 熊市价差策略（看涨期权组合）
# K1 = 4300  # 较低行权价格
# K2 = 5200  # 较高行权价格
# C1 = 486.0  # 较低行权价格看涨期权价格
# C2 = 152.4  # 较高行权价格看涨期权价格
# S0 = 4694.39  # 策略构建日指数收盘价
# St = np.linspace(3300, 6200, 500)  # 期权到期日指数序列
#
# # 计算收益
# profit_C1_short = N1 * M * (C1 - maximum(St - K1, 0))  # 较低行权看涨期权空头收益
# profit_C2_long = N2 * M * (maximum(St - K2, 0) - C2)  # 较高行权看涨期权多头收益
# profit_bearspread = profit_C1_short + profit_C2_long  # 熊市价差策略收益
#
# # 可视化
# plt.figure(figsize=(9, 6))
# plt.plot(St, profit_C1_short, 'b--', label=u'较低行权价格沪深300股指认购期权空头', lw=2.5)
# plt.plot(St, profit_C2_long, 'g--', label=u'较高行权价格沪深300股指认购期权多头', lw=2.5)
# plt.plot(St, profit_bearspread, 'r-', label=u'熊市价差策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与熊市价差策略价值的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
# # 5. 盒式价差策略
# K1 = 4000  # 较低行权价格
# K2 = 4600  # 较高行权价格
# C1 = 161.6  # 较低行权看涨期权价格
# C2 = 33.2  # 较高行权看涨期权价格
# P1 = 285.4  # 较低行权看跌期权价格
# P2 = 776.0  # 较高行权看跌期权价格
# S0 = 4044.38  # 策略构建日指数收盘价
# St = np.linspace(3000, 5000, 500)  # 期权到期日指数序列
#
# # 计算收益
# profit_C1_long = N1 * M * (maximum(St - K1, 0) - C1)  # 较低行权看涨期权多头收益
# profit_P1_short = N1 * M * (P1 - maximum(K1 - St, 0))  # 较低行权看跌期权空头收益
# profit_C2_short = N2 * M * (C2 - maximum(St - K2, 0))  # 较高行权看涨期权空头收益
# profit_P2_long = N2 * M * (maximum(K2 - St, 0) - P2)  # 较高行权看跌期权多头收益
# profit_boxspread = profit_C1_long + profit_C2_short + profit_P1_short + profit_P2_long  # 盒式价差策略收益
#
# # 可视化
# plt.figure(figsize=(9, 6))
# plt.plot(St, profit_C1_long, 'b--', label=u'较低行权价格沪深300股指认购期权多头', lw=2.5)
# plt.plot(St, profit_C2_short, 'g--', label=u'较高行权价格沪深300股指认购期权空头', lw=2.5)
# plt.plot(St, profit_P1_short, 'c--', label=u'较低行权价格沪深300股指认沽期权空头', lw=2.5)
# plt.plot(St, profit_P2_long, 'm--', label=u'较高行权价格沪深300股指认沽期权多头', lw=2.5)
# plt.plot(St, profit_boxspread, 'r-', label=u'盒式价差策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与盒式价差策略收益的关系图', fontsize=13)
# plt.legend(fontsize=12)
# plt.grid()
# plt.show()
#
# # 盒式价差策略现值计算
# shibor = 0.02115  # 6个月期Shibor
# tenor = 0.5  # 期权剩余期限（年）
# PV_boxspread = profit_boxspread[0] * exp(-shibor * tenor)  # 收益现值
# print('策略构建日（2020年6月18日）盒式价差策略收益', round(PV_boxspread, 2))
#
# # 6. 蝶式价差策略（看涨期权组合）
# K1 = 4400  # 较低行权价格
# K2 = 4800  # 中间行权价格
# K3 = 5200  # 较高行权价格
# C1 = 571.6  # 较低行权看涨期权价格
# C2 = 388.6  # 中间行权看涨期权价格
# C3 = 255.0  # 较高行权看涨期权价格
# S0 = 4842.12  # 策略构建日指数收盘价
# St = np.linspace(3400, 6200, 500)  # 期权到期日指数序列
# N1 = 1  # 较低行权期权多头数量
# N2 = 2  # 中间行权期权空头数量
# N3 = 1  # 较高行权期权多头数量
#
# # 计算收益
# profit_C1_long = N1 * M * (maximum(St - K1, 0) - C1)  # 较低行权看涨期权多头收益
# profit_C2_short = N2 * M * (C2 - maximum(St - K2, 0))  # 中间行权看涨期权空头收益
# profit_C3_long = N3 * M * (maximum(St - K3, 0) - C3)  # 较高行权看涨期权多头收益
# profit_buttspread = profit_C1_long + profit_C2_short + profit_C3_long  # 蝶式价差策略收益
#
# # 可视化
# plt.figure(figsize=(9, 6))
# plt.plot(St, profit_C1_long, 'b--', label=u'较低行权价格沪深300股指认购期权多头', lw=2.5)
# plt.plot(St, profit_C2_short, 'g--', label=u'中间行权价格沪深300股指认购期权空头', lw=2.5)
# plt.plot(St, profit_C3_long, 'c--', label=u'较高行权价格沪深300股指认购期权多头', lw=2.5)
# plt.plot(St, profit_buttspread, 'r-', label=u'蝶式价差策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与蝶式价差策略收益的关系图', fontsize=13)
# plt.legend(fontsize=12)
# plt.grid()
# plt.show()
#
# # 7. 蝶式价差策略（看跌期权组合）
# K1 = 4200  # 较低行权价格
# K2 = 4600  # 中间行权价格
# K3 = 5000  # 较高行权价格
# P1 = 264.2  # 较低行权看跌期权价格
# P2 = 476.2  # 中间行权看跌期权价格
# P3 = 748.2  # 较高行权看跌期权价格
# S0 = 4581.98  # 策略构建日指数收盘价
# St = np.linspace(3200, 6000, 500)  # 期权到期日指数序列
#
# # 计算收益
# profit_P1_long = N1 * M * (maximum(K1 - St, 0) - P1)  # 较低行权看跌期权多头收益
# profit_P2_short = N2 * M * (P2 - maximum(K2 - St, 0))  # 中间行权看跌期权空头收益
# profit_P3_long = N3 * M * (maximum(K3 - St, 0) - P3)  # 较高行权看跌期权多头收益
# profit_buttspread = profit_P1_long + profit_P2_short + profit_P3_long  # 蝶式价差策略收益
#
# # 可视化
# plt.figure(figsize=(9, 6))
# plt.plot(St, profit_P1_long, 'b--', label=u'较低行权价格沪深300股指认沽期权多头', lw=2.5)
# plt.plot(St, profit_P2_short, 'g--', label=u'中间行权价格沪深300股指认沽期权空头', lw=2.5)
# plt.plot(St, profit_P3_long, 'c--', label=u'较高行权价格沪深300股指认沽期权多头', lw=2.5)
# plt.plot(St, profit_buttspread, 'r-', label=u'蝶式价差策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与蝶式价差策略收益的关系图', fontsize=13)
# plt.legend(fontsize=12)
# plt.grid()
# plt.show()


# 8. 日历价差策略（看涨期权组合）
def binomial_tree_model_n_step(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps, option_type):
    '''N步二叉树模型计算欧式期权价值'''
    t = time_to_maturity / steps
    u = exp(volatility * sqrt(t))
    d = 1 / u
    p = (exp(interest_rate * t) - d) / (u - d)
    option_matrix = np.zeros((steps + 1, steps + 1))
    N_list = np.arange(0, steps + 1)
    S_end = spot_price * np.power(u, steps - N_list) * np.power(d, N_list)

    if option_type == 'call':
        option_matrix[:, -1] = maximum(S_end - strike_price, 0)
    else:
        option_matrix[:, -1] = maximum(strike_price - S_end, 0)

    i_list = list(range(0, steps))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            option_matrix[i, j] = exp(-interest_rate * t) * (p * option_matrix[i + 1, j + 1] + (1 - p) * option_matrix[i + 1, j])
    return option_matrix[0, 0]


# K_same = 4600  # 相同行权价格
# C1 = 224.0  # 较近到期日看涨期权价格
# C2 = 348.0  # 较远到期日看涨期权价格
# S0 = 4584.59  # 策略构建日指数收盘价
# St = np.linspace(3000, 6000, 500)  # 策略到期日指数序列
# N1 = 1  # 较近到期日期权空头数量
# N2 = 1  # 较远到期日期权多头数量
#
# # 计算较近到期日看涨期权空头收益
# profit_C1_short = N1 * M * (C1 - maximum(St - K_same, 0))
#
# # 二叉树计算较远到期日期权价值（2020年12月18日）
# sigma = 0.22  # 年化波动率
# shibor_1218 = 0.02922  # 6个月期Shibor
# T = 0.5  # 剩余期限（年）
# N = 120  # 二叉树步数
# C2_value = BTM_Nstep(S=S0, K=K_same, sigma=sigma, r=shibor_1218, T=T, N=N, types='call')
# profit_C2_long = N2 * M * (maximum(St - K_same, 0) - C2_value)  # 较远到期日看涨期权多头收益
# profit_calendar = profit_C1_short + profit_C2_long  # 日历价差策略收益
#
# # 可视化
# plt.figure(figsize=(9, 6))
# plt.plot(St, profit_C1_short, 'b--', label=u'较近到期日沪深300股指认购期权空头', lw=2.5)
# plt.plot(St, profit_C2_long, 'g--', label=u'较远到期日沪深300股指认购期权多头', lw=2.5)
# plt.plot(St, profit_calendar, 'r-', label=u'日历价差策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与日历价差策略收益的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


# 1. 定义N步二叉树模型计算欧式期权价值的函数
def binomial_tree_model_n_step(spot_price, strike_price, volatility, interest_rate, time_to_maturity, steps, option_type):
    t = time_to_maturity / steps  # 每一步长时期限（年）
    u = exp(volatility * sqrt(t))  # 基础资产价格上涨比例
    d = 1 / u  # 基础资产价格下跌比例
    p = (exp(interest_rate * t) - d) / (u - d)  # 基础资产价格上涨概率
    N_list = range(0, steps + 1)  # 从0到N的自然数序列
    A = []  # 空列表

    for j in N_list:
        # 期权到期日某节点的期权价值
        C_Nj = maximum(spot_price * power(u, j) * power(d, steps - j) - strike_price, 0)
        # 到达该节点的实现路径数量
        Num = factorial(steps) / (factorial(j) * factorial(steps - j))
        A.append(Num * power(p, j) * power(1 - p, steps - j) * C_Nj)  # 列表尾部添加新元素

    call = exp(-interest_rate * time_to_maturity) * sum(A)  # 看涨期权期初价值
    put = call + strike_price * np.exp(-interest_rate * time_to_maturity) - spot_price  # 看跌期权期初价值

    if option_type == 'call':
        value = call
    else:
        value = put
    return value


# # 2. 日历价差策略（看涨期权组合）
# K_same = 4600  # 期权行权价格
# C1 = 224.0  # 较近到期日看涨期权价格
# C2 = 348.0  # 较远到期日看涨期权价格
# S0 = 4584.59  # 策略构建日沪深300指数收盘价
# St = np.linspace(3000, 6000, 500)  # 策略到期日指数序列
# N1 = 1  # 较近到期日期权空头数量
# N2 = 1  # 较远到期日期权多头数量
# M = 100  # 合约乘数（每点100元）
#
# # 较近到期日看涨期权空头收益
# profit_C1_short = N1 * M * (C1 - maximum(St - K_same, 0))
#
# # 计算较远到期日看涨期权价值（二叉树模型）
# tenor = 0.5  # 策略到期日较远到期日期权剩余期限
# sigma_index = 0.22  # 沪深300指数年化波动率
# shibor = 0.02922  # 6个月期Shibor（无风险收益率）
# step = 120  # 二叉树模型步数
# Ct = np.ones_like(St)  # 存放较远到期日看涨期权价值的数组
#
# for i in range(len(Ct)):
#     Ct[i] = BTM_Nstep(S=St[i], K=K_same, sigma=sigma_index, r=shibor, T=tenor, N=step, types='call')
#
# # 较远到期日看涨期权多头收益
# profit_C2_long = N2 * M * (Ct - C2)
# # 日历价差策略收益
# profit_calendarspread = profit_C1_short + profit_C2_long
#
# # 3. 日历价差策略（看跌期权组合）
# K_same = 5000  # 期权行权价格
# P1 = 597.6  # 较近到期日看跌期权价格
# P2 = 746.4  # 较远到期日看跌期权价格
# St = np.linspace(3500, 6500, 500)  # 策略到期日指数序列
#
# # 较近到期日看跌期权空头收益
# profit_P1_short = N1 * M * (P1 - maximum(K_same - St, 0))
#
# # 计算较远到期日看跌期权价值（二叉树模型）
# Pt = np.ones_like(St)  # 存放较远到期日看跌期权价值的数组
# for i in range(len(Pt)):
#     Pt[i] = BTM_Nstep(S=St[i], K=K_same, sigma=sigma_index, r=shibor, T=tenor, N=step, types='put')
#
# # 较远到期日看跌期权多头收益
# profit_P2_long = N2 * M * (Pt - P2)
# # 日历价差策略收益
# profit_calendarspread = profit_P1_short + profit_P2_long
#
# # 可视化
# plt.figure(figsize=(9, 6))
# plt.plot(St, profit_P1_short, 'b--', label=u'较近到期日沪深300股指认沽期权空头', lw=2.5)
# plt.plot(St, profit_P2_long, 'g--', label=u'较远到期日沪深300股指认沽期权多头', lw=2.5)
# plt.plot(St, profit_calendarspread, 'r-', label=u'日历价差策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与日历价差策略收益的关系图', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


'''combination strategy'''
# # 1. 底部跨式组合策略（看涨+看跌期权多头）
# K = 4700  # 期权行权价格
# C = 336.4  # 看涨期权价格
# P = 326.4  # 看跌期权价格
# S0 = 4698.13  # 策略构建日沪深300指数收盘价
# St = np.linspace(3000, 6400, 500)  # 期权到期日指数序列
# N_C = 1  # 看涨期权头寸数量
# N_P = 1  # 看跌期权头寸数量
# M = 100  # 合约乘数（每点100元）
#
# # 计算收益
# profit_C_long = N_C*M * (np.maximum(St-K, 0) - C)  # 看涨期权多头收益
# profit_P_long = N_P*M * (np.maximum(K-St, 0) - P)  # 看跌期权多头收益
# profit_straddle = profit_C_long + profit_P_long  # 底部跨式策略收益
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(St, profit_C_long, 'b--', label=u'沪深300股指认购期权多头', lw=2.5)
# plt.plot(St, profit_P_long, 'g--', label=u'沪深300股指认沽期权多头', lw=2.5)
# plt.plot(St, profit_straddle, 'r-', label=u'底部跨式组合策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与底部跨式组合策略收益的关系图', fontsize=13)
# plt.legend(loc=9, fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 2. 顶部跨式组合策略（看涨+看跌期权空头）
# plt.figure(figsize=(9,6))
# plt.plot(St, -profit_C_long, 'b--', label=u'沪深300股指认购期权空头', lw=2.5)
# plt.plot(St, -profit_P_long, 'g--', label=u'沪深300股指认沽期权空头', lw=2.5)
# plt.plot(St, -profit_straddle, 'r-', label=u'顶部跨式组合策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与顶部跨式组合策略收益的关系图', fontsize=13)
# plt.legend(loc=8, fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 3. 序列组合（Strip）与带式组合（Strap）策略
# K = 4600  # 期权行权价格
# C = 290.0  # 看涨期权价格
# P = 387.0  # 看跌期权价格
# S0 = 4635.71  # 策略构建日指数收盘价
# St = np.linspace(3000, 6200, 500)  # 期权到期日指数序列
# N1 = 1  # 1张期权多头数量
# N2 = 2  # 2张期权多头数量
#
# # 序列组合（1张看涨+2张看跌）
# profit_C_strip = N1*M * (np.maximum(St-K, 0) - C)
# profit_P_strip = N2*M * (np.maximum(K-St, 0) - P)
# profit_strip = profit_C_strip + profit_P_strip
#
# # 带式组合（2张看涨+1张看跌）
# profit_C_strap = N2*M * (np.maximum(St-K, 0) - C)
# profit_P_strap = N1*M * (np.maximum(K-St, 0) - P)
# profit_strap = profit_C_strap + profit_P_strap
#
# # 可视化（子图）
# plt.figure(figsize=(10,6))
# # 子图1：序列组合
# plt.subplot(1,2,1)
# plt.plot(St, profit_C_strip, 'b--', label=u'沪深300股指认购期权（1张）', lw=2.0)
# plt.plot(St, profit_P_strip, 'c--', label=u'沪深300股指认沽期权（2张）', lw=2.0)
# plt.plot(St, profit_strip, 'r-', label=u'序列组合策略', lw=2.0)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与序列组合策略收益的关系图', fontsize=13)
# plt.legend(loc=0, fontsize=12)
# plt.grid()
#
# # 子图2：带式组合
# plt.subplot(1,2,2)
# plt.plot(St, profit_C_strap, 'b--', label=u'沪深300股指认购期权（2张）', lw=2.0)
# plt.plot(St, profit_P_strap, 'c--', label=u'沪深300股指认沽期权（1张）', lw=2.0)
# plt.plot(St, profit_strap, 'r-', label=u'带式组合策略', lw=2.0)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与带式组合策略收益的关系图', fontsize=13)
# plt.legend(loc=0, fontsize=12)
# plt.grid()
# plt.show()
#
#
# # 4. 买入宽跨式组合策略
# # 策略1：K1=4200（看跌）、K2=4900（看涨）
# K1 = 4200
# K2 = 4900
# P = 264.2
# C = 245.0
# S0 = 4581.98
# St = np.linspace(3000, 6100, 500)
# N_P = 1
# N_C = 1
#
# profit_P_long = N_P*M * (np.maximum(K1-St, 0) - P)
# profit_C_long = N_C*M * (np.maximum(St-K2, 0) - C)
# profit_strangle = profit_P_long + profit_C_long
#
# plt.figure(figsize=(9,6))
# plt.plot(St, profit_C_long, 'b--', label=u'沪深300股指认购期权多头', lw=2.5)
# plt.plot(St, profit_P_long, 'g--', label=u'沪深300股指认沽期权多头', lw=2.5)
# plt.plot(St, profit_strangle, 'r-', label=u'买入宽跨式组合策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与买入宽跨式组合策略收益的关系图', fontsize=13)
# plt.legend(loc=9, fontsize=13)
# plt.grid()
# plt.show()
#
# # 策略2：新行权价格（K1=4500、K2=4700）
# K1 = 4500
# K2 = 4700
# P = 417.4
# C = 305.0
#
# profit_P_long = N_P*M * (np.maximum(K1-St, 0) - P)
# profit_C_long = N_C*M * (np.maximum(St-K2, 0) - C)
# profit_strangle = profit_P_long + profit_C_long
#
# plt.figure(figsize=(9,6))
# plt.plot(St, profit_C_long, 'b--', label=u'沪深300股指认购期权多头', lw=2.5)
# plt.plot(St, profit_P_long, 'g--', label=u'沪深300股指认沽期权多头', lw=2.5)
# plt.plot(St, profit_strangle, 'r-', label=u'新的买入宽跨式组合策略', lw=2.5)
# plt.xlabel(u'沪深300指数', fontsize=13)
# plt.ylabel(u'收益金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'沪深300指数与新的买入宽跨式组合策略收益的关系图', fontsize=13)
# plt.legend(loc=9, fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 5. 卖出宽跨式组合策略（英镑兑美元汇率）
# K1 = 1.9  # 较低行权价格
# K2 = 2.0  # 较高行权价格
# C = 0.0104  # 看涨期权价格
# P = 0.0116  # 看跌期权价格
# N_C = 1
# N_P = 1
#
# # 盈亏平衡汇率临界值
# V1 = K1 - P - C
# V2 = K2 + P + C
# print('卖出宽跨式组合策略盈亏平衡的汇率临界值1：', round(V1, 4))
# print('卖出宽跨式组合策略盈亏平衡的汇率临界值2：', round(V2, 4))
#
# # 收益计算
# St = np.linspace(1.6, 2.3, 100)  # 期权到期日汇率序列
# profit_C_short = N_C * (C - np.maximum(St-K2, 0))  # 看涨期权空头收益
# profit_P_short = N_P * (P - np.maximum(K1-St, 0))  # 看跌期权空头收益
# profit_strangle_short = profit_C_short + profit_P_short  # 卖出宽跨式收益
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(St, profit_C_short, 'b--', label=u'英镑看涨期权空头', lw=2.0)
# plt.plot(St, profit_P_short, 'g--', label=u'英镑看跌期权空头', lw=2.0)
# plt.plot(St, profit_strangle_short, 'r-', label=u'卖出宽跨式组合策略', lw=2.5)
# plt.xlabel(u'英镑兑美元汇率', fontsize=13)
# plt.ylabel(u'盈亏金额', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'汇率与卖出宽跨式组合策略盈亏的关系图', fontsize=13)
# # 添加盈亏平衡标注
# plt.annotate(u'盈亏平衡的汇率临界值1', xy=(V1,0.0), xytext=(1.58,-0.01),
#              arrowprops=dict(shrink=0.01), fontsize=13)
# plt.annotate(u'盈亏平衡的汇率临界值2', xy=(V2,0.0), xytext=(2.08,-0.01),
#              arrowprops=dict(shrink=0.01), fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 6. 英镑兑美元汇率走势图（1991年）
# USD_GBP = pd.read_excel(r'英镑兑美元的汇率（1991年）.xlsx',
#                         sheet_name="Sheet1", header=0, index_col=0)
# USD_GBP.index = pd.DatetimeIndex(USD_GBP.index)
#
# plt.figure(figsize=(9,6))
# plt.plot(USD_GBP, 'b-', lw=2.0)
# plt.xlabel(u'日期', fontsize=13)
# plt.ylabel(u'汇率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'英镑兑美元汇率走势图（1991年）', fontsize=13)
# # 添加策略盈亏平衡标注
# plt.annotate(u'1991年3月8日跌破策略盈亏平衡的汇率临界值',
#              xy=('1991-03-08', 1.87), xytext=('1991-04-30', 1.88),
#              arrowprops=dict(shrink=0.01), fontsize=13)
# plt.grid()
# plt.show()