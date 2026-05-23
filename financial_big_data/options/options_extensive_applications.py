import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
from pylab import mpl
from pandas.plotting import register_matplotlib_converters
from scipy.stats import norm
import scipy.optimize as sco
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
register_matplotlib_converters()


'''Merton model(KMV)'''
# # 1. 计算股票年化波动率
# # 导入股价数据（需替换为实际文件路径）
# price_Sun = pd.read_excel(r'超日太阳股票收盘价(2012年8月至2014年2月).xlsx',
#                           sheet_name="Sheet1", header=0, index_col=0)
# return_Sun = np.log(price_Sun / price_Sun.shift(1))  # 日收益率
# sigma_Sun = np.sqrt(252) * np.std(return_Sun)  # 年化波动率
# print('超日太阳股票收益率的年化波动率', round(sigma_Sun, 4))
#
#
# # 2. 计算2014年2月19日企业价值与企业价值年化波动率
# # 输入参数
# equity = 63.85  # 股票市值（亿元）
# debt = 21.90  # 债务金额（亿元）
# tenor = 1  # 债务期限（年）
# rate = 0.050001  # 无风险收益率

# 定义方程组（Merton模型）
def f(x):
    V, sigma_V = x
    # 公式(14-2)：股权价值方程
    d1 = (np.log(V/debt) + (rate + np.power(sigma_V, 2)/2)*tenor) / (sigma_V * np.sqrt(tenor))
    d2 = d1 - sigma_V * np.sqrt(tenor)
    eq1 = V*norm.cdf(d1) - debt*np.exp(-rate*tenor)*norm.cdf(d2) - equity
    # 公式(14-3)：波动率匹配方程
    eq2 = sigma_Sun * equity - norm.cdf(d1) * sigma_V * V
    return [eq1, eq2]

# # 求解方程组
# result = sco.fsolve(func=f, x0=[80, 0.5])  # 初始值：企业价值80亿、波动率50%
# print('计算得到2014年2月19日超日太阳的企业价值（亿元）', round(result[0], 4))
# print('超日太阳企业价值的年化波动率', round(result[1], 4))
#

# 3. 计算违约概率（Merton模型）
def merton_default_probability(exchange_rate, debt_value, asset_value, volatility, interest_rate, time_to_maturity):
    """运用默顿模型计算企业违约概率"""
    d1 = (np.log(asset_value/debt_value) + (interest_rate + np.power(volatility, 2)/2)*time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    PD = norm.cdf(-d2)
    return PD

# PD_Sun = PD_Merton(E=equity, D=debt, V=result[0], sigma=result[1], r=rate, T=tenor)
# print('2014年2月19日超日太阳的违约概率', round(PD_Sun, 6))
#
#
# # 4. 计算2011年12月30日企业价值、波动率及违约概率
# # 输入参数
# equity_new = 70.75  # 股票市值（亿元）
# debt_new = 28.02  # 债务金额（亿元）
# rate_new = 0.052378  # 无风险收益率
# sigma_new = 0.4654  # 股票年化波动率
#
# # 定义方程组
def g(x):
    V, sigma_V = x
    d1 = (np.log(V/debt_new) + (rate_new + np.power(sigma_V, 2)/2)*tenor) / (sigma_V * np.sqrt(tenor))
    d2 = d1 - sigma_V * np.sqrt(tenor)
    eq1 = V*norm.cdf(d1) - debt_new*np.exp(-rate_new*tenor)*norm.cdf(d2) - equity_new
    eq2 = sigma_new * equity_new - norm.cdf(d1) * sigma_V * V
    return [eq1, eq2]

# # 求解方程组
# # result_new = sco.fsolve(func=g, x0=[80, 0.5])
# # print('2011年12月30日超日太阳的企业价值（亿元）', round(result_new[0], 4))
# # print('超日太阳企业价值的年化波动率', round(result_new[1], 4))
# #
# # # 计算违约概率
# # PD_Sun_new = PD_Merton(E=equity_new, D=debt_new, V=result_new[0], sigma=result_new[1], r=rate_new, T=tenor)
# # print('2011年12月30日超日太阳的违约概率', round(PD_Sun_new, 6))
# #
# # # 违约概率倍数
# # M = PD_Sun / PD_Sun_new
# # print('2014年2月19日违约概率与2011年末违约概率的倍数', round(M, 2))


'''convertible bond'''
# # 1. 可转换债券数据可视化
# # 导入数据（需替换为实际文件路径）
# data_CB = pd.read_excel(r'可转换债券数量和存续金额(2010年至2020).xlsx',
#                         sheet_name="Sheet1", header=0, index_col=0)
#
# # 可视化（子图：数量+金额）
# data_CB.plot(kind='bar', subplots=True, layout=(1, 2), figsize=(9, 6), grid=True, fontsize=13)
# plt.subplot(1, 2, 1)
# plt.ylabel(u'数量或金额', fontsize=11)
# plt.show()


# 2. 二又树模型计算可转换债券价值
def value_cb(spot_price, volatility, par_value, confidence_level, lambda_value, interest_rate, rate, quantity_two, time_to_maturity, steps):
    """
    N步二又树模型计算可转换债券价值
    S: 股票初始价格
    sigma: 股票年化波动率
    par: 可转债本金
    X: 转股比例（每份可转债转股数）
    Lambda: 年化违约概率（连续复利）
    r: 无风险收益率
    R: 违约回收率
    Q2: 赎回价格
    T: 可转债期限（年）
    N: 二又树步数
    """
    # 步骤1：计算参数
    t = time_to_maturity / steps  # 每步期限（年）
    u = np.exp(np.sqrt((np.power(volatility, 2) - lambda_value) * t))  # 股价上涨比例
    d = 1 / u  # 股价下跌比例
    Pu = (np.exp(interest_rate * t) - d * np.exp(-lambda_value * t)) / (u - d)  # 股价上涨概率
    Pd = (u * np.exp(-lambda_value * t) - np.exp(interest_rate * t)) / (u - d)  # 股价下跌概率
    P_default = 1 - np.exp(-lambda_value * t)  # 违约概率
    D_value = par_value * rate  # 违约回收价值
    CB_matrix = np.zeros((steps + 1, steps + 1))  # 存储各节点可转债价值的矩阵

    # 步骤2：计算到期节点的可转债价值
    N_list = np.arange(0, steps + 1)
    S_end = spot_price * np.power(u, steps - N_list) * np.power(d, N_list)  # 到期节点股价
    Q1 = par_value  # 到期不转股/不赎回的本金
    Q3 = confidence_level * S_end  # 到期转股价值
    # 到期价值：取（min(本金,赎回价)、转股价值）的最大值
    CB_matrix[:, -1] = np.maximum(np.minimum(Q1, quantity_two), Q3)

    # 步骤3：倒推计算非到期节点的可转债价值
    i_list = list(range(0, steps))
    i_list.reverse()  # 从N-1到0倒推
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = spot_price * np.power(u, i - j) * np.power(d, j)  # 当前节点股价
            # 非违约时的价值（折现后）
            Q1 = np.exp(-interest_rate * t) * (Pu * CB_matrix[i + 1, j + 1] + Pd * CB_matrix[i + 1, j] + P_default * D_value)
            Q3 = confidence_level * Si  # 当前节点转股价值
            # 当前节点价值：取（min(本金,赎回价)、转股价值）的最大值
            CB_matrix[i, j] = np.maximum(np.minimum(Q1, quantity_two), Q3)

    V0 = CB_matrix[0, 0]  # 初始价值
    return V0


# # 3. 计算示例
# # 输入参数
# tenor = 9 / 12  # 期限（9个月）
# S0 = 50  # 股票初始价格
# sigma_A = 0.2  # 股票年化波动率
# par_CB = 100  # 可转债本金
# share = 2  # 转股比例
# Lambda_A = 0.01  # 年化违约概率
# rate = 0.05  # 无风险收益率
# R_A = 0.4  # 违约回收率
# Q2_A = 110  # 赎回价格
#
# # 3步二又树计算
# step1 = 3
# V1_CB = value_CB(S=S0, sigma=sigma_A, par=par_CB, X=share, Lambda=Lambda_A,
#                  r=rate, R=R_A, Q2=Q2_A, T=tenor, N=step1)
# print('运用三步二又树模型计算可转换债券初始价值', round(V1_CB, 4))
#
# # 100步二又树计算
# step2 = 100
# V2_CB = value_CB(S=S0, sigma=sigma_A, par=par_CB, X=share, Lambda=Lambda_A,
#                  r=rate, R=R_A, Q2=Q2_A, T=tenor, N=step2)
# print('运用100步二又树模型计算可转换债券初始价值', round(V2_CB, 4))
#
# # 300步二又树计算
# step3 = 300
# V3_CB = value_CB(S=S0, sigma=sigma_A, par=par_CB, X=share, Lambda=Lambda_A,
#                  r=rate, R=R_A, Q2=Q2_A, T=tenor, N=step3)
# print('运用300步二又树模型计算可转换债券初始价值', round(V3_CB, 4))


'''futures options'''
# 1. 布莱克模型计算欧式期货期权价格
def black_model(forward_price, strike_price, volatility, interest_rate, time_to_maturity, typ):
    """
    布莱克模型计算欧式期货期权价格
    F: 期货合约当前价格
    K: 期权行权价格
    sigma: 期货收益率年化波动率
    r: 无风险收益率
    T: 期权期限（年）
    typ: 期权类型，'call'为看涨，其他为看跌
    """
    d1 = (np.log(forward_price/strike_price) + np.power(volatility, 2)*time_to_maturity/2) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    if typ == 'call':
        price = np.exp(-interest_rate*time_to_maturity) * (forward_price*norm.cdf(d1) - strike_price*norm.cdf(d2))
    else:
        price = np.exp(-interest_rate*time_to_maturity) * (strike_price*norm.cdf(-d2) - forward_price*norm.cdf(-d1))
    return price


# # 2. 黄金期货AU2012期权定价（欧式）
# # 导入黄金期货数据（需替换为实际路径）
# price_AU2012 = pd.read_excel(r'C:/Desktop/黄金期货AU2012合约结算价(2019年11月18日至2020年9月11日).xlsx',
#                              sheet_name="Sheet1", header=0, index_col=0)
# return_AU2012 = np.log(price_AU2012 / price_AU2012.shift(1))  # 日收益率
# Sigma_AU2012 = np.sqrt(252) * np.std(return_AU2012)  # 年化波动率
# print('黄金期货AU2012合约收益率的年化波动率', round(Sigma_AU2012, 4))
#
# # 计算期权期限
# t0 = dt.datetime(2020,9,11)
# t1 = dt.datetime(2020,11,24)
# tenor = (t1 - t0).days / 365  # 剩余期限（年）
#
# # 输入参数
# strike = 380  # 行权价格
# shibor_Sep11 = 0.02697  # 无风险收益率
# price_Sep11 = 420.36  # 期货结算价
#
# # 计算欧式期权价格
# price_call = Black_model(F=price_Sep11, K=strike, sigma=Sigma_AU2012,
#                          r=shibor_Sep11, T=tenor, typ='call')
# price_put = Black_model(F=price_Sep11, K=strike, sigma=Sigma_AU2012,
#                         r=shibor_Sep11, T=tenor, typ='put')
# print('2020年9月11日黄金AU2012购380期权合约（看涨期货期权）的价格', round(price_call, 4))
# print('2020年9月11日黄金AU2012沽380期权合约（看跌期货期权）的价格', round(price_put, 4))
#

# 3. N步二叉树模型计算美式看涨期货期权价格
def american_futures_call_option(forward_price, strike_price, volatility, interest_rate, time_to_maturity, steps):
    """
    N步二叉树计算美式看涨期货期权价格
    F: 期货合约当前价格
    K: 期权行权价格
    sigma: 期货收益率年化波动率
    r: 无风险收益率
    T: 期权期限（年）
    N: 二叉树步数
    """
    t = time_to_maturity / steps  # 每步期限（年）
    u = np.exp(volatility * np.sqrt(t))  # 期货价格上涨比例
    d = 1 / u  # 期货价格下跌比例
    p = (1 - d) / (u - d)  # 上涨概率
    call_matrix = np.zeros((steps+1, steps+1))  # 存储期权价值的矩阵

    # 到期节点价值
    N_list = np.arange(0, steps+1)
    F_end = forward_price * np.power(u, steps - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(F_end - strike_price, 0)

    # 倒推计算非到期节点价值
    i_list = list(range(0, steps))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i+1)
        for j in j_list:
            Fi = forward_price * np.power(u, i - j) * np.power(d, j)
            call_strike = np.maximum(Fi - strike_price, 0)  # 提前行权收益
            # 不提前行权的价值（折现）
            call_nostrike = np.exp(-interest_rate*t) * (p*call_matrix[i+1, j+1] + (1-p)*call_matrix[i+1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)
    return call_matrix[0, 0]


# 4. N步二叉树模型计算美式看跌期货期权价格
def american_futures_put_amer(forward_price, strike_price, volatility, interest_rate, time_to_maturity, steps):
    """
    N步二叉树计算美式看跌期货期权价格
    参数同FutOption_call_Amer
    """
    t = time_to_maturity / steps
    u = np.exp(volatility * np.sqrt(t))
    d = 1 / u
    p = (1 - d) / (u - d)
    put_matrix = np.zeros((steps+1, steps+1))

    # 到期节点价值
    N_list = np.arange(0, steps+1)
    F_end = forward_price * np.power(u, steps - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(strike_price - F_end, 0)

    # 倒推计算非到期节点价值
    i_list = list(range(0, steps))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i+1)
        for j in j_list:
            Fi = forward_price * np.power(u, i - j) * np.power(d, j)
            put_strike = np.maximum(strike_price - Fi, 0)
            put_nostrike = np.exp(-interest_rate*t) * (p*put_matrix[i+1, j+1] + (1-p)*put_matrix[i+1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)
    return put_matrix[0, 0]


# # 5. 豆粕期货M2103期权定价（美式）
# # # 导入豆粕期货数据（需替换为实际路径）
# # price_M2103 = pd.read_excel(r'C:/Desktop/豆粕期货M2103合约结算价(2020年3月16日至11月5日).xlsx',
# #                             sheet_name="Sheet1", header=0, index_col=0)
# # return_M2103 = np.log(price_M2103 / price_M2103.shift(1))
# # Sigma_M2103 = np.sqrt(252) * np.std(return_M2103)
# # print('豆粕期货M2103合约收益率的年化波动率', round(Sigma_M2103, 4))
# #
# # # 输入参数
# # T_3M = 3/12  # 期限（3个月）
# # strike = 3000  # 行权价格
# # shibor_Nov5 = 0.02996  # 无风险收益率
# # price_Nov5 = 3221  # 期货结算价
# # step = 100  # 二叉树步数
# #
# # # 计算美式期权价格
# # value_Amecall = FutOption_call_Amer(F=price_Nov5, K=strike, sigma=Sigma_M2103,
# #                                     r=shibor_Nov5, T=T_3M, N=step)
# # value_Amerput = FutOption_put_Amer(F=price_Nov5, K=strike, sigma=Sigma_M2103,
# #                                    r=shibor_Nov5, T=T_3M, N=step)
# # print('2020年11月5日豆粕M2103购3000期权合约（美式看涨）的价值', round(value_Amecall, 4))
# # print('2020年11月5日豆粕M2103沽3000期权合约（美式看跌）的价值', round(value_Amerput, 4))


'''interest rate options'''
# 1. 计算利率上限单元价值
def caplet(notional_amount, rate, forward_price, strike_rate, volatility, start_time, end_time):
    """
    计算利率上限单元价值
    L: 本金
    R: 无风险收益率（连续复利）
    F: 远期利率
    Rk: 上限利率
    sigma: 远期利率年化波动率
    t1: 重置日时间（年）
    t2: 支付日时间（年）
    """
    d1 = (np.log(forward_price/strike_rate) + 0.5 * np.power(volatility, 2) * start_time) / (volatility * np.sqrt(start_time))
    d2 = d1 - volatility * np.sqrt(start_time)
    tau = end_time - start_time  # 期限长度
    value = notional_amount * tau * np.exp(-rate * end_time) * (forward_price * norm.cdf(d1) - strike_rate * norm.cdf(d2))
    return value


# 2. 计算远期利率
def forward_rate(R1, R2, end_time, T2):
    """
    计算远期利率
    R1: 对应期限T1的零息利率
    R2: 对应期限T2的零息利率
    T1: R1的期限（年）
    T2: R2的期限（年）
    """
    forward_rate = R2 + (R2 - R1) * end_time / (T2 - end_time)
    return forward_rate


# # 3. 导入Shibor数据并计算远期利率
# # 导入数据（需替换为实际路径）
# shibor_list = pd.read_excel(r'C:/Desktop/Shibor(2019年1月至2020年3月20日).xlsx',
#                             sheet_name="Sheet1", header=0, index_col=0)
#
# # 计算各期远期3个月Shibor
# FR1_list = Rf(R1=shibor_list['SHIBOR(3M)'], R2=shibor_list['SHIBOR(6M)'], T1=3/12, T2=6/12)  # 3个月后远期3M
# FR2_list = Rf(R1=shibor_list['SHIBOR(6M)'], R2=shibor_list['SHIBOR(9M)'], T1=6/12, T2=9/12)  # 6个月后远期3M
# FR3_list = Rf(R1=shibor_list['SHIBOR(9M)'], R2=shibor_list['SHIBOR(12M)'], T1=9/12, T2=12/12)  # 9个月后远期3M
#
#
# # 4. 计算远期利率的年化波动率
# return_FR1 = np.log(FR1_list / FR1_list.shift(1))
# return_FR2 = np.log(FR2_list / FR2_list.shift(1))
# return_FR3 = np.log(FR3_list / FR3_list.shift(1))
#
# sigma_FR1 = np.sqrt(252) * return_FR1.std()  # 3个月后远期3M波动率
# sigma_FR2 = np.sqrt(252) * return_FR2.std()  # 6个月后远期3M波动率
# sigma_FR3 = np.sqrt(252) * return_FR3.std()  # 9个月后远期3M波动率
#
# print('3个月后的远期3个月Shibor的年化波动率', round(sigma_FR1, 6))
# print('6个月后的远期3个月Shibor的年化波动率', round(sigma_FR2, 6))
# print('9个月后的远期3个月Shibor的年化波动率', round(sigma_FR3, 6))
#
#
# # 5. 计算2020年3月20日利率上限价值
# # 提取2020年3月20日的远期利率
# FR1_Mar20 = FR1_list.iloc[-1]
# FR2_Mar20 = FR2_list.iloc[-1]
# FR3_Mar20 = FR3_list.iloc[-1]
#
# # 无风险收益率（连续复利）
# R_6M = 0.017049
# R_9M = 0.018499
# R_12M = 0.018682
#
# # 输入参数
# par = 1e8  # 本金
# cap_rate = 0.022  # 上限利率
#
# # 各期利率上限单元价值
# caplet1 = caplet(L=par, R=R_6M, F=FR1_Mar20, Rk=cap_rate, sigma=sigma_FR1, t1=3/12, t2=6/12)
# caplet2 = caplet(L=par, R=R_9M, F=FR2_Mar20, Rk=cap_rate, sigma=sigma_FR2, t1=6/12, t2=9/12)
# caplet3 = caplet(L=par, R=R_12M, F=FR3_Mar20, Rk=cap_rate, sigma=sigma_FR3, t1=9/12, t2=12/12)
#
# # 输出结果
# print('利率重置日2020年6月20日、收益支付日2020年9月20日的利率上限单元价值', round(caplet1, 2))
# print('利率重置日2020年9月20日、收益支付日2020年12月20日的利率上限单元价值', round(caplet2, 2))
# print('利率重置日2020年12月20日、收益支付日2021年3月20日的利率上限单元价值', round(caplet3, 2))
#
# # 总利率上限价值
# cap = caplet1 + caplet2 + caplet3
# print('2020年3月20日利率上限期权的价值', round(cap, 2))
#

# 6. 计算利率下限单元价值
def floorlet(notional_amount, rate, forward_price, strike_rate, volatility, start_time, end_time):
    """
    计算利率下限单元价值
    参数同caplet
    """
    d1 = (np.log(forward_price/strike_rate) + np.power(volatility, 2) * start_time/2) / (volatility * np.sqrt(start_time))
    d2 = d1 - volatility * np.sqrt(start_time)
    tau = end_time - start_time
    value = notional_amount * tau * np.exp(-rate * end_time) * (strike_rate * norm.cdf(-d2) - forward_price * norm.cdf(-d1))
    return value


# # 7. 计算2020年3月20日利率下限价值
# floor_rate = 0.025  # 下限利率
#
# # 各期利率下限单元价值
# floorlet1 = floorlet(L=par, R=R_6M, F=FR1_Mar20, Rk=floor_rate, sigma=sigma_FR1, t1=3/12, t2=6/12)
# floorlet2 = floorlet(L=par, R=R_9M, F=FR2_Mar20, Rk=floor_rate, sigma=sigma_FR2, t1=6/12, t2=9/12)
# floorlet3 = floorlet(L=par, R=R_12M, F=FR3_Mar20, Rk=floor_rate, sigma=sigma_FR3, t1=9/12, t2=12/12)
#
# # 输出结果
# print('利率重置日2020年6月20日、收益支付日2020年9月20日的利率下限单元的价值', round(floorlet1, 2))
# print('利率重置日2020年9月20日、收益支付日2020年12月20日的利率下限单元的价值', round(floorlet2, 2))
# print('利率重置日2020年12月20日、收益支付日2021年3月20日的利率下限单元的价值', round(floorlet3, 2))
#
# # 总利率下限价值
# floor = floorlet1 + floorlet2 + floorlet3
# print('2020年3月20日利率下限期权的价值', round(floor, 2))

# # 1. 利率双限期权价值计算
# # （复用之前定义的caplet、floorlet函数）
# par_new = 1e9  # 本金
# cap_rate_new = 0.029  # 上限利率
# floor_rate_new = 0.023  # 下限利率
#
# # 计算各期利率上限单元价值
# caplet1_new = caplet(L=par_new, R=R_6M, F=FR1_Mar20, Rk=cap_rate_new, sigma=sigma_FR1, t1=3/12, t2=6/12)
# caplet2_new = caplet(L=par_new, R=R_9M, F=FR2_Mar20, Rk=cap_rate_new, sigma=sigma_FR2, t1=6/12, t2=9/12)
# caplet3_new = caplet(L=par_new, R=R_12M, F=FR3_Mar20, Rk=cap_rate_new, sigma=sigma_FR3, t1=9/12, t2=1)
#
# # 计算各期利率下限单元价值
# floorlet1_new = floorlet(L=par_new, R=R_6M, F=FR1_Mar20, Rk=floor_rate_new, sigma=sigma_FR1, t1=3/12, t2=6/12)
# floorlet2_new = floorlet(L=par_new, R=R_9M, F=FR2_Mar20, Rk=floor_rate_new, sigma=sigma_FR2, t1=6/12, t2=9/12)
# floorlet3_new = floorlet(L=par_new, R=R_12M, F=FR3_Mar20, Rk=floor_rate_new, sigma=sigma_FR3, t1=9/12, t2=1)
#
# # 总利率上限、下限价值
# cap_new = caplet1_new + caplet2_new + caplet3_new
# floor_new = floorlet1_new + floorlet2_new + floorlet3_new
# collar_long = cap_new - floor_new
#
# print('2020年3月20日利率双限期权中的利率上限期权价值', round(cap_new, 2))
# print('2020年3月20日利率双限期权中的利率下限期权价值', round(floor_new, 2))
# print('2020年3月20日利率双限期权多头头寸的价值', round(collar_long, 2))
#

# 2. 利率互换期权价值计算
def swaption_price(notional_amount, forward_swap_rate, strike_swap_rate, coupon_frequency, volatility, time_points, n, rate_list, direction):
    """
    计算利率互换期权价值
    L: 本金
    Sf: 远期互换利率
    Sk: 固定利率
    m: 每年支付次数
    sigma: 远期互换利率年化波动率
    t: 期权期限（年）
    n: 互换合约期限（年）
    R_list: 无风险收益率（连续复利）数组
    direction: 'pay'=支付固定利息，其他=收取固定利息
    """
    d1 = (np.log(forward_swap_rate/strike_swap_rate) + np.power(volatility, 2)*time_points/2) / (volatility * np.sqrt(time_points))
    d2 = d1 - volatility * np.sqrt(time_points)
    # 构建支付日期限数组
    T_list = coupon_frequency*time_points + np.arange(1, coupon_frequency*n+1) / coupon_frequency
    if direction == 'pay':
        value = np.sum(np.exp(-rate_list * T_list) * notional_amount * (forward_swap_rate*norm.cdf(d1) - strike_swap_rate*norm.cdf(d2)) / coupon_frequency)
    else:
        value = np.sum(np.exp(-rate_list * T_list) * notional_amount * (strike_swap_rate*norm.cdf(-d2) - forward_swap_rate*norm.cdf(-d1)) / coupon_frequency)
    return value


def forward_swaprate(spot_price_list, time_points, n, coupon_frequency):
    """
    计算远期互换利率
    S_list: 不同期限的互换利率数组
    t: 期权期限（年）
    n: 互换合约期限（年）
    m: 每年支付次数
    """
    t_list = coupon_frequency*time_points + np.arange(1, coupon_frequency*n+1) / coupon_frequency
    # 计算分子
    A = (pow(1+spot_price_list[0]/coupon_frequency, -coupon_frequency*time_points) - pow(1+spot_price_list[-1]/coupon_frequency, -coupon_frequency*(time_points+n)))
    # 计算分母
    B = (1/coupon_frequency) * np.sum(pow(1+spot_price_list[1:]/coupon_frequency, -t_list))
    value = A / B
    return value

#
# # 导入Shibor互换利率数据（需替换为实际路径）
# swaprate_list = pd.read_excel(r'C:/Desktop/Shibor互换利率数据(2019年1月至2020年9月1日).xlsx',
#                               sheet_name="Sheet1", header=0, index_col=0)
#
# # 输入参数
# T_swaption = 0.5  # 期权期限（年）
# T_swap = 0.5  # 互换合约期限（年）
# M = 4  # 每年复利次数（按季）
#
# # 计算每日远期互换利率
# forward_list = np.zeros(len(swaprate_list.index))
# for i in range(len(swaprate_list.index)):
#     forward_list[i] = forward_swaprate(S_list=swaprate_list.iloc[i], t=T_swaption, n=T_swap, m=M)
#
# # 转换为数据框并可视化
# forward_list = pd.DataFrame(data=forward_list, index=swaprate_list.index, columns=['远期互换利率'])
# forward_list.plot(figsize=(9,6), grid=True)
# plt.ylabel(u'利率', fontsize=11)
# plt.show()
#
#
# # 计算远期互换利率的年化波动率
# return_forward = np.log(forward_list / forward_list.shift(1))
# sigma_forward = np.sqrt(252) * return_forward.std()
# sigma_forward = float(sigma_forward)
# print('计算得到远期互换利率的年化波动率', round(sigma_forward, 6))
#
# # 2020年9月1日的远期互换利率
# forward_Sep1 = float(forward_list.iloc[-1])
# print('2020年9月1日的远期互换利率', round(forward_Sep1, 6))
#

# 复利转连续复利
def conversion_rate(market_rate, coupon_frequency):
    """复利利率转连续复利利率"""
    r = coupon_frequency * np.log(1+market_rate/coupon_frequency)
    return r


# # 输入参数
# par = 1e9  # 本金
# rate_fixed = 0.029  # 固定利率
# # 提取2020年9月1日的无风险收益率
# R_norisk = np.array(swaprate_list.iloc[-1])
# # 转换为连续复利
# Rc_norisk = Rc(Rm=R_norisk, m=M)
# Rc_9M_12M = Rc_norisk[:]  # 9个月和1年期无风险收益率
#
# # 计算互换期权价值（收取固定利息）
# value = swaption(L=par, Sf=forward_Sep1, Sk=rate_fixed, m=M, sigma=sigma_forward,
#                  t=T_swaption, n=T_swap, R_list=Rc_9M_12M, direction='receive')
# print('2020年9月1日利率互换期权的价值', round(value, 2))
