import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from pandas.plotting import register_matplotlib_converters
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
register_matplotlib_converters()


'''期货市场概览'''
# # 1. 导入并可视化黄金期货AU2008合约数据
# data_AU2008 = pd.read_excel(
#     r'黄金期货AU2008合约.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# # 可视化（2×2子图布局）
# plt.figure(figsize=(10,9))
# data_AU2008.plot(subplots=True, layout=(2,2), grid=True, fontsize=13)
# plt.subplot(2,2,1)
# plt.ylabel('金额或数量', fontsize=11, position=(0,0))
# plt.show()
#
#
# # 2. 导入并可视化沪深300股指期货IF2009合约数据
# data_IF2009 = pd.read_excel(
#     r'沪深300股指期货IF2009合约.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# # 可视化（2×2子图布局）
# plt.figure(figsize=(10,9))
# data_IF2009.plot(subplots=True, layout=(2,2), grid=True, fontsize=13)
# plt.subplot(2,2,1)
# plt.ylabel('金额或数量', fontsize=11, position=(0,0))
# plt.show()


'''期货价格与现货价格的关系'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

# 配置中文显示
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


# 1. 定义期货理论价格计算函数
def price_futures(S, r, y, u, c, T):
    '''计算期货理论价格的函数
    S: 现货价格
    r: 无风险利率（连续复利）
    y: 便利收益率（连续复利）
    u: 租借利率（期间收益率，连续复利）
    c: 仓储费用
    T: 剩余期限（年）'''
    from numpy import exp
    # 期货理论价格公式：S * exp((r - y + u) * T) + c
    price = S * exp((r - y + u) * T) + c
    return price


# # 2. 计算黄金期货AU2104的理论价格
# spot = 400.53          # 2020年7月15日黄金现货价格
# R_riskfree = 0.02438   # 无风险利率（连续复利）
# y_conv = 0.002         # 便利收益率（连续复利）
# R_lease = 0.005        # 黄金租借利率（连续复利）
# C_storage = 0.438      # 1克黄金的年化仓储费用
# tenor = 9/12           # 期货合约剩余期限（年）
#
# price_AU2104 = price_futures(
#     S=spot, r=R_riskfree, y=y_conv, u=R_lease, c=C_storage, T=tenor
# )
# print('2020年7月15日黄金期货AU2104合约的理论价格', round(price_AU2104, 2))
#
#
# # 3. 模拟不同变量下的期货价格
# # 不同无风险利率
# R_riskfree_list = np.linspace(0.02, 0.03)
# futures_list1 = price_futures(
#     S=spot, r=R_riskfree_list, y=y_conv, u=R_lease, c=C_storage, T=tenor
# )
#
# # 不同便利收益率
# y_conv_list = np.linspace(0.001, 0.004)
# futures_list2 = price_futures(
#     S=spot, r=R_riskfree, y=y_conv_list, u=R_lease, c=C_storage, T=tenor
# )
#
# # 不同租借利率
# R_lease_list = np.linspace(0.002, 0.008)
# futures_list3 = price_futures(
#     S=spot, r=R_riskfree, y=y_conv, u=R_lease_list, c=C_storage, T=tenor
# )
#
# # 不同仓储费用
# C_storage_list = np.linspace(0.3, 1.2)
# futures_list4 = price_futures(
#     S=spot, r=R_riskfree, y=y_conv, u=R_lease, c=C_storage_list, T=tenor
# )
#
#
# # 4. 可视化不同变量与期货价格的关系
# plt.figure(figsize=(10,11))
#
# # 子图1：无风险利率 vs 期货价格
# plt.subplot(2,2,1)
# plt.plot(R_riskfree_list, futures_list1, 'r-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'无风险利率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'期货价格', fontsize=13, rotation=90)
# plt.grid()
#
# # 子图2：便利收益率 vs 期货价格（共享y轴）
# plt.subplot(2,2,2, sharey=plt.gca())
# plt.plot(y_conv_list, futures_list2, 'b-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'便利收益率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.grid()
#
# # 子图3：租借利率 vs 期货价格（共享y轴）
# plt.subplot(2,2,3, sharey=plt.gca())
# plt.plot(R_lease_list, futures_list3, 'c-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'黄金租借利率（期间收益率）', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'期货价格', fontsize=13, rotation=90)
# plt.grid()
#
# # 子图4：仓储费用 vs 期货价格（共享y轴）
# plt.subplot(2,2,4, sharey=plt.gca())
# plt.plot(C_storage_list, futures_list4, 'm-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'仓储费用', fontsize=13)
# plt.yticks(fontsize=13)
# plt.grid()
#
# plt.show()
#
#
# # 5. 导入并可视化黄金期货及现货价格数据
# price_AU2004_AU9995 = pd.read_excel(
#     r'黄金期货AU2004、AU2010合约以及现货价格.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# price_AU2004_AU9995.plot(figsize=(9,6), grid=True, fontsize=13, title=u'期货价格数据性（以黄金期货AU2004合约为例）')
# plt.ylabel(u'金额', fontsize=11)
# plt.show()
#
# price_AU2010_AU9995 = pd.read_excel(
#     r'黄金期货AU2004、AU2010合约以及现货价格.xlsx',
#     sheet_name="Sheet2",
#     header=0,
#     index_col=0
# )
# price_AU2010_AU9995.plot(figsize=(9,6), grid=True, fontsize=13, title=u'期货价格数据性（以黄金期货AU2010合约为例）')
# plt.ylabel(u'金额', fontsize=11)
# plt.show()


'''股指期货的套期保值'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


# # 1. 现货期货套期保值收益计算与可视化
# # 套期保值参数
# fund1 = 2e8       # 购买基金时的基金市值
# index = 4000      # 购买基金时沪深300指数的点位
# N = 100           # 沪深300股指期货的空头数量
# M = 300           # 沪深300股指期货的乘数
#
# # 模拟不同指数点位的收益
# index_list = np.linspace(3500, 4500, 200)
# profit_spot = (index_list - index) * fund1 / index  # 现货投资收益
# profit_future = -(index_list - index) * N * M       # 期货合约收益
# profit_portfolio = profit_spot + profit_future      # 投资组合收益
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.plot(index_list, profit_spot, label=u'沪深300指数ETF基金', lw=2.5)
# plt.plot(index_list, profit_future, label=u'沪深300股指期货合约', lw=2.5)
# plt.plot(index_list, profit_portfolio, label=u'套期保值的投资组合', lw=2.5)
# plt.xlabel(u'沪深300指数点位', fontsize=13)
# plt.ylabel(u'盈亏', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'买卖期货保值的盈亏情况', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 2. 沪深300股指期货IF2007合约盈亏与保证金计算
# # 导入数据
# price_IF2007 = pd.read_excel(
#     r'沪深300股指期货2007合约的结算价(2020年6月19日至7月17日).xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
#
# # 计算参数
# N_short = 1.8e7   # 初始保证金
# margin0 = 0.1     # 合约保证金率
# F0 = 4000         # 成交价格
#
# # 计算累积盈亏
# profit_sum_IF2007 = N_short * (price_IF2007 - F0)
# profit_sum_IF2007 = profit_sum_IF2007.rename(columns={u'IF2007 合约结算价': u'合约累积盈亏'})
#
# # 计算当日盈亏
# profit_daily_IF2007 = profit_sum_IF2007 - profit_sum_IF2007.shift(1)
# profit_daily_IF2007.iloc[0] = profit_sum_IF2007.iloc[0]  # 首个交易日当日盈亏=累积盈亏
# profit_daily_IF2007 = profit_daily_IF2007.rename(columns={u'合约累积盈亏': u'合约当日盈亏'})
#
# # 计算保证金金额
# margin_daily_IF2007 = profit_sum_IF2007 + margin0 * N_short
# margin_daily_IF2007 = margin_daily_IF2007.rename(columns={u'合约累积盈亏': u'保证金余额'})
#
# # 拼接数据
# data_IF2007 = pd.concat([profit_daily_IF2007, profit_sum_IF2007, margin_daily_IF2007], axis=1)
# print("沪深300股指期货IF2007合约盈亏与保证金数据：")
# print(data_IF2007)
#
#
# # 3. 上证50股指期货IH2009合约基差计算与可视化
# # 导入数据
# data_price = pd.read_excel(
#     r'上证50股指期货IH2009合约结算价和上证50指数收盘.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# data_price.index = pd.DatetimeIndex(data_price.index, name=u'日期')  # 转换索引为日期格式
#
# # 计算基差
# basis = data_price[u'上证50期货IH2009合约结算价'] - data_price[u'上证50指数收盘价值']
# print("基差的统计指标：")
# print(basis.describe())
#
# # 基差可视化
# zero_basis = pd.DataFrame(np.zeros_like(basis), index=basis.index)
# plt.figure(figsize=(9,6))
# plt.plot(basis, 'b-', label=u'基差', lw=2.0)
# plt.plot(zero_basis, 'r--', label=u'基差等于0', lw=3.0)
# plt.xlabel(u'日期', fontsize=13)
# plt.ylabel(u'基差', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'上证50股指期货IH2009合约的基差趋势图', fontsize=13)
# plt.legend(fontsize=13, loc=9)
# plt.grid()
# plt.show()


'''最优套保比的计算'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


# # 1. 导入数据并计算日收益率
# fund_future = pd.read_excel(
#     r'上证180指数ETF基金净值和3只A股股指期货合约收盘价数据.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
#
# # 基金日收益率
# R_fund = np.log(fund_future['上证180指数ETF基金'] / fund_future['上证180指数ETF基金'].shift(1))
# R_fund = R_fund.dropna()
#
# # 各期货合约日收益率
# R_IH2009 = np.log(fund_future['IH2009合约'] / fund_future['IH2009合约'].shift(1)).dropna()
# R_IF2009 = np.log(fund_future['IF2009合约'] / fund_future['IF2009合约'].shift(1)).dropna()
# R_IC2009 = np.log(fund_future['IC2009合约'] / fund_future['IC2009合约'].shift(1)).dropna()
#
#
# # 2. 构建基金与各期货的OLS回归模型
# ## （1）基金 vs 上证50期货IH2009
# R_IH2009_addcons = sm.add_constant(R_IH2009)
# model_fund_IH2009 = sm.OLS(R_fund, R_IH2009_addcons).fit()
# print("基金与上证50期货IH2009的回归结果：")
# print(model_fund_IH2009.summary())
#
# ## （2）基金 vs 沪深300期货IF2009
# R_IF2009_addcons = sm.add_constant(R_IF2009)
# model_fund_IF2009 = sm.OLS(R_fund, R_IF2009_addcons).fit()
# print("基金与沪深300期货IF2009的回归结果：")
# print(model_fund_IF2009.summary())
#
# ## （3）基金 vs 中证500期货IC2009
# R_IC2009_addcons = sm.add_constant(R_IC2009)
# model_fund_IC2009 = sm.OLS(R_fund, R_IC2009_addcons).fit()
# print("基金与中证500期货IC2009的回归结果：")
# print(model_fund_IC2009.summary())
#
#
# # 3. 基金与IF2009合约的收益率散点图+拟合线
# cons = model_fund_IF2009.params[0]
# beta = model_fund_IF2009.params[1]
#
# plt.figure(figsize=(9,6))
# plt.scatter(R_IF2009, R_fund, marker='o')  # 散点图
# plt.plot(R_IF2009, cons + beta*R_IF2009, 'r-', lw=2.5)  # 拟合线
# plt.xticks(fontsize=13)
# plt.xlabel(u'沪深300股指期货IF2009合约', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'上证180指数ETF基金', fontsize=13)
# plt.title(u'沪深300股指期货IF2009合约与上证180指数ETF基金的日收益率散点图', fontsize=13)
# plt.grid(True)
# plt.show()


# 4. 计算套期保值最优合约数量
def N_future(h, Q_A, Q_F):
    '''定义计算套期保值最优合约数量的函数
    h: 最优套期比率
    Q_A: 被套期保值资产的数量（或金额）
    Q_F: 1份期货合约的规模（或金额）'''
    N = h * Q_A / Q_F
    return N

# # 输入参数
# share_fund = 5e7       # 购买上证180指数ETF基金的份数
# price_fund = 4.058     # 2020年10月12日基金收盘净值
# value_fund = share_fund * price_fund  # 基金资产金额
#
# price_IF2011 = 4775.6  # 2020年11月12日期货结算价
# M = 300                # 期货合约乘数
# value_IF2011 = price_IF2011 * M  # 1份期货合约规模
#
# h_IF2011 = model_fund_IF2009.params[1]  # IF2011合约的最优套期比率
# N_IF2011 = N_future(h=h_IF2011, Q_A=value_fund, Q_F=value_IF2011)
# print('用于套期保值的沪深300股指期货IF2011合约数量（张）', round(N_IF2011, 0))
#
#
# # 5. 计算套期保值组合的累积盈亏
# N = 17  # 套期保值的期货合约数量
# # 基金净值与期货结算价序列（套期保值首日及后续3个交易日）
# fund_list = np.array([4.0580, 4.0143, 3.9089, 4.0951])
# IF2011_list = np.array([4775.6, 4758.0, 4683.4, 4942.4])
#
# # 计算累积盈亏
# profit_list = share_fund * (fund_list[1:] - fund_list[0]) - N * (IF2011_list[1:] - IF2011_list[0])
# print('2020年10月20日套期保值组合的累积盈亏', round(profit_list[0], 2))
# print('2020年10月30日套期保值组合的累积盈亏', round(profit_list[1], 2))
# print('2020年11月10日套期保值组合的累积盈亏', round(profit_list[2], 2))


'''滚动套保（展期）'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False

# 1. 定义滚动套期保值期货组合盈亏计算函数
def stack_roll(F_open, F_close, M, N, position):
    '''定义计算滚动套期保值期间期货组合盈亏的函数
    F_open: 代表期货的开仓时的期货价格，以数组格式输入
    F_close: 代表期货合约平仓时的期货价格，以数组格式输入
    M: 代表合约乘数
    N: 代表持有期货合约的数量
    position: 代表期货合约的头寸方向，输入position='long'表示多头头寸，输入其他则表示空头头寸'''
    if position == 'long':
        # 多头套期保值，计算每次期货合约移仓的盈亏
        profit_list = (F_close - F_open) * M * N
    else:
        # 空头套期保值，计算每次期货合约移仓的盈亏
        profit_list = (F_open - F_close) * M * N
    # 计算套期保值期间期货合约的盈亏合计
    profit_sum = np.sum(profit_list)
    return profit_sum
#
#
# # 2. 计算滚动套期保值期货组合盈亏
# # 期货开仓、平仓价格数组
# price_open = np.array([3300.00, 3790.60, 3994.00, 3389.00, 3728.00, 3918.20, 3526.81])
# price_close = np.array([3833.40, 4081.29, 3386.46, 3740.14, 3932.45, 3624.55, 4638.20])
#
# # 合约参数
# M_future = 300    # 沪深300股指期货合约乘数
# N_future = 100    # 持有期货合约的数量（空头）
#
# # 计算盈亏合计
# profit_sum = stack_roll(
#     F_open=price_open, F_close=price_close,
#     M=M_future, N=N_future, position='short'
# )
# print('滚动套期保值期间期货移仓盈亏合计数', round(profit_sum, 2))
#
#
# # 3. 可视化每次移仓的盈亏
# # 计算每次移仓的盈亏
# profit_list = (price_open - price_close) * M_future * N_future
# # 转换为列表并添加合计值
# profit_list = list(profit_list)
# profit_list.append(np.sum(profit_list))
#
# # 期货合约名称列表
# name = [
#     'IF1709合约', 'IF1803合约', 'IF1809合约',
#     'IF1903合约', 'IF1909合约', 'IF2003合约',
#     'IF2009合约', '合计'
# ]
#
# # 可视化
# plt.figure(figsize=(9,6))
# plt.barh(name, profit_list, height=0.6, label='期货移仓的盈亏额')
# plt.xticks(fontsize=13)
# plt.xlabel('盈亏额', fontsize=13)
# plt.yticks(fontsize=13)
# plt.title('滚动套期保值期间期货移仓的盈亏', fontsize=13)
# plt.legend(loc=3, fontsize=13)
# plt.grid(True)
# plt.show()


'''国债期货套期保值'''
import numpy as np
import pandas as pd
import datetime as dt
from numpy import exp, power

# 1. 定义应计利息计算函数
def accrued_interest(par, c, m, t1, t2, t3, t4, rule):
    '''定义按照不同计息天数规则计算债券期间应计利息的函数
    par: 债券本金
    c: 债券票面利率
    m: 每年付息频次
    t1: 非参考期间起始日（datetime对象）
    t2: 非参考期间到期日（datetime对象）
    t3: 参考期间起始日（datetime对象）
    t4: 参考期间到期日（datetime对象）
    rule: 计息天数规则（'actual/actual'/'actual/360'/'actual/365'）'''
    d1 = (t2 - t1).days  # 非参考期间天数
    if rule == "actual/actual":
        d2 = (t4 - t3).days  # 参考期间天数
        interest = (d1 / d2) * par * c / m
    elif rule == "actual/360":
        interest = (d1 / 360) * par * c
    else:
        interest = (d1 / 365) * par * c
    return interest

#
# # 2. 计算20附息国债06的应计利息
# par_TB06 = 1e6    # 本金
# C_TB06 = 0.0268   # 票面利率
# m_TB06 = 2        # 每年付息频次
# # 时间参数
# t1_TB06 = dt.datetime(2020, 5, 28)
# t2_TB06 = dt.datetime(2020, 10, 16)
# t3_TB06 = dt.datetime(2020, 5, 21)
# t4_TB06 = dt.datetime(2020, 11, 21)
#
# # 不同规则下的应计利息
# R1_TB06 = accrued_interest(par_TB06, C_TB06, m_TB06, t1_TB06, t2_TB06, t3_TB06, t4_TB06, rule="actual/actual")
# R2_TB06 = accrued_interest(par_TB06, C_TB06, m_TB06, t1_TB06, t2_TB06, t3_TB06, t4_TB06, rule="actual/360")
# R3_TB06 = accrued_interest(par_TB06, C_TB06, m_TB06, t1_TB06, t2_TB06, t3_TB06, t4_TB06, rule="actual/365")
# print("按照“实际天数/实际天数”的规则计算期间利息", round(R1_TB06, 2))
# print("按照“实际天数/360”的规则计算期间利息", round(R2_TB06, 2))
# print("按照“实际天数/365”的规则计算期间利息", round(R3_TB06, 2))


'''债券定价'''

# 3. 定义单一贴现率下的债券定价函数
def Bondprice_onediscount(C, M, m, y, t):
    '''基于单一贴现率计算债券价格的函数
    C: 票面利率（0表示零息债券）
    M: 债券本金（面值）
    m: 每年付息频次
    y: 连续复利到期收益率
    t: 定价日后各付息日的期限（数组格式）'''
    if C == 0:
        price = exp(-y * t) * M  # 零息债券定价
    else:
        coupon = np.ones_like(t) * M * C / m  # 每期利息金额
        NPV_coupon = np.sum(coupon * exp(-y * t))  # 利息现值和
        NPV_par = M * exp(-y * t[-1])  # 本金现值
        price = NPV_coupon + NPV_par  # 全价
    return price


# # 4. 计算20附息国债06的全价、应计利息、净价
# # 时间参数
# t_begin = dt.datetime(2020, 5, 21)
# t_mature = dt.datetime(2030, 5, 21)
# t_pricing = dt.datetime(2020, 8, 6)
# t_next1 = dt.datetime(2020, 11, 21)
#
# # 剩余付息次数与期限数组
# N = (t_mature - t_pricing).days / 365 + 1
# N = int(N * m_TB06)  # 剩余付息次数
# tenor = (t_next1 - t_pricing).days / 365  # 定价日距下一付息日期限
# t_list = np.arange(N) / 2 + tenor  # 剩余付息日距定价日的期限（年）
#
# # 债券定价参数
# bond_par = 100     # 债券本金
# y_TB06 = 0.0301    # 连续复利到期收益率
# # 计算全价
# dirty_price = Bondprice_onediscount(C=C_TB06, M=bond_par, m=m_TB06, y=y_TB06, t=t_list)
# print('2020年8月6日20附息国债06的全价', round(dirty_price, 4))
#
# # 计算应计利息
# bond_interest = accrued_interest(
#     par=bond_par, c=C_TB06, m=m_TB06,
#     t1=t_begin, t2=t_pricing, t3=t_begin, t4=t_next1,
#     rule='actual/actual'
# )
# print('2020年8月6日20附息国债06的应计利息金额', round(bond_interest, 4))
#
# # 计算净价
# clean_price = dirty_price - bond_interest
# print('2020年8月6日20附息国债06的净价', round(clean_price, 4))
#
#
# # 5. 定义可交割债券转换因子计算函数
# def CF(x, n, c, m):
#     '''计算可交割债券转换因子的函数
#     x: 期货交割后至下一付息月的月份数
#     n: 剩余付息次数
#     c: 可交割债券票面利率
#     m: 每年付息次数'''
#     A = 1 / power(1 + 0.03/m, x*m/12)  # 式(10-17)因子式
#     B = c/m + c/0.03/(1 - c/0.03) / power(1 + 0.03/m, n-1)  # 式(10-17)括号内表达式
#     D = c/m * (1 - x/12)  # 式(10-17)括号后因子式
#     value = A * B - D
#     return value
#
#
# # 6. 计算20附息国债06的转换因子
# t_settle1 = dt.datetime(2020, 12, 16)  # 期货最后交割日
# t_next2 = dt.datetime(2021, 5, 21)     # 交割日后下一付息日
# # 交割月至下一付息月的月份数
# months = 12 + (t_next2.month - t_settle1.month)
# # 剩余付息次数
# N2 = (t_mature - t_settle1).days / 365 * m_TB06 + 1
# # 计算转换因子
# CF_TB06 = CF(x=months, n=N2, c=C_TB06, m=m_TB06)
# print('10年期国债期货T2012合约可交割债券20附息国债06的转换因子', round(CF_TB06, 4))
#
#
# # 7. 计算交割日应计利息
# t_settle2 = dt.datetime(2020, 12, 15)  # 第二个交割日
# bond_interest2 = accrued_interest(
#     par=bond_par, c=C_TB06, m=m_TB06,
#     t1=t_next1, t2=t_settle2, t3=t_next1, t4=t_next2,
#     rule="actual/actual"
# )
# print("20附息国债06作为可交割债券的应计利息", round(bond_interest2, 4))


'''最廉价交割的选择'''
# 8. 定义最便宜可交割债券（CTD）成本计算函数
def CTD_cost(price1, price2, CF, name):
    '''计算国债期货可交割债券的交割成本并找出最便宜可交割债券
    price1: 可交割债券净价（数组）
    price2: 期货价格（数组）
    CF: 转换因子（数组）
    name: 可交割债券名称（数组）'''
    cost = price1 - price2 * CF  # 交割成本
    cost = pd.DataFrame(cost, index=name, columns=["交割成本"])
    CTD_bond = cost.idxmin()  # 最便宜可交割债券
    CTD_bond = CTD_bond.rename(index={'交割成本': '最廉价交割债券'})
    return cost, CTD_bond

import pandas as pd
import numpy as np

# （需提前定义CTD_cost函数）
def CTD_cost(price1, price2, CF, name):
    cost = price1 - price2 * CF
    cost = pd.DataFrame(cost, index=name, columns=["交割成本"])
    CTD_bond = cost.idxmin()
    CTD_bond = CTD_bond.rename(index={'交割成本': '最廉价交割债券'})
    return cost, CTD_bond

#
# # 输入3只可交割债券的参数
# price_3bond = np.array([194.9870, 98.6951, 96.1669])  # 净价
# price_T2012 = 97.225  # 国债期货结算价格
# CF_3bond = np.array([10.9739, 1.0101, 0.98841])  # 转换因子
# name_3bond = np.array(['20附息国债06', '19附息国债15', '20抗疫国债04'])  # 债券名称
#
# # 计算交割成本与最便宜可交割债券
# result = CTD_cost(price1=price_3bond, price2=price_T2012, CF=CF_3bond, name=name_3bond)
#
# # 输出结果
# print("3只可交割债券的交割成本：")
# print(result[0])
# print("\n最廉价交割债券：")
# print(result[1])


'''基于久期的套保策略'''
import numpy as np
import datetime as dt
from numpy import exp, ones_like, sum


# 1. 定义国债期货套期保值合约数量计算函数
def N_TBF(PF, par, value, Df, Dp):
    '''计算基于久期套期保值的国债期货合约数量的函数
    PF: 期货价格
    par: 1手国债期货合约基础资产对应的国债面值
    value: 被套期保值投资组合当前市值
    Df: 期货合约基础资产在套期保值到期日的麦考利久期
    Dp: 被套期保值投资组合在套期保值到期日的麦考利久期'''
    value_TBF = PF * par  # 1手国债期货合约的价格
    N = value * Dp / (value_TBF * Df)  # 计算合约数量
    return N


# 2. 定义麦考利久期计算函数
def Mac_Duration(C, M, m, y, t):
    '''计算债券麦考利久期的函数
    C: 债券票面利率
    M: 债券面值
    m: 每年付息频次
    y: 连续复利到期收益率
    t: 定价日后各现金流支付日的期限（数组）'''
    if C == 0:
        duration = t  # 零息债券久期
    else:
        coupon = ones_like(t) * M * C / m  # 每期利息金额
        NPV_coupon = sum(coupon * exp(-y * t))  # 利息现值和
        NPV_par = M * exp(-y * t[-1])  # 本金现值
        Bond_value = NPV_coupon + NPV_par  # 债券价格

        cashflow = coupon
        cashflow[-1] = M * (1 + C / m)  # 最后一期现金流（本息和）
        weight = cashflow * exp(-y * t) / Bond_value  # 时间权重
        duration = sum(t * weight)  # 麦考利久期
    return duration


# # 3. 输入20抗疫国债04的参数
# C_TB04 = 0.0286  # 票面利率
# y_TB04 = 0.0295  # 到期收益率
# m_TB04 = 2  # 每年付息频次
# par_TB04 = 100  # 面值
#
# # 时间参数
# t_T2009 = dt.datetime(2020, 9, 11)  # 期货到期日（套期保值到期日）
# t1_TB04 = dt.datetime(2021, 1, 16)  # 下一付息日
# t2_TB04 = dt.datetime(2030, 7, 16)  # 债券到期日
#
# # 剩余付息次数
# N_TB04 = ((t2_TB04 - t_T2009).days / 365 + 1) * m_TB04
# # 套期保值到期日距下一付息日期限
# tenor = (t1_TB04 - t_T2009).days / 365
# # 剩余现金流支付日的期限数组
# t_list = np.arange(N_TB04) / m_TB04 + tenor
#
# # 计算麦考利久期
# D_TB04 = Mac_Duration(C=C_TB04, M=par_TB04, m=m_TB04, y=y_TB04, t=t_list)
# print('2020年9月11日（套期保值到期日）20抗疫国债04的麦考利久期', round(D_TB04, 4))
#
# # 4. 计算国债期货套期保值合约数量
# par_T2009 = 1e6  # 1手期货对应的国债面值
# price_T2009 = 99.51  # 期货结算价格
# value_fund = 1e9  # 债券投资组合市值
# D_fund = 8.68  # 投资组合麦考利久期
#
# N_T2009 = N_TBF(
#     PF=price_T2009, par=par_T2009,
#     value=value_fund, Df=D_TB04, Dp=D_fund
# )
# print('用于对冲债券投资组合的10年国债期货T2009合约数量', round(N_T2009, 2))


