import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

'''互换市场的概况'''

# # 1. 利率互换交易饼图
# IRS_data = pd.read_excel(
#     r'利率互换交易规模.xls',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# name = IRS_data.index  # 获取利率类型名称
# volume = (np.array(IRS_data)).ravel()  # 转换为一维数组
#
# plt.figure(figsize=(9,7))
# plt.pie(x=volume, labels=name, textprops={'fontsize':13})
# plt.axis('equal')  # 使饼图为正圆形
# plt.show()
#
#
# # 2. 外汇货币掉期成交金额（分币种、期限）
# currency = ['美元与人民币', '非美元外币与人民币']
# volume1 = [158.45, 10.67]
# tenor = ['不超过1年', '超过1年']
# volume2 = [141.29, 27.83]
# plt.figure(figsize=(11,7))
# # 第1张子图：不同交换币种
# plt.subplot(1,2,1)
# plt.pie(x=volume1, labels=currency, textprops={'fontsize':13})
# plt.axis('equal')
# plt.title(u'不同交换币种', fontsize=14)
# # 第2张子图：不同期限
# plt.subplot(1,2,2)
# plt.pie(x=volume2, labels=tenor, textprops={'fontsize':13})
# plt.axis('equal')
# plt.title(u'不同期限', fontsize=14)
# plt.show()
# # 3. 未到期信用风险缓释工具合约面值
# CRM_data = pd.read_excel(
#     r'C:/Desktop/未到期信用风险缓释工具合约面值（2020年年末）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# type_CRM = CRM_data.index  # 获取合约创设机构类型
# par_CRM = (np.array(CRM_data)).ravel()  # 转换为一维数组
#
# plt.figure(figsize=(9,7))
# plt.pie(x=par_CRM, labels=type_CRM, textprops={'fontsize':13})
# plt.axis('equal')
# plt.show()


'''利率互换的计算'''

# # 1. 定义利率互换每期净现金流计算函数
def IRS_cashflow(R_flt, R_fix, L, m, position):
    '''定义一个计算利率互换合约存续期内每期支付净息额的函数
    R_flt: 代表利率互换的每期浮动利率，以数组格式输入；
    R_fix: 代表利率互换的固定利率；
    L: 代表利率互换的本金；
    m: 代表利率互换存续期内每年交换利息的频次；
    position: 代表头寸方向，输入position='long'代表多头（支付固定利息、收取浮动利息），输入其他代表空头（支付浮动利息、收取固定利息）。'''
    if position == 'long':
        # 计算利率互换多头时期的净现金流
        cashflow = (R_flt - R_fix) * L / m
    else:
        # 计算利率互换空头时期的净现金流
        cashflow = (R_fix - R_flt) * L / m
    return cashflow
#
# # 2. 计算A、B银行的每期净息支付额
# rate_float = np.array([0.031970, 0.032000, 0.029823, 0.030771, 0.044510, 0.047093, 0.040340, 0.032750, 0.029630, 0.015660])
# rate_fix = 0.037
# L = 1e8  # 本金
# m = 2  # 每年交换利息的频次
#
# # A银行（多头）的每期利息支付净额
# Netpay_A = IRS_cashflow(R_flt=rate_float, R_fix=rate_fix, L=L, m=m, position="long")
# # B银行（空头）的每期利息支付净额
# Netpay_B = IRS_cashflow(R_flt=rate_float, R_fix=rate_fix, L=L, m=m, position="short")
#
# # 3. 计算利息支付净额的合计数
# Totalpay_A = np.sum(Netpay_A)
# Totalpay_B = np.sum(Netpay_B)
# print('利率互换合约存续期内A银行利息支付净额的合计数', round(Totalpay_A, 2))
# print('利率互换合约存续期内B银行利息支付净额的合计数', round(Totalpay_B, 2))
#
#
# # 4. 定义互换利率计算函数
# def swap_rate(m, y, T):
#     '''定义一个计算互换利率的函数
#     m: 代表利率互换合约存续期内每年交换利息的频次；
#     y: 代表合约初始日对应于每期利息交换期限、连续复利的零息利率，用数组格式输入；
#     T: 代表利率互换的期限（年）。'''
#     n_list = np.arange(1, m*T+1)  # 创建1到mT的整数数组
#     t = n_list / m  # 计算合约初始日距离每期利息交换日的期限数组
#     q = np.exp(-y * t)  # 计算针对不同期限的贴现因子（数组格式）
#     # 计算互换利率
#     rate = (1 - q[-1]) / np.sum(q)
#     return rate
#
# # 5. 计算2020年7月1日的互换利率
# freq = 2  # 每年交换利息的频次
# tenor = 3  # 利率互换的期限
# r_list = np.array([0.020579, 0.021276, 0.022080, 0.022853, 0.023527, 0.024036])  # 对应互换期限的零息利率
#
# R_July1 = swap_rate(m=freq, y=r_list, T=tenor)
# print('2020年7月1日利率互换合约的互换利率', round(R_July1, 4))


'''利率互换的定价'''
import numpy as np
from numpy import exp
import scipy.interpolate as si
import datetime as dt

# 1. 定义利率互换合约价值计算函数
def swap_value(R_fix, R_flt, t, y, m, L, position):
    '''定义一个计算互换合约存续期内利率互换合约价值的函数
    R_fix: 代表合约存续期的固定利率（互换利率）；
    R_flt: 代表距离合约估价日最近的下一期利息交换的浮动利率；
    t: 代表估价日距离各期利息交换日期的期限（年），用数组格式输入；
    y: 代表期限为t并且连续复利的零息利率（贴现利率），用数组格式输入；
    m: 代表利率互换合约每年交换利息的频次；
    L: 代表利率互换合约的本金；
    position: 代表头寸方向，输入position='long'代表多头（支付固定利息、收取浮动利息），输入其他代表空头（支付浮动利息、收取固定利息）。'''
    # 计算固定利率债券价值
    B_fix = (R_fix * sum(exp(-y*t))/m + exp(-y[-1]*t[-1]))*L
    # 计算浮动利率债券价值
    B_flt = (R_flt/m + 1) * exp(-y[0] * t[0]) * L
    if position == 'long':
        # 计算互换利率合约的多头价值
        value = B_flt - B_fix
    else:
        # 计算互换利率合约的空头价值
        value = B_fix - B_flt
    return value
#
#
# # 2. 插值法构建零息利率函数
# # 输入期限数组
# t = np.array([1/12, 2/12, 0.25, 0.5, 0.75, 1.0, 2.0, 3.0])
# # 2020年7月10日已知零息利率
# R_July10 = np.array([0.017219, 0.017526, 0.021012, 0.021100, 0.021764, 0.022165, 0.025040, 0.026994])
# # 2020年7月20日已知零息利率
# R_July20 = np.array([0.016730, 0.018373, 0.019934, 0.020439, 0.021621, 0.022540, 0.024251, 0.025256])
#
# # 构建插值函数（3阶样条曲线）
# func_July10 = si.interp1d(x=t, y=R_July10, kind="cubic")
# func_July20 = si.interp1d(x=t, y=R_July20, kind="cubic")
#
# # 新期限数组（包含1.5年、2.5年）
# t_new = np.array([1/12, 2/12, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0])
# # 插值计算新零息利率
# R_new_July10 = func_July10(t_new)
# R_new_July20 = func_July20(t_new)
#
#
# # 3. 计算各日期距离利息交换日的期限
# # 输入日期
# T1 = dt.datetime(2020, 7, 10)
# T2 = dt.datetime(2020, 7, 20)
# T3 = dt.datetime(2021, 1, 1)  # 下一期利息交换日
#
# # 计算期限（年）
# tenor1 = (T3 - T1).days / 365
# tenor2 = (T3 - T2).days / 365
# T = 3  # 总期限
# M = 2  # 每年交换利息频次
#
# # 2020年7月10日距离各期利息交换日的期限
# T_list1 = np.arange(T*M) / M + tenor1
# # 2020年7月20日距离各期利息交换日的期限
# T_list2 = np.arange(T*M) / M + tenor2
#
#
# # 4. 匹配零息利率数组
# # 2020年7月10日对应的零息利率
# yield_July10 = np.zeros_like(T_list1)
# yield_July10[0] = R_new_July10[3]  # 6个月期
# yield_July10[1:] = R_new_July10[5:]  # 1年、1.5年等期限
#
# # 2020年7月20日对应的零息利率
# yield_July20 = np.zeros_like(T_list2)
# yield_July20[0] = R_new_July20[3]  # 6个月期
# yield_July20[1:] = R_new_July20[5:]  # 1年、1.5年等期限
#
#
# # 5. 计算利率互换合约价值
# rate_fix = 0.0241  # 互换利率
# rate_float = 0.02178  # 浮动利率
# par = 1e8  # 本金
#
# # 2020年7月10日合约价值
# value_July10_long = swap_value(R_fix=rate_fix, R_flt=rate_float, t=T_list1, y=yield_July10, m=M, L=par, position="long")
# value_July10_short = swap_value(R_fix=rate_fix, R_flt=rate_float, t=T_list1, y=yield_July10, m=M, L=par, position="short")
# print('2020年7月10日c银行（多头）的利率互换合约价值', round(value_July10_long, 2))
# print('2020年7月10日d银行（空头）的利率互换合约价值', round(value_July10_short, 2))
#
# # 2020年7月20日合约价值
# value_July20_long = swap_value(R_fix=rate_fix, R_flt=rate_float, t=T_list2, y=yield_July20, m=M, L=par, position="long")
# value_July20_short = swap_value(R_fix=rate_fix, R_flt=rate_float, t=T_list2, y=yield_July20, m=M, L=par, position="short")
# print('2020年7月20日c银行（多头）的利率互换合约价值', round(value_July20_long, 2))
# print('2020年7月20日d银行（空头）的利率互换合约价值', round(value_July20_short, 2))


'''货币互换'''

'''固定换固定'''
import numpy as np

# 1. 定义货币互换双方固定利率现金流计算函数
def CCS_fixed_cashflow(La, Lb, Ra_fix, Rb_fix, m, T, trader, par):
    '''定义一个计算双方固定利率货币互换在存续期间每期现金流的函数
    La: 代表在合约初始日A交易方支付的一种货币本金（合约到期日A交易方收回的货币本金）；
    Lb: 代表在合约初始日A交易方支付的另一种货币本金（合约到期日A交易方收回的货币本金）；
    Ra_fix: 代表基于本金La计算的固定利率；
    Rb_fix: 代表基于本金Lb计算的固定利率；
    m: 代表货币互换合约每年交换利息的频次；
    T: 代表货币互换合约的期限（年）；
    trader: 代表合约的交易方，输入trader='A'表示计算A交易方发生的期间现金流，输入其他则表示计算B交易方发生的期间现金流；
    par: 代表计算现金流所依据的本金，输入par='La'表示计算的现金流基于本金La，输入其他则表示计算的现金流基于本金Lb。'''
    cashflow = np.zeros(m*T + 1)  # 创建存放每期现金流的初始数组
    if par == 'La':
        # 依据本金La计算现金流
        cashflow[0] = La  # 计算A交易方第1期的现金流
        cashflow[1:-1] = Ra_fix * La / m  # 计算A交易方第2期至倒数第2期的现金流
        cashflow[-1] = (Ra_fix / m + 1) * La  # 计算A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow  # 针对B交易方
    else:
        # 依据本金Lb计算现金流
        cashflow[0] = Lb  # 计算A交易方第1期的现金流
        cashflow[1:-1] = Rb_fix * Lb / m  # 计算A交易方第2期至倒数第2期的现金流
        cashflow[-1] = (Rb_fix / m + 1) * Lb  # 计算A交易方最后一期的现金流
        if trader == 'A':
            return -cashflow  # 针对A交易方
        else:
            return cashflow  # 针对B交易方
#
#
# # 2. 输入货币互换参数
# par_RMB = 6.4e8  # E银行支付的人民币本金
# par_USD = 1e8    # E银行支付的美元本金
# rate_RMB = 0.02  # 人民币本金的利率
# rate_USD = 0.01  # 美元本金的利率
# m = 2            # 每年交换利息的频次
# tenor = 5        # 货币互换的期限（年）
#
#
# # 3. 计算E银行的每期现金流
# # E银行基于人民币本金的每期现金流（人民币）
# cashflow_Ebank_RMB = CCS_fixed_cashflow(
#     La=par_RMB, Lb=par_USD, Ra_fix=rate_RMB, Rb_fix=rate_USD,
#     m=m, T=tenor, trader='A', par='La'
# )
# # E银行基于美元本金的每期现金流（美元）
# cashflow_Ebank_USD = CCS_fixed_cashflow(
#     La=par_RMB, Lb=par_USD, Ra_fix=rate_RMB, Rb_fix=rate_USD,
#     m=m, T=tenor, trader='A', par='Lb'
# )
# print('E银行基于人民币本金的每期现金流（人民币）\n', cashflow_Ebank_RMB)
# print('E银行基于美元本金的每期现金流（美元）\n', cashflow_Ebank_USD)
#
#
# # 4. 计算F银行的每期现金流
# # F银行基于人民币本金的每期现金流（人民币）
# cashflow_Fbank_RMB = CCS_fixed_cashflow(
#     La=par_RMB, Lb=par_USD, Ra_fix=rate_RMB, Rb_fix=rate_USD,
#     m=m, T=tenor, trader='B', par='La'
# )
# # F银行基于美元本金的每期现金流（美元）
# cashflow_Fbank_USD = CCS_fixed_cashflow(
#     La=par_RMB, Lb=par_USD, Ra_fix=rate_RMB, Rb_fix=rate_USD,
#     m=m, T=tenor, trader='B', par='Lb'
# )
# print('F银行基于人民币本金的每期现金流（人民币）\n', cashflow_Fbank_RMB)
# print('F银行基于美元本金的每期现金流（美元）\n', cashflow_Fbank_USD)


'''固定换浮动'''
import numpy as np

# 定义货币互换（固定-浮动利率）每期现金流计算函数
def CCS_fixflt_cashflow(La, Lb, Ra_fix, Rb_flt, m, T, trader, par):
    '''定义一个计算双方固定对浮动货币互换在存续期间每期现金流的函数
    La: 代表在合约初始日A交易方支付的一种货币本金（合约到期日A交易方收回的货币本金）；
    Lb: 代表在合约初始日A交易方支付的另一种货币本金（合约到期日A交易方收回的货币本金）；
    Ra_fix: 代表基于本金La的固定利率；
    Rb_flt: 代表基于本金Lb的浮动利率，并且以数组格式输入；
    m: 代表货币互换合约每年交换利息的频次；
    T: 代表货币互换合约的期限（年）；
    trader: 代表合约的交易方，输入trader='A'表示计算A交易方发生的期间现金流，输入其他则表示计算B交易方发生的期间现金流；
    par: 代表计算现金流所依据的本金，输入par='La'表示计算的现金流基于本金La，输入其他则表示计算的现金流基于本金Lb。'''
    cashflow = np.zeros(m*T + 1)  # 创建存放每期现金流的初始数组
    if par == 'La':
        # 依据本金La计算现金流
        cashflow[0] = La  # A交易方第1期的现金流
        cashflow[1:-1] = Ra_fix * La / m  # A交易方第2期至倒数第2期的现金流
        cashflow[-1] = (Ra_fix / m + 1) * La  # A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow  # 针对B交易方
    else:
        # 依据本金Lb计算现金流
        cashflow[0] = Lb  # A交易方第1期的现金流
        cashflow[1:-1] = -Rb_flt[:-1] * Lb / m  # A交易方第2期至倒数第2期的现金流
        cashflow[-1] = -(Rb_flt[-1] / m + 1) * Lb  # A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow  # 针对B交易方


'''浮动换浮动'''
import numpy as np

# 定义货币互换（双方浮动利率）每期现金流计算函数
def CCS_float_cashflow(La, Lb, Ra_flt, Rb_flt, m, T, trader, par):
    '''定义一个计算双方浮动利率货币互换在存续期间每期现金流的函数
    La: 代表在合约初始日A交易方支付的一种货币本金（合约到期日A交易方收回的货币本金）；
    Lb: 代表在合约初始日A交易方支付的另一种货币本金（合约到期日A交易方收回的货币本金）；
    Ra_flt: 代表基于本金La的浮动利率，以数组格式输入；
    Rb_flt: 代表基于本金Lb的浮动利率，以数组格式输入；
    m: 代表货币互换合约每年交换利息的频次；
    T: 代表货币互换合约的期限（年）；
    trader: 代表合约的交易方，输入trader='A'表示计算A交易方的期间现金流，输入其他则计算B交易方的期间现金流；
    par: 代表计算现金流所依据的本金，输入par='La'表示基于本金La，输入其他则基于本金Lb。'''
    cashflow = np.zeros(m*T + 1)  # 创建存放每期现金流的初始数组
    if par == 'La':
        # 依据本金La计算现金流
        cashflow[0] = La  # A交易方第1期的现金流
        cashflow[1:-1] = Ra_flt[:-1] * La / m  # A交易方第2期至倒数第2期的现金流
        cashflow[-1] = (Ra_flt[-1] / m + 1) * La  # A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow  # 针对B交易方
    else:
        # 依据本金Lb计算现金流
        cashflow[0] = Lb  # A交易方第1期的现金流
        cashflow[1:-1] = -Rb_flt[:-1] * Lb / m  # A交易方第2期至倒数第2期的现金流
        cashflow[-1] = -(Rb_flt[-1] / m + 1) * Lb  # A交易方最后一期的现金流
        if trader == 'A':
            return cashflow  # 针对A交易方
        else:
            return -cashflow  # 针对B交易方


# import numpy as np
#
# # 输入货币互换合约参数
# # 第1份货币互换合约
# par_RMB1 = 6.9e8   # 人民币本金
# par_USD = 1e8      # 美元本金
# M1 = 2             # 每年交换利息次数
# T1 = 3             # 期限（年）
# rate_fix = 0.03    # 人民币本金的固定利率
# Libor = np.array([0.012910, 0.014224, 0.016743, 0.024744, 0.028946, 0.025166])  # 美元本金的浮动利率
#
# # 第2份货币互换合约
# par_RMB2 = 1.8e8   # 人民币本金
# par_HKD = 2e8      # 港元本金
# M2 = 1             # 每年交换利息次数
# T2 = 4             # 期限（年）
# Shibor = np.array([0.031600, 0.046329, 0.035270, 0.031220])  # 人民币本金的浮动利率
# Hibor = np.array([0.013295, 0.015057, 0.026593, 0.023743])   # 港元本金的浮动利率
#
#
# # 第1份货币互换合约（固定-浮动）现金流计算
# # G银行的现金流
# cashflow_Gbank_RMB1 = CCS_fixflt_cashflow(
#     La=par_RMB1, Lb=par_USD, Ra_fix=rate_fix, Rb_flt=Libor,
#     m=M1, T=T1, trader='A', par='La'
# )
# cashflow_Gbank_USD = CCS_fixflt_cashflow(
#     La=par_RMB1, Lb=par_USD, Ra_fix=rate_fix, Rb_flt=Libor,
#     m=M1, T=T1, trader='A', par='Lb'
# )
# print('第1份货币互换合约在存续期内G银行的人民币现金流\n', cashflow_Gbank_RMB1)
# print('第1份货币互换合约在存续期内G银行的美元现金流\n', cashflow_Gbank_USD)
#
# # H银行的现金流
# cashflow_Hbank_RMB1 = CCS_fixflt_cashflow(
#     La=par_RMB1, Lb=par_USD, Ra_fix=rate_fix, Rb_flt=Libor,
#     m=M1, T=T1, trader='B', par='La'
# )
# cashflow_Hbank_USD = CCS_fixflt_cashflow(
#     La=par_RMB1, Lb=par_USD, Ra_fix=rate_fix, Rb_flt=Libor,
#     m=M1, T=T1, trader='B', par='Lb'
# )
# print('第1份货币互换合约在存续期内H银行的人民币现金流\n', cashflow_Hbank_RMB1)
# print('第1份货币互换合约在存续期内H银行的美元现金流\n', cashflow_Hbank_USD)
#
#
# # 第2份货币互换合约（双方浮动）现金流计算
# # G银行的现金流
# cashflow_Gbank_RMB2 = CCS_float_cashflow(
#     La=par_RMB2, Lb=par_HKD, Ra_flt=Shibor, Rb_flt=Hibor,
#     m=M2, T=T2, trader='A', par='La'
# )
# cashflow_Gbank_HKD = CCS_float_cashflow(
#     La=par_RMB2, Lb=par_HKD, Ra_flt=Shibor, Rb_flt=Hibor,
#     m=M2, T=T2, trader='A', par='Lb'
# )
# print('第2份货币互换合约在存续期内G银行的人民币现金流\n', cashflow_Gbank_RMB2)
# print('第2份货币互换合约在存续期内G银行的港元现金流\n', cashflow_Gbank_HKD)
#
# # H银行的现金流
# cashflow_Hbank_RMB2 = CCS_float_cashflow(
#     La=par_RMB2, Lb=par_HKD, Ra_flt=Shibor, Rb_flt=Hibor,
#     m=M2, T=T2, trader='B', par='La'
# )
# cashflow_Hbank_HKD = CCS_float_cashflow(
#     La=par_RMB2, Lb=par_HKD, Ra_flt=Shibor, Rb_flt=Hibor,
#     m=M2, T=T2, trader='B', par='Lb'
# )
# print('第2份货币互换合约在存续期内H银行的人民币现金流\n', cashflow_Hbank_RMB2)
# print('第2份货币互换合约在存续期内H银行的港元现金流\n', cashflow_Hbank_HKD)


'''货币互换定价'''
import numpy as np
from numpy import exp
import datetime as dt

# 1. 定义货币互换合约价值计算函数
def CCS_value(types, La, Lb, Ra, Rb, ya, yb, E, m, t, trader):
    '''定义一个计算货币互换合约价值的函数
    types: 代表货币互换类型，输入types='双固定利率货币互换'表示计算双固定利率货币互换，
           输入types='双浮动利率货币互换'表示计算双浮动利率货币互换，输入其他则表示计算固定对浮动货币互换；
           并约定针对固定对浮动货币互换，固定利率针对A货币本金，浮动利率针对B货币本金；
    La: 代表A货币本金；
    Lb: 代表B货币本金；
    Ra: 代表针对A货币本金的利率；
    Rb: 代表针对B货币本金的利率；
    ya: 代表在合约定价日针对A货币本金并对应不同期限、连续复利的零息利率，用数组格式输入；
    yb: 代表在合约定价日针对B货币本金并对应不同期限、连续复利的零息利率，用数组格式输入；
    E: 代表合约定价日的即期汇率，标价方式是1单位B货币对A货币的数量；
    m: 代表每年交换利息的频次；
    t: 代表合约定价日距离剩余每期利息交换日的期限长度，用数组格式输入；
    trader: 代表交易方，输入trader='A'表示A交易方，输入其他则表示B交易方。'''
    if types == '双固定利率货币互换':
        # 计算对应A货币本金的固定利率债券价值
        Bond_A = (Ra * np.sum(exp(-ya * t)) / m + exp(-ya[-1] * t[-1])) * La
        # 计算对应B货币本金的固定利率债券价值
        Bond_B = (Rb * np.sum(exp(-yb * t)) / m + exp(-yb[-1] * t[-1])) * Lb
        if trader == 'A':
            # 计算货币互换合约的价值（以A货币计价）
            swap_value = Bond_A - Bond_B * E
        else:
            # 计算货币互换合约的价值（以B货币计价）
            swap_value = Bond_B - Bond_A / E
    elif types == '双浮动利率货币互换':
        # 计算对应A货币本金的浮动利率债券价值
        Bond_A = (Ra / m + 1) * exp(-ya[0] * t[0]) * La
        # 计算对应B货币本金的浮动利率债券价值
        Bond_B = (Rb / m + 1) * exp(-yb[0] * t[0]) * Lb
        if trader == 'A':
            swap_value = Bond_A - Bond_B * E
        else:
            swap_value = Bond_B - Bond_A / E
    else:
        # 固定对浮动货币互换：A货币固定，B货币浮动
        Bond_A = (Ra * np.sum(exp(-ya * t)) / m + exp(-ya[-1] * t[-1])) * La
        Bond_B = (Rb / m + 1) * exp(-yb[0] * t[0]) * Lb
        if trader == 'A':
            swap_value = Bond_A - Bond_B * E
        else:
            swap_value = Bond_B - Bond_A / E
    return swap_value
#
#
# # 2. 计算货币互换的固定利率（基于swap_rate函数，需提前定义）
# def swap_rate(m, y, T):
#     n_list = np.arange(1, m*T+1)
#     t = n_list / m
#     q = np.exp(-y * t)
#     rate = (1 - q[-1]) / np.sum(q)
#     return rate
#
# y_RMB_April = np.array([0.016778, 0.019062, 0.019821])
# M = 1
# tenor = 3
# rate_RMB = swap_rate(m=M, y=y_RMB_April, T=tenor)
# print('货币互换合约针对人民币本金的固定利率', round(rate_RMB, 4))
#
#
# # 3. 输入货币互换合约参数
# FX_April = 7.0771  # 2020年4月1日美元兑人民币汇率
# par_USD = 1e8      # 美元本金
# par_RMB = par_USD * FX_April  # 人民币本金
# Libor_April = 0.10024  # 2020年4月1日12个月期美元Libor
#
# # 2020年6月18日定价参数
# y_RMB_Jun18 = np.array([0.021156, 0.023294, 0.023811])
# y_USD_Jun18 = np.array([0.0019, 0.0019, 0.00221])
# FX_Jun18 = 7.0903
#
# # 2020年7月20日定价参数
# y_RMB_Jul20 = np.array([0.022540, 0.024251, 0.025256])
# y_USD_Jul20 = np.array([0.0014, 0.0016, 0.0018])
# FX_Jul20 = 6.9928
#
# # 计算定价日距离利息交换日的期限
# t0 = dt.datetime(2020, 4, 1)
# t1 = dt.datetime(2020, 6, 18)
# t2 = dt.datetime(2020, 7, 20)
#
# t1_list = np.arange(1, tenor+1) + (t1 - t0).days / 365
# t2_list = np.arange(1, tenor+1) + (t2 - t0).days / 365
#
#
# # 4. 计算货币互换合约价值
# # 2020年6月18日 J银行（A交易方）、K银行（B交易方）
# value_RMB_Jun18 = CCS_value(
#     types='固定对浮动货币互换', La=par_RMB, Lb=par_USD, Ra=rate_RMB, Rb=Libor_April,
#     ya=y_RMB_Jun18, yb=y_USD_Jun18, E=FX_Jun18, m=M, t=t1_list, trader='A'
# )
# value_USD_Jun18 = CCS_value(
#     types='固定对浮动货币互换', La=par_RMB, Lb=par_USD, Ra=rate_RMB, Rb=Libor_April,
#     ya=y_RMB_Jun18, yb=y_USD_Jun18, E=FX_Jun18, m=M, t=t1_list, trader='B'
# )
#
# # 2020年7月20日 J银行、K银行
# value_RMB_Jul20 = CCS_value(
#     types='固定对浮动货币互换', La=par_RMB, Lb=par_USD, Ra=rate_RMB, Rb=Libor_April,
#     ya=y_RMB_Jul20, yb=y_USD_Jul20, E=FX_Jul20, m=M, t=t2_list, trader='A'
# )
# value_USD_Jul20 = CCS_value(
#     types='固定对浮动货币互换', La=par_RMB, Lb=par_USD, Ra=rate_RMB, Rb=Libor_April,
#     ya=y_RMB_Jul20, yb=y_USD_Jul20, E=FX_Jul20, m=M, t=t2_list, trader='B'
# )
#
# # 输出结果
# print('2020年6月18日J银行的货币互换合约价值（人民币）', round(value_RMB_Jun18, 2))
# print('2020年6月18日K银行的货币互换合约价值（美元）', round(value_USD_Jun18, 2))
# print('2020年7月20日J银行的货币互换合约价值（人民币）', round(value_RMB_Jul20, 2))
# print('2020年7月20日K银行的货币互换合约价值（美元）', round(value_USD_Jul20, 2))


'''CDS'''
import numpy as np
from numpy import exp

# 1. 定义信用违约互换（CDS）现金流计算函数
def CDS_cashflow(S, m, t1, t2, L, recovery, trader, event):
    '''定义一个计算信用违约互换期间现金流的函数
    S: 代表信用违约互换的价差（用于计算信用保护费用）；
    m: 代表信用违约互换每年支付的频次，并且不超过2次；
    t1: 代表合约的期限（年）；
    t2: 代表合约初始日距离信用事件发生日的期限长度（年），信用事件未发生则输入t2='Na'；
    L: 代表合约的本金；
    recovery: 代表信用事件发生时的回收率，信用事件未发生则输入recovery='Na'；
    trader: 代表交易方，输入trader='buyer'表示买方，输入其他则表示卖方；
    event: 代表信用事件，输入event='N'表示合约存续期内信用事件未发生，输入其他则表示合约存续期内信用事件发生。'''
    # 步骤1：合约到期未发生信用事件时计算现金流
    if event == 'N':
        n = int(t1 * m)  # 计算期间现金流支付的次数
        cashflow = S * t1 * np.ones(n) / m  # 合约期间支付的信用保护费用金额的现金流
        if trader == 'buyer':
            CF = -cashflow  # 针对信用保护买方的期间现金流
        else:
            CF = cashflow  # 针对信用保护卖方的期间现金流
    # 步骤2：合约存续期内发生信用事件且每年支付1次
    else:
        default_pay = (1 - recovery) * L  # 信用事件发生时买方支付的赔偿性支付
        if m == 1:
            n = int(t2 * m)  # 计算期间现金流支付的次数
            cashflow = (S * t2 * np.ones(n)) / m  # 计算期间的现金流（最后一个元素后面要调整）
            spread_end = (t2 - int(t2)) * S * L  # 合约最后一期（信用事件发生日）支付的信用保护费用
            cashflow[-1] = spread_end - default_pay  # 合约最后一期的现金流
            if trader == 'buyer':
                CF = cashflow
            else:
                CF = cashflow
    # 步骤3：合约存续期内发生信用事件且每年支付2次
        else:
            if t2 - int(t2) < 0.5:  # 信用事件发生在前半年
                n = int(t2 * m)
                cashflow = (S * t2 * np.ones(n)) / m
                spread_end = (t2 - int(t2)) * S * L
                cashflow[-1] = spread_end - default_pay
            else:  # 信用事件发生在后半年
                n = (int(t2) + 1) * m
                cashflow = (S * t2 * np.ones(n)) / m + 0.5 * S * L
                spread_end = (t2 - int(t2) - 0.5) * S * L
                cashflow[-1] = spread_end - default_pay
            if trader == 'buyer':
                CF = -cashflow
            else:
                CF = cashflow
        return CF
#
#
# # 2. 计算CDS现金流（情形1：未发生信用事件）
# spread = 0.012  # CDS价差
# m = 1           # 每年支付频次
# tenor = 3       # 合约期限
# par = 1e8       # 合约本金
#
# cashflow_buyer1 = CDS_cashflow(
#     S=spread, m=m, t1=tenor, t2='Na', L=par, recovery='Na', trader='buyer', event='N'
# )
# cashflow_seller1 = CDS_cashflow(
#     S=spread, m=m, t1=tenor, t2='Na', L=par, recovery='Na', trader='seller', event='N'
# )
# print('未发生信用事件情形下合约期间买方的现金流', cashflow_buyer1)
# print('未发生信用事件情形下合约期间卖方的现金流', cashflow_seller1)
#
#
# # 3. 计算CDS现金流（情形2：发生信用事件，每年支付1次）
# T_default = 28 / 12  # 初始日距离信用事件发生日的期限（年）
# rate = 0.35          # 回收率
#
# cashflow_buyer2 = CDS_cashflow(
#     S=spread, m=m, t1=tenor, t2=T_default, L=par, recovery=rate, trader='buyer', event='Y'
# )
# cashflow_seller2 = CDS_cashflow(
#     S=spread, m=m, t1=tenor, t2=T_default, L=par, recovery=rate, trader='seller', event='Y'
# )
# print('发生信用事件情形下合约期间买方的现金流', cashflow_buyer2)
# print('发生信用事件情形下合约期间卖方的现金流', cashflow_seller2)
#
#
# # 4. 计算CDS现金流（情形3：发生信用事件，每年支付2次）
# m_new = 2           # 支付频次调整为每年2次
# T_default_new = 32 / 12  # 新的信用事件发生期限
#
# cashflow_buyer3 = CDS_cashflow(
#     S=spread, m=m_new, t1=tenor, t2=T_default_new, L=par, recovery=rate, trader='buyer', event='Y'
# )
# cashflow_seller3 = CDS_cashflow(
#     S=spread, m=m_new, t1=tenor, t2=T_default_new, L=par, recovery=rate, trader='seller', event='Y'
# )
# print('发生信用事件情形下合约期间买方的现金流（新n）', cashflow_buyer3)
# print('发生信用事件情形下合约期间卖方的现金流（新n）', cashflow_seller3)
#
#
# # 5. 计算累积违约概率、存活率、边际违约概率
# h = 0.03  # 连续复利的违约概率
# T = 5     # 期限
# CDP = np.ones(T)  # 存放累积违约概率的数组
# for t in range(1, T+1):
#     CDP[t-1] = 1 - exp(-h * t)  # 计算累积违约概率
# print('累积违约概率（保留4位小数）', CDP.round(4))
#
# SR = 1 - CDP  # 计算存活率
# print('存活率（保留4位小数）', SR.round(4))
#
# MDP = np.ones_like(CDP)  # 存放边际违约概率的数组
# MDP[0] = CDP[0]  # 第1年的边际违约概率
# for t in range(1, T):
#     MDP[t] = SR[t-1] - SR[t]  # 计算第2至第5年的边际违约概率
# print('边际违约概率（保留4位小数）', MDP.round(4))
#
#
# # 6. 定义CDS价差计算函数
# def CDS_spread(m, Lambda, T, R, y):
#     '''定义一个计算信用违约互换价差（年化）的函数
#     m: 代表信用违约互换价差（信用保护费用）每年支付的频次；
#     Lambda: 代表连续复利的年化违约概率；
#     T: 代表合约的期限（年）；
#     R: 代表对应事件发生时的回收率；
#     y: 代表信用合约初始日距离信用保护费用支付的期限且连续复利的零息利率，用数组格式输入。'''
#     t_list = np.arange(1, m*T+1) / m  # 创建期限数组
#     # 计算式(9-31)方括号内的分子
#     A = np.sum(exp(-Lambda * t_list) * exp(-y * t_list))
#     # 计算式(9-31)方括号内的分母
#     B = np.sum((1 - R) * Lambda * exp(-(Lambda + y) * t_list))
#     spread = (1 - R) * (A / B - 1)  # 计算信用违约互换价差
#     return spread
#
#
# # 7. 计算CDS价差
# zero_rate = np.array([0.021276, 0.022853, 0.024036, 0.025010, 0.025976])  # 零息利率
# recovery = 0.4  # 违约回收率
# M = 1           # 每年支付频次
# tenor = 5       # 合约期限
# h = 0.03        # 年化违约概率
#
# spread = CDS_spread(m=M, Lambda=h, T=tenor, R=recovery, y=zero_rate)
# print('计算得到信用违约互换价差', spread.round(4))

'''CDS敏感性分析'''
# import numpy as np
# import matplotlib.pyplot as plt
# from numpy import exp
#
# # （需提前定义CDS_spread函数）
# def CDS_spread(m, Lambda, T, R, y):
#     t_list = np.arange(1, m*T+1) / m
#     A = np.sum(exp(-Lambda * t_list) * exp(-y * t_list))
#     B = np.sum((1 - R) * Lambda * exp(-(Lambda + y) * t_list))
#     spread = (1 - R) * (A / B - 1)
#     return spread
#
#
# # 1. 不同违约概率对应的CDS价差
# h_list = np.linspace(0.01, 0.06, 200)  # 违约概率数组
# spread_list1 = np.zeros_like(h_list)    # 存放对应CDS价差的数组
# M = 1
# tenor = 5
# recovery = 0.4
# zero_rate = np.array([0.021276, 0.022853, 0.024036, 0.025010, 0.025976])
#
# for i in range(len(h_list)):
#     spread_list1[i] = CDS_spread(m=M, Lambda=h_list[i], T=tenor, R=recovery, y=zero_rate)
#
#
# # 2. 不同违约回收率对应的CDS价差
# r_list = np.linspace(0.1, 0.6, 200)    # 违约回收率数组
# spread_list2 = np.zeros_like(r_list)   # 存放对应CDS价差的数组
# h = 0.03
#
# for i in range(len(r_list)):
#     spread_list2[i] = CDS_spread(m=M, Lambda=h, T=tenor, R=r_list[i], y=zero_rate)
#
#
# # 3. 可视化：违约概率、回收率与CDS价差的关系
# plt.figure(figsize=(11,6))
#
# # 子图1：违约概率与CDS价差
# plt.subplot(1,2,1)
# plt.plot(h_list, spread_list1, 'r-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'违约概率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'信用违约互换价差', fontsize=13, rotation=90)
# plt.title(u'违约概率与信用违约互换价差的关系图', fontsize=14)
# plt.grid()
#
# # 子图2：违约回收率与CDS价差（共享y轴）
# plt.subplot(1,2,2, sharey=plt.gca())
# plt.plot(r_list, spread_list2, 'b-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'违约回收率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'违约回收率与信用违约互换价差的关系图', fontsize=14)
# plt.grid()
#
# plt.show()


