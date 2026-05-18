import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from pandas.plotting import register_matplotlib_converters
import scipy.stats as st
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
register_matplotlib_converters()

'''VaR概述'''
# # 计算95%置信水平下的VaR分位数
# x = 0.95  # 置信水平
# z = st.norm.ppf(q=1 - x)  # 正态分布左尾5%的分位数（约为-1.645）
#
# # 生成数据：投资组合盈亏的正态分布序列
# x_seq = np.linspace(-4, 4, 200)  # 盈亏范围（-4到4）
# y_pdf = st.norm.pdf(x_seq)  # 正态分布的概率密度
#
# # 左尾5%的区间（对应VaR区域）
# x1 = np.linspace(-4, z, 100)
# y1 = st.norm.pdf(x1)
#
# # 绘图
# plt.figure(figsize=(9, 6))
# plt.plot(x_seq, y_pdf, 'r-', lw=2.0)  # 绘制正态分布曲线
# plt.fill_between(x1, y1, color='lightblue')  # 填充左尾5%区域
#
# # 图表标注
# plt.xlabel(u'投资组合盈亏', fontsize=13)
# plt.ylabel(u'概率密度', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylim(0, 0.42)
# # 标注VaR位置
# plt.annotate('VaR',
#              xy=(z-0.02, st.norm.pdf(z)+0.005),
#              xytext=(-2.3, 0.17),
#              arrowprops=dict(shrink=0.01),
#              fontsize=13)
# plt.title(u'假定投资组合盈亏服从正态分布的风险价值（VaR）', fontsize=13)
# plt.grid()
# plt.show()


'''Variance-Covariance Method，VCM'''
# 1. 定义方差-协方差法计算VaR的函数
def VaR_VCM(Value, Rp, Vp, X, N):
    """
    方差-协方差法计算风险价值
    Value: 投资组合市值
    Rp: 组合日平均收益率
    Vp: 组合日波动率
    X: 置信水平
    N: 持有期（天）
    """
    z = abs(st.norm.ppf(q=1 - X))  # 正态分布分位数（取绝对值）
    VaR_1day = Value * (z * Vp - Rp)  # 1天VaR
    VaR_Nday = np.sqrt(N) * VaR_1day  # N天VaR（时间平方根法则）
    return VaR_Nday


# # 2. 导入并预处理资产价格数据
# # （需替换为实际文件路径）
# price = pd.read_excel(r'C:/Desktop/投资组合配置资产的每日价格(2018年至2020年).xlsx',
#                       sheet_name="Sheet1", header=0, index_col=0)
# price = price.dropna()  # 删除缺失值
# price.index = pd.DatetimeIndex(price.index)  # 转换索引为日期格式
#
# # 价格归一化并可视化
# (price / price.iloc[0]).plot(figsize=(9, 6), grid=True)
# plt.title("资产价格归一化走势（2018-2020）")
# plt.show()
#
#
# # 3. 计算资产收益率的统计特征
# R = np.log(price / price.shift(1))  # 对数收益率
# R = R.dropna()  # 删除缺失值
#
# # 描述性统计
# print("资产收益率描述性统计：")
# print(R.describe())
#
# # 日平均收益率、日波动率
# R_mean = R.mean()
# print("\n2018年至2020年期间日平均收益率：")
# print(R_mean)
#
# R_vol = R.std()
# print("\n2018年至2020年期间日波动率：")
# print(R_vol)
#
# # 协方差矩阵、相关系数矩阵
# R_cov = R.cov()
# R_corr = R.corr()
# print("\n资产收益率相关系数矩阵：")
# print(R_corr)
#
#
# # 4. 计算投资组合的日收益率、日波动率
# W = np.array([0.15, 0.20, 0.50, 0.05, 0.10])  # 资产权重
# Rp_daily = np.sum(W * R_mean)  # 组合日平均收益率
# print("\n2018年至2020年期间投资组合的日平均收益率：", round(Rp_daily, 6))
#
# Vp_daily = np.sqrt(np.dot(W, np.dot(R_cov, W.T)))  # 组合日波动率
# print("2018年至2020年期间投资组合的日波动率：", round(Vp_daily, 6))
#
#
# # 5. 计算不同场景下的VaR
# value_port = 1e10  # 组合市值（100亿元）
# D1, D2 = 1, 10  # 持有期（1天、10天）
# X1, X2 = 0.95, 0.99  # 置信水平（95%、99%）
#
# # 1天VaR
# VaR95_1day_VCM = VaR_VCM(Value=value_port, Rp=Rp_daily, Vp=Vp_daily, X=X1, N=D1)
# VaR99_1day_VCM = VaR_VCM(Value=value_port, Rp=Rp_daily, Vp=Vp_daily, X=X2, N=D1)
# print("\n方差-协方差法计算持有期为1天、置信水平为95%的风险价值：", round(VaR95_1day_VCM, 2))
# print("方差-协方差法计算持有期为1天、置信水平为99%的风险价值：", round(VaR99_1day_VCM, 2))
#
# # 10天VaR
# VaR95_10day_VCM = VaR_VCM(Value=value_port, Rp=Rp_daily, Vp=Vp_daily, X=X1, N=D2)
# VaR99_10day_VCM = VaR_VCM(Value=value_port, Rp=Rp_daily, Vp=Vp_daily, X=X2, N=D2)
# print("\n方差-协方差法计算持有期为10天、置信水平为95%的风险价值：", round(VaR95_10day_VCM, 2))
# print("方差-协方差法计算持有期为10天、置信水平为99%的风险价值：", round(VaR99_10day_VCM, 2))


'''historical method'''
# # （承接之前的变量：value_port=1e10, W=[0.15,0.20,0.50,0.05,0.10], R为收益率数据框）
# # 1. 计算每个资产的最新市值
# value_past = value_port * W  # 组合市值 × 资产权重
#
# # 2. 模拟投资组合日收益金额
# profit_past = np.dot(R, value_past)  # 每日盈亏=收益率 × 资产市值
# profit_past = pd.DataFrame(
#     data=profit_past,
#     index=R.index,
#     columns=['投资组合的模拟日收益']
# )
#
# # 3. 日收益可视化
# profit_past.plot(figsize=(9, 6), grid=True)
# plt.title("投资组合模拟日收益走势（2018-2020）")
# plt.show()
#
# # 4. 日收益直方图
# plt.figure(figsize=(9, 6))
# plt.hist(
#     np.array(profit_past),
#     bins=30,
#     facecolor='y',
#     edgecolor='k'
# )
# plt.xlabel(u'投资组合的模拟日收益金额', fontsize=13)
# plt.ylabel(u'频数', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'投资组合模拟日收益金额的直方图', fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 5. 收益正态性检验
# print("Kolmogorov-Smirnov检验（正态分布）：")
# print(st.kstest(rvs=profit_past['投资组合的模拟日收益'], cdf='norm'))
#
# print("\nAnderson-Darling检验（正态分布）：")
# print(st.anderson(x=profit_past['投资组合的模拟日收益'], dist='norm'))
#
# print("\nShapiro-Wilk检验（正态分布）：")
# print(st.shapiro(profit_past['投资组合的模拟日收益']))
#
# print("\n正态性检验（normaltest）：")
# print(st.normaltest(profit_past['投资组合的模拟日收益']))
#
#
# # 6. 历史模拟法计算VaR
# X1, X2 = 0.95, 0.99  # 置信水平
# D2 = 10  # 持有期（10天）
#
# # 1天VaR（取历史收益的分位数，绝对值为亏损）
# VaR95_1day_history = np.abs(profit_past.quantile(q=1 - X1))
# VaR99_1day_history = np.abs(profit_past.quantile(q=1 - X2))
#
# VaR95_1day_history = float(VaR95_1day_history)
# VaR99_1day_history = float(VaR99_1day_history)
#
# print("\n历史模拟法计算持有期为1天、置信水平为95%的风险价值：", round(VaR95_1day_history, 2))
# print("历史模拟法计算持有期为1天、置信水平为99%的风险价值：", round(VaR99_1day_history, 2))
#
# # 10天VaR（时间平方根法则）
# VaR95_10day_history = np.sqrt(D2) * VaR95_1day_history
# VaR99_10day_history = np.sqrt(D2) * VaR99_1day_history
#
# print("\n历史模拟法计算持有期为10天、置信水平为95%的风险价值：", round(VaR95_10day_history, 2))
# print("历史模拟法计算持有期为10天、置信水平为99%的风险价值：", round(VaR99_10day_history, 2))


'''Monte Carlo simulation'''
# # （承接之前的变量：value_port=1e10, W=[0.15,0.20,0.50,0.05,0.10], R为收益率数据框）
# # 1. 蒙特卡罗模拟参数配置
# I = 100000  # 模拟次数
# n = 8  # 学生t分布自由度
# X1, X2 = 0.95, 0.99  # 置信水平
# D2 = 10  # 持有期（10天）
#
#
# # 2. 计算资产年化收益率、波动率
# R_mean = R.mean() * 252  # 年化平均收益率
# R_vol = R.std() * np.sqrt(252)  # 年化波动率
# dt = 1/252  # 步长（1个交易日）
#
#
# # 3. 基于学生t分布的蒙特卡罗模拟
# # 从学生t分布抽样
# epsilon = npr.standard_t(df=n, size=I)
#
# # 获取资产最新价格
# P1 = price.iloc[-1, 0]  # 贵州茅台
# P2 = price.iloc[-1, 1]  # 交通银行
# P3 = price.iloc[-1, 2]  # 嘉实增强信用基金
# P4 = price.iloc[-1, 3]  # 华夏恒生ETF
# P5 = price.iloc[-1, -1]  # 博时标普500ETF
#
# # 模拟资产下一个交易日价格（几何布朗运动）
# P1_new = P1 * np.exp((R_mean[0] - 0.5*R_vol[0]**2)*dt + R_vol[0]*epsilon*np.sqrt(dt))
# P2_new = P2 * np.exp((R_mean[1] - 0.5*R_vol[1]**2)*dt + R_vol[1]*epsilon*np.sqrt(dt))
# P3_new = P3 * np.exp((R_mean[2] - 0.5*R_vol[2]**2)*dt + R_vol[2]*epsilon*np.sqrt(dt))
# P4_new = P4 * np.exp((R_mean[3] - 0.5*R_vol[3]**2)*dt + R_vol[3]*epsilon*np.sqrt(dt))
# P5_new = P5 * np.exp((R_mean[-1] - 0.5*R_vol[-1]**2)*dt + R_vol[-1]*epsilon*np.sqrt(dt))
#
# # 计算组合模拟收益
# profit1 = (P1_new/P1 - 1) * value_port * W[0]
# profit2 = (P2_new/P2 - 1) * value_port * W[1]
# profit3 = (P3_new/P3 - 1) * value_port * W[2]
# profit4 = (P4_new/P4 - 1) * value_port * W[3]
# profit5 = (P5_new/P5 - 1) * value_port * W[-1]
# profit_port = profit1 + profit2 + profit3 + profit4 + profit5
#
# # 收益分布直方图
# plt.figure(figsize=(9, 6))
# plt.hist(profit_port, bins=50, facecolor='y', edgecolor='k')
# plt.xlabel(u'投资组合模拟的日收益金额', fontsize=13)
# plt.ylabel(u'频数', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'通过蒙特卡罗模拟（服从学生t分布）得到投资组合日收益金额的直方图', fontsize=13)
# plt.grid()
# plt.show()
#
# # 计算VaR（学生t分布）
# VaR95_1day_MCst = np.abs(np.percentile(a=profit_port, q=(1-X1)*100))
# VaR99_1day_MCst = np.abs(np.percentile(a=profit_port, q=(1-X2)*100))
# print('蒙特卡罗模拟法（服从学生t分布）计算持有期为1天、置信水平为95%的风险价值', round(VaR95_1day_MCst, 2))
# print('蒙特卡罗模拟法（服从学生t分布）计算持有期为1天、置信水平为99%的风险价值', round(VaR99_1day_MCst, 2))
#
# VaR95_10day_MCst = np.sqrt(D2) * VaR95_1day_MCst
# VaR99_10day_MCst = np.sqrt(D2) * VaR99_1day_MCst
# print('蒙特卡罗模拟法（服从学生t分布）计算持有期为10天、置信水平为95%的风险价值', round(VaR95_10day_MCst, 2))
# print('蒙特卡罗模拟法（服从学生t分布）计算持有期为10天、置信水平为99%的风险价值', round(VaR99_10day_MCst, 2))
#
#
# # 4. 基于正态分布的蒙特卡罗模拟
# # 从正态分布抽样
# epsilon_norm = npr.standard_normal(I)
#
# # 模拟资产下一个交易日价格（向量化实现）
# P = np.array(price.iloc[-1])  # 资产最新价格数组
# P_new = np.zeros(shape=(I, len(R_mean)))
# for i in range(len(R_mean)):
#     P_new[:, i] = P[i] * np.exp((R_mean[i] - 0.5*R_vol[i]**2)*dt + R_vol[i]*epsilon_norm*np.sqrt(dt))
#
# # 计算组合模拟收益
# profit_port_norm = (np.dot(P_new/P - 1, W)) * value_port
#
# # 收益分布直方图
# plt.figure(figsize=(9, 6))
# plt.hist(profit_port_norm, bins=30, facecolor='y', edgecolor='k')
# plt.xlabel(u'投资组合模拟的日收益金额', fontsize=13)
# plt.ylabel(u'频数', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'通过蒙特卡罗模拟（服从正态分布）得到投资组合日收益金额的直方图', fontsize=13)
# plt.grid()
# plt.show()
#
# # 计算VaR（正态分布）
# VaR95_1day_MCnorm = np.abs(np.percentile(a=profit_port_norm, q=(1-X1)*100))
# VaR99_1day_MCnorm = np.abs(np.percentile(a=profit_port_norm, q=(1-X2)*100))
# print('\n蒙特卡罗模拟法（服从正态分布）计算持有期为1天、置信水平为95%的风险价值', round(VaR95_1day_MCnorm, 2))
# print('蒙特卡罗模拟法（服从正态分布）计算持有期为1天、置信水平为99%的风险价值', round(VaR99_1day_MCnorm, 2))
#
# VaR95_10day_MCnorm = np.sqrt(D2) * VaR95_1day_MCnorm
# VaR99_10day_MCnorm = np.sqrt(D2) * VaR99_1day_MCnorm
# print('蒙特卡罗模拟法（服从正态分布）计算持有期为10天、置信水平为95%的风险价值', round(VaR95_10day_MCnorm, 2))
# print('蒙特卡罗模拟法（服从正态分布）计算持有期为10天、置信水平为99%的风险价值', round(VaR99_10day_MCnorm, 2))


'''back testing'''

# # （承接之前的变量：profit_past为模拟日收益数据框，VaR95_1day_VCM为95%置信水平1天VaR）
# # 1. 按年度拆分日收益
# profit_2018 = profit_past.loc['2018-01-01':'2018-12-31']
# profit_2019 = profit_past.loc['2019-01-01':'2019-12-31']
# profit_2020 = profit_past.loc['2020-01-01':'2020-12-31']
#
# # 2. 生成每年的VaR亏损阈值数组
# VAR_2018_neg = VaR95_1day_VCM * np.ones_like(profit_2018)
# VAR_2019_neg = VaR95_1day_VCM * np.ones_like(profit_2019)
# VAR_2020_neg = VaR95_1day_VCM * np.ones_like(profit_2020)
#
# # 转换为带日期索引的数据框
# VAR_2018_neg = pd.DataFrame(data=VAR_2018_neg, index=profit_2018.index)
# VAR_2019_neg = pd.DataFrame(data=VAR_2019_neg, index=profit_2019.index)
# VAR_2020_neg = pd.DataFrame(data=VAR_2020_neg, index=profit_2020.index)
#
#
# # 3. 可视化年度收益与VaR阈值
# plt.figure(figsize=(9, 12))
#
# # 2018年子图
# plt.subplot(3, 1, 1)
# plt.plot(profit_2018, 'b-', label=u'2018年投资组合日收益')
# plt.plot(VAR_2018_neg, 'r-', label=u'风险价值对应的亏损', lw=2.0)
# plt.ylabel(u'收益')
# plt.legend(fontsize=12)
# plt.grid()
#
# # 2019年子图
# plt.subplot(3, 1, 2)
# plt.plot(profit_2019, 'b-', label=u'2019年投资组合日收益')
# plt.plot(VAR_2019_neg, 'r-', label=u'风险价值对应的亏损', lw=2.0)
# plt.ylabel(u'收益')
# plt.legend(fontsize=12)
# plt.grid()
#
# # 2020年子图
# plt.subplot(3, 1, 3)
# plt.plot(profit_2020, 'b-', label=u'2020年投资组合日收益')
# plt.plot(VAR_2020_neg, 'r-', label=u'风险价值对应的亏损', lw=2.0)
# plt.xlabel(u'日期')
# plt.ylabel(u'收益')
# plt.legend(fontsize=12)
# plt.grid()
#
# plt.show()
#
#
# # 4. 回测统计：计算亏损超过VaR的天数
# days_2018 = len(profit_2018)
# days_2019 = len(profit_2019)
# days_2020 = len(profit_2020)
# print('2018年的全部交易天数', days_2018)
# print('2019年的全部交易天数', days_2019)
# print('2020年的全部交易天数', days_2020)
#
# # 亏损超过VaR的天数（收益 < -VaR，即亏损 > VaR）
# dayexcept_2018 = len(profit_2018[profit_2018['投资组合的模拟日收益'] < -VaR95_1day_VCM])
# dayexcept_2019 = len(profit_2019[profit_2019['投资组合的模拟日收益'] < -VaR95_1day_VCM])
# dayexcept_2020 = len(profit_2020[profit_2020['投资组合的模拟日收益'] < -VaR95_1day_VCM])
# print('\n2018年超过风险价值对应亏损的天数', dayexcept_2018)
# print('2019年超过风险价值对应亏损的天数', dayexcept_2019)
# print('2020年超过风险价值对应亏损的天数', dayexcept_2020)
#
# # 超过天数的占比
# ratio_2018 = dayexcept_2018 / days_2018
# ratio_2019 = dayexcept_2019 / days_2019
# ratio_2020 = dayexcept_2020 / days_2020
# print('\n2018年超过风险价值对应亏损的天数占全年交易天数的比例', round(ratio_2018, 4))
# print('2019年超过风险价值对应亏损的天数占全年交易天数的比例', round(ratio_2019, 4))
# print('2020年超过风险价值对应亏损的天数占全年交易天数的比例', round(ratio_2020, 4))


'''stress testing'''
# # （承接之前的变量：value_past为各资产市值数组，X1=0.95、X2=0.99为置信水平，D2=10为持有期）
# # 1. 导入并预处理压力期间资产价格数据
# price_stress = pd.read_excel(
#     r'C:/Desktop/投资组合配置资产压力期间的每日价格.xlsx',
#     sheet_name="Sheet1", header=0, index_col=0
# )
# price_stress = price_stress.dropna()  # 删除缺失值
# price_stress.index = pd.DatetimeIndex(price_stress.index)  # 转换索引为日期格式
#
#
# # 2. 计算压力期间的对数收益率
# R_stress = np.log(price_stress / price_stress.shift(1))
# R_stress = R_stress.dropna()  # 清洗缺失值
#
#
# # 3. 计算压力期间组合的日收益金额
# profit_stress = np.dot(R_stress, value_past)  # 收益=收益率 × 资产市值
# profit_stress = pd.DataFrame(
#     data=profit_stress,
#     index=R_stress.index,
#     columns=['投资组合的模拟日收益']
# )
# print("压力期间组合收益的描述性统计：")
# print(profit_stress.describe())
#
#
# # 4. 压力期间收益可视化
# profit_zero = np.zeros_like(profit_stress)  # 收益为0的基准数组
# profit_zero = pd.DataFrame(data=profit_zero, index=profit_stress.index)
#
# plt.figure(figsize=(9, 6))
# plt.plot(profit_stress, 'b-', label=u'压力期间投资组合的日收益')
# plt.plot(profit_zero, 'r-', label=u'收益等于0', lw=2.5)
# plt.xlabel(u'日期', fontsize=13)
# plt.ylabel(u'收益', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'压力期间投资组合的收益表现情况', fontsize=13)
# plt.legend(fontsize=12)
# plt.grid()
# plt.show()
#
#
# # 5. 计算压力风险价值（Stress VaR）
# SVaR95_1day = np.abs(np.percentile(a=profit_stress, q=(1-X1)*100))  # 95%置信水平1天压力VaR
# SVaR99_1day = np.abs(np.percentile(a=profit_stress, q=(1-X2)*100))  # 99%置信水平1天压力VaR
# print('\n持有期为1天、置信水平为95%的压力风险价值', round(SVaR95_1day, 2))
# print('持有期为1天、置信水平为99%的压力风险价值', round(SVaR99_1day, 2))
#
# # 10天压力VaR（时间平方根法则）
# SVaR95_10day = np.sqrt(D2) * SVaR95_1day
# SVaR99_10day = np.sqrt(D2) * SVaR99_1day
# print('\n持有期为10天、置信水平为95%的压力风险价值', round(SVaR95_10day, 2))
# print('持有期为10天、置信水平为99%的压力风险价值', round(SVaR99_10day, 2))


