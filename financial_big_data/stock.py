import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# 读取Excel数据
# index_data = pd.read_excel(
#     r'四只A股市场股指的日收盘价数据（2018-2020）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# # 绘制2×2子图并设置样式
# index_data.plot(subplots=True, layout=(2,2), figsize=(10,10), fontsize=13, grid=True)
# plt.subplot(2,2,1)
# plt.ylabel(u'指数点位', fontsize=11)
# plt.show()


'''零增长估值模型与案例'''
def value_ZGM(D,r):
    '''定义一个运用零增长模型计算股票内在价值的函数
    D: 代表企业已支付的最近一期每股股息金额。
    r: 代表与企业的风险相匹配的贴现利率（每年复利1次）'''
    value = D / r  # 计算股票的内在价值
    return value
# # 招商银行A股的固定股息
# Div = 1.2
# # 贴现利率
# rate = 0.1118
#
# # 计算股票内在价值
# value = value_ZGM(D=Div, r=rate)
# print('运用零增长模型计算招商银行A股股票内在价值', round(value, 4))


'''不变增长估值模型与案例'''
def value_CGM(D,g,r):
    '''定义一个运用不变增长模型计算股票内在价值的函数
    D: 代表企业已支付的最近一期每股股息金额。
    g: 代表企业的股息增长率，并且数值要小于贴现利率。
    r: 代表与企业的风险相匹配的贴现利率（每年复利1次）'''
    if r>g:  # 当贴现利率大于股息增长率
        value = D * (1+g) / (r - g)  # 计算股票内在价值
    else:  # 当贴现利率小于或等于股息增长率
        value = '输入的贴现利率小于或等于股息增长率而导致结果不存在'
    return value
# # 招商银行股息增长率
# growth = 0.1
# Div = 1.2
# rate = 0.1118
# # 计算股票内在价值
# value_new = value_CGM(D=Div, g=growth, r=rate)
# print('运用不变增长模型计算招商银行A股股票的内在价值', round(value_new, 4))


'''二阶段增长估值模型'''
def value_2SGM(D,g1,g2,T,r):
    '''定义一个运用二阶段增长模型计算股票内在价值的函数
    D: 代表企业已支付的最近一期每股股息金额。
    g1: 代表企业在第1个阶段的股息增长率。
    g2: 代表企业在第2个阶段的股息增长率，并且数值要小于贴现利率。
    T: 代表企业第1个阶段的期限，单位是年。
    r: 代表与企业的风险相匹配的贴现利率（每年复利1次）'''
    if r > g2:  # 贴现利率大于第2个阶段的股息增长率
        T_list = np.arange(1, T+1)  # 创建从1到T的整数数列
        # 计算第1个阶段股息贴现之和
        V1 = D * np.sum(np.power(1+g1, T_list) / np.power(1+r, T_list))
        # 计算第2个阶段股息贴现之和
        V2 = D * np.power(1+g1, T) * (1+g2) / (np.power(1+r, T) * (r - g2))
        value = V1 + V2  # 计算股票的内在价值
    else:  # 贴现利率小于或等于第2个阶段的股息增长率
        value = '输入的贴现利率小于或等于第2个阶段的股息增长率而导致结果不存在'
    return value


'''二阶段增长案例'''
# # 第1个阶段的股息增长率
# g_stage1 = 0.11
# # 第2个阶段的股息增长率
# g_stage2 = 0.08
# # 第1个阶段的期限（年）
# T_stage1 = 10
# Div = 1.2
# rate = 0.1118
# # # 计算股票内在价值
# # value_2stages = value_2SGM(D=Div, g1=g_stage1, g2=g_stage2, T=T_stage1, r=rate)
# # print('运用二阶段增长模型计算招商银行A股股票内在价值', round(value_2stages, 4))
# #二阶段模型敏感性分析（g1，g2）
# # 第1个阶段股息增长率的数组
# g1_list = np.linspace(0.06, 0.11, 100)
# # 第2个阶段股息增长率的数组
# g2_list = np.linspace(0.03, 0.08, 100)
#
# # 创建存放对应第1个阶段股息增长率变化的股票内在价值初始数组
# value_list1 = np.zeros_like(g1_list)
# # 运用for语句计算股票内在价值
# for i in range(len(g1_list)):
#     value_list1[i] = value_2SGM(D=Div, g1=g1_list[i], g2=g_stage2, T=T_stage1, r=rate)
#
# # 创建存放对应第2个阶段股息增长率变化的股票内在价值初始数组
# value_list2 = np.zeros_like(g2_list)
# # 运用for语句计算股票内在价值
# for i in range(len(g2_list)):
#     value_list2[i] = value_2SGM(D=Div, g1=g_stage1, g2=g2_list[i], T=T_stage1, r=rate)
#
# # 可视化
# plt.figure(figsize=(11, 6))
#
# # 第1行第1列的子图
# plt.subplot(1, 2, 1)
# plt.plot(g1_list, value_list1, 'r-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'第1个阶段股息增长率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'股票内在价值', fontsize=13, rotation=90)
# plt.title(u'第1个阶段股息增长率与股票内在价值的关系图', fontsize=14)
# plt.grid()
#
# # 第1行第2列的子图（与第1个子图的y轴同刻度）
# plt.subplot(1, 2, 2, sharey=plt.subplot(1, 2, 1))
# plt.plot(g2_list, value_list2, 'b-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'第2个阶段股息增长率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'第2个阶段股息增长率与股票内在价值的关系图', fontsize=14)
# plt.grid()
#
# plt.show()


'''三阶段增长估值模型'''
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


'''三阶段模型案例'''
# # 第1个阶段的股息增长率
# g_stage1 = 0.11
# # 第3个阶段的股息增长率
# g_stage3 = 0.075
# # 第1个阶段的年限
# T_stage1 = 6
# # 第2个阶段的年限
# T_stage2 = 4
# Div = 1.2
# rate = 0.1118
#
# # 计算股票内在价值
# value_3stages = value_3SGM(D=Div, ga=g_stage1, gb=g_stage3, Tr=T_stage1, Tb=T_stage1+T_stage2, r=rate)
# print('运用三阶段增长模型计算招商银行A股股票内在价值', round(value_3stages, 4))

# #三阶段模型敏感性分析
# # 生成各变量的数组
# Div_list = np.linspace(0.8, 1.6, 100)  # 最近一期已支付的股息金额的数组
# rate_list = np.linspace(0.08, 0.12, 100)  # 贴现利率的数组
# ga_list = np.linspace(0.07, 0.11, 100)  # 第1个阶段股息增长率的数组
# gb_list = np.linspace(0.04, 0.08, 100)  # 第3个阶段股息增长率的数组
#
# # 1. 对应不同股息金额的股票内在价值
# value_list1 = np.zeros_like(Div_list)
# for i in range(len(Div_list)):
#     value_list1[i] = value_3SGM(D=Div_list[i], ga=g_stage1, gb=g_stage3, Tr=T_stage1, Tb=T_stage1+T_stage2, r=rate)
#
# # 2. 对应不同贴现利率的股票内在价值
# value_list2 = np.zeros_like(rate_list)
# for i in range(len(rate_list)):
#     value_list2[i] = value_3SGM(D=Div, ga=g_stage1, gb=g_stage3, Tr=T_stage1, Tb=T_stage1+T_stage2, r=rate_list[i])
#
# # 3. 对应第1个阶段不同股息增长率的股票内在价值
# value_list3 = np.zeros_like(ga_list)
# for i in range(len(ga_list)):
#     value_list3[i] = value_3SGM(D=Div, ga=ga_list[i], gb=g_stage3, Tr=T_stage1, Tb=T_stage1+T_stage2, r=rate)
#
# # 4. 对应第3个阶段不同股息增长率的股票内在价值
# value_list4 = np.zeros_like(gb_list)
# for i in range(len(gb_list)):
#     value_list4[i] = value_3SGM(D=Div, ga=g_stage1, gb=gb_list[i], Tr=T_stage1, Tb=T_stage1+T_stage2, r=rate)
#
# # 可视化（2×2子图）
# plt.figure(figsize=(10, 11))
#
# # 第1行第1列：股息金额与内在价值
# plt.subplot(2, 2, 1)
# plt.plot(Div_list, value_list1, 'r-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'最近一期已支付的股息金额', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'股票内在价值', fontsize=13, rotation=90)
# plt.grid()
#
# # 第1行第2列：贴现利率与内在价值
# plt.subplot(2, 2, 2)
# plt.plot(rate_list, value_list2, 'b-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'贴现利率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.grid()
#
# # 第2行第1列：第1阶段股息增长率与内在价值
# plt.subplot(2, 2, 3)
# plt.plot(ga_list, value_list3, 'r-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'第1个阶段股息增长率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'股票内在价值', fontsize=13, rotation=90)
# plt.grid()
#
# # 第2行第2列：第3阶段股息增长率与内在价值
# plt.subplot(2, 2, 4)
# plt.plot(gb_list, value_list4, 'b-', lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'第3个阶段股息增长率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.grid()
#
# plt.show()


'''股票价格波动的随机过程：几何布朗运动'''

# # 第1步：导入数据并计算平均年化收益率、年化波动率
# S = pd.read_excel(
#     r'招商银行A股日收盘价数据（2018-2020年）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# R = np.log(S / S.shift(1))  # 计算日收益率
# mu = R.mean() * 252  # 计算平均年化收益率
# mu = float(mu)
# print('招商银行A股平均年化收益率', round(mu, 6))
#
# sigma = R.std() * np.sqrt(252)  # 计算年化波动率
# sigma = float(sigma)
# print('招商银行A股年化波动率', round(sigma, 6))
#
# # 第2步：设置模拟参数并创建时间序列
# import numpy.random as npr
#
# # 创建2021-01-04至2023-12-31的工作日序列
# date = pd.date_range(start='2021-01-04', end='2023-12-31', freq='B')
# N = len(date)  # 时间序列长度
# I = 500  # 模拟路径数量
#
# dt = 1.0 / 252  # 单日时间长度
# S_GBM = np.zeros((N, I))  # 初始化未来股价数组
# S_GBM[0] = 43.17  # 模拟起点（2021-01-04收盘价）
#
# # 模拟未来每个工作日的股价
# for t in range(1, N):
#     epsilon = npr.standard_normal(I)  # 基于标准正态分布的随机抽样
#     # 几何布朗运动公式计算股价
#     S_GBM[t] = S_GBM[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * epsilon * np.sqrt(dt))
#
# # 转换为带时间索引的数据框
# S_GBM = pd.DataFrame(S_GBM, index=date)
#
# # 显示数据框的开头5行
# print(S_GBM.head())
#
# # 显示数据框的末尾5行
# print(S_GBM.tail())
#
# # 显示数据框的描述性统计指标
# print(S_GBM.describe())
#
# import matplotlib.pyplot as plt
#
# # 所有模拟路径可视化
# plt.figure(figsize=(9,6))
# plt.plot(S_GBM)
# plt.xlabel(u'日期', fontsize=13)
# plt.ylabel(u'招商银行股价', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'2021-2023年服从几何布朗运动的股价模拟路径', fontsize=13)
# plt.grid()
# plt.show()
#
# # 前20条模拟路径可视化
# plt.figure(figsize=(9,6))
# plt.plot(S_GBM.iloc[:, :20])
# plt.xlabel(u'日期', fontsize=13)
# plt.ylabel(u'招商银行股价', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'2021-2023年服从几何布朗运动的股价的前20条模拟路径', fontsize=13)
# plt.grid()
# plt.show()


'''构建最优投资组合'''

# #导入数据
# data_stocks = pd.read_excel(
#     r'5只A股股票的收盘价（2018年至2020年）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
#
# # 股价归一化并可视化
# (data_stocks / data_stocks.iloc[0]).plot(figsize=(9,6), grid=True)
# plt.show()
#
# # 计算对数收益率
# R = np.log(data_stocks / data_stocks.shift(1))
#
# # 输出描述性统计指标
# print(R.describe())
#
# # 收益率直方图
# R.hist(bins=40, figsize=(9,11))
# plt.show()
#
# # 计算年化波动率
# R_vol = R.std() * np.sqrt(252)
# print(R_vol)
#
# # 计算年化协方差矩阵
# R_cov = R.cov() * 252
# print(R_cov)
#
# # 计算相关系数矩阵
# R_corr = R.corr()
# print(R_corr)
#
# # 计算等权重投资组合的预期收益率与波动率
# n = 5  # 个股数量
# w = np.ones(n) / n  # 等权重数组
# print(w)
#
# R_mean = R.mean() * 252  # 个股年化预期收益率
# R_port = np.sum(w * R_mean)  # 组合年化预期收益率
# print('投资组合年化的预期收益率', round(R_port, 4))
#
# vol_port = np.sqrt(np.dot(w, np.dot(R_cov, w.T)))  # 组合年化波动率
# print('投资组合年化的波动率', round(vol_port, 4))
#
#
# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.optimize as sco
#
# # 1. 随机权重组合的收益与波动率模拟
# I = 2000
# Rp_list = np.ones(I)
# Vp_list = np.ones(I)
#
# for i in np.arange(I):
#     x = np.random.rand(n)
#     weights = x / sum(x)
#     Rp_list[i] = np.sum(weights * R_mean)
#     Vp_list[i] = np.sqrt(np.dot(weights, np.dot(R_cov, weights.T)))
#
# # 可视化随机组合的收益-波动率
# plt.figure(figsize=(9,6))
# plt.scatter(Vp_list, Rp_list)
# plt.xlabel(u'波动率', fontsize=13)
# plt.ylabel(u'预期收益率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'投资组合预期收益率与波动率的关系图', fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 2. 定义目标函数与约束
# def f(w):
#     w = np.array(w)
#     Rp_opt = np.sum(w * R_mean)
#     Vp_opt = np.sqrt(np.dot(w, np.dot(R_cov, w.T)))
#     return np.array([Rp_opt, Vp_opt])
#
# def Vmin_f(w):
#     return f(w)[1]
#
#
# # 3. 目标收益15%对应的最小波动率组合
# cons = (
#     {'type': 'eq', 'fun': lambda x: np.sum(x)-1},
#     {'type': 'eq', 'fun': lambda x: f(x)[0]-0.15}
# )
# bnds = ((0,1), (0,1), (0,1), (0,1), (0,1))
# w0 = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
#
# result = sco.minimize(fun=Vmin_f, x0=w0, method='SLSQP', bounds=bnds, constraints=cons)
# print('投资组合预期收益率15%对应投资组合的波动率', round(result['fun'],4))
# print('投资组合预期收益率15%对应长江电力的权重', round(result['x'][0],4))
# print('投资组合预期收益率15%对应平安银行的权重', round(result['x'][1],4))
# print('投资组合预期收益率15%对应上海机场的权重', round(result['x'][2],4))
# print('投资组合预期收益率15%对应中信证券的权重', round(result['x'][3],4))
# print('投资组合预期收益率15%对应顺丰控股的权重', round(result['x'][4],4))
#
#
# # 4. 全局最小波动率组合
# cons_min = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
# result_min = sco.minimize(fun=Vmin_f, x0=w0, method='SLSQP', bounds=bnds, constraints=cons_min)
# Vp_min = result_min['fun']
# print('在可行集上属于全局最小值的波动率', round(Vp_min,4))
#
# Rp_min = np.sum(R_mean * result_min['x'])
# print('全局最小值的波动率对应投资组合的预期收益率', round(Rp_min,4))
# print('全局最小值的波动率对应长江电力的权重', round(result_min['x'][0],4))
# print('全局最小值的波动率对应平安银行的权重', round(result_min['x'][1],4))
# print('全局最小值的波动率对应上海机场的权重', round(result_min['x'][2],4))
# print('全局最小值的波动率对应中信证券的权重', round(result_min['x'][3],4))
# print('全局最小值的波动率对应顺丰控股的权重', round(result_min['x'][4],4))
#
#
# # 5. 有效前沿绘制
# Rp_target = np.linspace(Rp_min, 0.3, 200)
# Vp_target = []
# for r in Rp_target:
#     cons_new = (
#         {'type': 'eq', 'fun': lambda x: np.sum(x)-1},
#         {'type': 'eq', 'fun': lambda x: f(x)[0]-r}
#     )
#     result_new = sco.minimize(fun=Vmin_f, x0=w0, method='SLSQP', bounds=bnds, constraints=cons_new)
#     Vp_target.append(result_new['fun'])
#
# plt.figure(figsize=(9,6))
# plt.scatter(Vp_list, Rp_list)
# plt.plot(Vp_target, Rp_target, 'r-', label=u'有效前沿', lw=2.5)
# plt.plot(Vp_min, Rp_min, 'g*', label=u'全局最小波动率', markersize=13)
# plt.xlabel(u'波动率', fontsize=13)
# plt.ylabel(u'预期收益率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.xlim(0.15, 0.3)
# plt.ylim(0.06, 0.22)
# plt.title(u'投资组合的有效前沿', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 6. 资本市场线（CML）
# Rf = 0.0385  # 无风险利率
# def F(w):
#     w = np.array(w)
#     Rp_opt = np.sum(w * R_mean)
#     Vp_opt = np.sqrt(np.dot(w, np.dot(R_cov, w.T)))
#     slope = (Rp_opt - Rf) / Vp_opt
#     return np.array([Rp_opt, Vp_opt, slope])
#
# def Slope_F(w):
#     return -F(w)[2]
#
# cons_Slope = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
# result_Slope = sco.minimize(fun=Slope_F, x0=w0, method='SLSQP', bounds=bnds, constraints=cons_Slope)
# Slope = -result_Slope['fun']
# print('资本市场线的斜率', round(Slope,4))
#
# wm = result_Slope['x']
# print('市场组合配置的长江电力的权重', round(wm[0],4))
# print('市场组合配置的平安银行的权重', round(wm[1],4))
# print('市场组合配置的上海机场的权重', round(wm[2],4))
# print('市场组合配置的中信证券的权重', round(wm[3],4))
# print('市场组合配置的顺丰控股的权重', round(wm[4],4))
#
# Em = np.sum(R_mean * wm)
# Vm = (Em - Rf) / Slope
# print('市场组合的预期收益率', round(Em,4))
# print('市场组合的波动率', round(Vm,4))
#
#
# # 7. 资本市场线可视化
# Rp_CML = np.linspace(Rf, 0.25, 200)
# Vp_CML = (Rp_CML - Rf) / Slope
#
# plt.figure(figsize=(9,6))
# plt.scatter(Vp_list, Rp_list)
# plt.plot(Vp_target, Rp_target, 'r-', label=u'有效前沿', lw=2.5)
# plt.plot(Vp_CML, Rp_CML, 'b--', label=u'资本市场线', lw=2.5)
# plt.plot(Vm, Em, 'yo', label=u'市场组合', markersize=14)
# plt.plot(Vp_min, Rp_min, 'g*', label=u'全局最小波动率', markersize=14)
# plt.xlabel(u'波动率', fontsize=13)
# plt.ylabel(u'预期收益率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.xlim(0.0, 0.3)
# plt.ylim(0.03, 0.22)
# plt.title(u'投资组合理论的可视化', fontsize=13)
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


'''CAPM'''
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import statsmodels.api as sm
#
# # 1. 导入上证180成分股数据并计算组合波动率随股票数量的变化
# price_stocks = pd.read_excel(
#     r'上证180指数成分股日收盘价（2018-2020年）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
#
# # 计算日收益率
# return_stocks = np.log(price_stocks / price_stocks.shift(1))
# n = len(return_stocks.columns)
# vol_port = np.zeros(n)
#
# # 逐次计算等权重组合的年化波动率
# for i in range(1, n+1):
#     w = np.ones(i) / i
#     cov = 252 * return_stocks.iloc[:, :i].cov()  # 年化协方差矩阵
#     vol_port[i-1] = np.sqrt(np.dot(w, np.dot(cov, w.T)))
#
# # 可视化组合数量与波动率的关系
# N_list = np.arange(n) + 1
# plt.figure(figsize=(9,6))
# plt.plot(N_list, vol_port, 'r-', lw=2.0)
# plt.xlabel(u'投资组合中的股票数量', fontsize=13)
# plt.ylabel(u'投资组合波动率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'投资组合中的股票数量与投资组合波动率之间的关系图', fontsize=13)
# plt.grid()
# plt.show()
#
#
# # 2. CAPM模型计算股票预期收益率
# def Ri_CAPM(beta, Rm, Rf):
#     '''定义运用资本资产定价模型计算股票预期收益率的函数
#     beta: 代表股票的贝塔值。
#     Rm: 代表市场收益率。
#     Rf: 代表无风险利率'''
#     Ri = Rf + beta * (Rm - Rf)
#     return Ri
#
# # 导入招商银行与沪深300数据
# P_bank_index = pd.read_excel(
#     r'招商银行A股与沪深300指数日收盘价数据（2017-2020年）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
#
# # 计算日收益率并删除缺失值
# R_bank_index = np.log(P_bank_index / P_bank_index.shift(1))
# R_bank_index = R_bank_index.dropna()
#
# # 提取因变量（招商银行收益率）和自变量（沪深300收益率）
# R_bank = R_bank_index['招商银行']
# R_index = R_bank_index['沪深300指数']
# R_index_addcons = sm.add_constant(R_index)  # 添加常数项
#
# # 构建OLS回归模型
# model = sm.OLS(endog=R_bank, exog=R_index_addcons)
# result = model.fit()
# print(result.summary())
# print(result.params)
#
#
# # 3. 计算年化预期收益率
# LPR_1Y = 0.0385  # 1年期无风险利率
# R_market = 252 * R_index.mean()  # 沪深300年化收益率
# R_stock = Ri_CAPM(beta=result.params[-1], Rm=R_market, Rf=LPR_1Y)
# print('招商银行A股的年化预期收益率', round(R_stock, 6))
#
#
# # 4. 证券市场线可视化
# beta_list = np.linspace(0, 2.0, 100)
# R_stock_list = Ri_CAPM(beta=beta_list, Rm=R_market, Rf=LPR_1Y)
#
# plt.figure(figsize=(9,6))
# plt.plot(beta_list, R_stock_list, 'r-', label=u'证券市场线', lw=2.0)
# plt.plot(result.params[-1], R_stock, 'o', lw=2.5)
# plt.axis('tight')
# plt.xticks(fontsize=13)
# plt.xlabel(u'贝塔值', fontsize=13)
# plt.xlim(0, 2.0)
# plt.yticks(fontsize=13)
# plt.ylabel(u'股票预期收益率', fontsize=13)
# plt.ylim(0, 0.2)
# plt.title(u'资本资产定价模型（以招商银行A股为例）', fontsize=13)
# plt.annotate(
#     u'贝塔值等于0.958对应的收益率',
#     fontsize=14,
#     xy=(0.96, 0.1115),
#     xytext=(1.0, 0.06),
#     arrowprops=dict(facecolor='b', shrink=0.05)
# )
# plt.legend(fontsize=13)
# plt.grid()
# plt.show()


'''绩效评估：各种比率'''

'''sharpe ratio'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 定义夏普比率计算函数
def SR(Rp, Rf, Vp):
    '''定义一个计算夏普比率的函数
    Rp: 代表投资组合的年化收益率。
    Rf: 代表无风险利率。
    Vp: 代表投资组合的年化波动率'''
    sharp_ratio = (Rp - Rf) / Vp  # 计算夏普比率的公式
    return sharp_ratio

# # 2. 导入基金数据并可视化
# fund = pd.read_excel(
#     r'国内4只开放式股票型基金净值数据（2018-2020）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# fund.plot(figsize=(9,6), grid=True)
# plt.show()
#
# # 3. 计算基金的年化收益、波动率与夏普比率
# R_fund = np.log(fund / fund.shift(1))  # 基金日收益率
# R_fund = R_fund.dropna()  # 删除缺失值
#
# R_mean = R_fund.mean() * 252  # 3年年均年化收益率
# Sigma = R_fund.std() * np.sqrt(252)  # 3年年化波动率
#
# R_f = 0.015  # 1年期银行存款基准利率（无风险利率）
# SR_3years = SR(Rp=R_mean, Rf=R_f, Vp=Sigma)
#
# print('2018年至2020年3年平均的夏普比率\n', round(SR_3years, 4))

# # 按年份提取基金日收益率
# R_fund2018 = R_fund.loc['2018-01-01':'2018-12-31']
# R_fund2019 = R_fund.loc['2019-01-01':'2019-12-31']
# R_fund2020 = R_f_fund.loc['2020-01-01':'2020-12-31']
#
# # 计算各年份的年化收益率
# R_mean_2018 = R_fund2018.mean() * 252
# R_mean_2019 = R_fund2019.mean() * 252
# R_mean_2020 = R_fund2020.mean() * 252
#
# # 计算各年份的年化波动率
# Sigma_2018 = R_fund2018.std() * np.sqrt(252)
# Sigma_2019 = R_fund2019.std() * np.sqrt(252)
# Sigma_2020 = R_fund2020.std() * np.sqrt(252)
#
# # 计算各年份的夏普比率
# SR_2018 = SR(Rp=R_mean_2018, Rf=R_f, Vp=Sigma_2018)
# SR_2019 = SR(Rp=R_mean_2019, Rf=R_f, Vp=Sigma_2019)
# SR_2020 = SR(Rp=R_mean_2020, Rf=R_f, Vp=Sigma_2020)
#
# # 输出2018年夏普比率
# print('2018年的夏普比率\n', round(SR_2018, 4))
#
# # 输出2019年夏普比率
# print('2019年的夏普比率\n', round(SR_2019, 4))
#
# # 输出2020年夏普比率
# print('2020年的夏普比率\n', round(SR_2020, 4))


'''sortino ratio'''
# 1. 定义索提诺比率计算函数
def SOR(Rp, Rf, Vd):
    '''定义一个计算索提诺比率的函数
    Rp: 表示投资组合的年化收益率。
    Rf: 表示无风险利率。
    Vd: 表示投资组合的年化下行标准差'''
    sortino_ratio = (Rp - Rf) / Vd  # 索提诺比率的数学表达式
    return sortino_ratio
# 2. 计算每只基金收益率的年化下行标准差
# fund = pd.read_excel(
#     r'国内4只开放式股票型基金净值数据（2018-2020）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# fund.plot(figsize=(9,6), grid=True)
# plt.show()
#
# R_fund = np.log(fund / fund.shift(1))  # 基金日收益率
# R_fund = R_fund.dropna()  # 删除缺失值
#
# R_mean = R_fund.mean() * 252  # 3年年均年化收益率
# Sigma = R_fund.std() * np.sqrt(252)  # 3年年化波动率
#
# R_f = 0.015  # 1年期银行存款基准利率（无风险利率）
#
# V_down = np.zeros_like(R_mean)
# for i in range(len(V_down)):
#     # 生成基金收益率为负的时间序列
#     R_neg = R_fund.iloc[:, i][R_fund.iloc[:, i] < 0]
#     N_down = len(R_neg)  # 计算亏损的交易天数
#     # 计算年化下行标准差
#     V_down[i] = np.sqrt(252) * np.sqrt(np.sum(R_neg**2) / N_down)
#     print(R_fund.columns[i], '年化下行标准差', round(V_down[i], 4))
#
# # 3. 计算2018-2020年3年平均的索提诺比率
# SOR_3years = SOR(Rp=R_mean, Rf=R_f, Vd=V_down)
# print('2018年至2020年3年平均的索提诺比率\n', round(SOR_3years, 4))


'''treynor ratio'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 1. 定义特雷诺比率计算函数
def TR(Rp, Rf, beta):
    '''定义一个计算特雷诺比率的函数
    Rp: 表示投资组合的年化收益率。
    Rf: 表示无风险利率。
    beta: 表示投资组合的贝塔值'''
    treynor_ratio = (Rp - Rf) / beta  # 特雷诺比率的数学表达式
    return treynor_ratio

# # 2. 导入沪深300指数数据并计算收益率
#
# fund = pd.read_excel(
#     r'国内4只开放式股票型基金净值数据（2018-2020）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# fund.plot(figsize=(9,6), grid=True)
# plt.show()
#
# R_fund = np.log(fund / fund.shift(1))  # 基金日收益率
# R_fund = R_fund.dropna()  # 删除缺失值
#
# R_mean = R_fund.mean() * 252  # 3年年均年化收益率
# Sigma = R_fund.std() * np.sqrt(252)  # 3年年化波动率
#
# R_f = 0.015  # 1年期银行存款基准利率（无风险利率）
#
# HS300 = pd.read_excel(
#     r'沪深300指数日收盘价（2018-2020年）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# R_HS300 = np.log(HS300 / HS300.shift(1))  # 沪深300日收益率
# R_HS300 = R_HS300.dropna()  # 删除缺失值
#
# # 3. 计算每只基金的贝塔值
# X_addcons = sm.add_constant(R_HS300)  # 自变量添加常数项
# betas = np.zeros_like(R_mean)
# cons = np.zeros_like(R_mean)
#
# for i in range(len(R_mean)):
#     y = R_fund.iloc[:, i]  # 因变量（基金收益率）
#     model = sm.OLS(endog=y, exog=X_addcons)  # 构建OLS模型
#     result = model.fit()  # 拟合模型
#     cons[i] = result.params[0]  # 常数项
#     betas[i] = result.params[1]  # 贝塔值
#     print(R_fund.columns[i], '贝塔值', round(betas[i], 4))
#
# # 4. 可视化基金与沪深300的散点及线性回归
# X_list = np.linspace(np.min(R_HS300), np.max(R_HS300), 200)
# plt.figure(figsize=(11,10))
# for i in range(len(R_mean)):
#     plt.scatter(R_HS300, R_fund.iloc[:, i])
#     plt.plot(X_list, cons[i] + betas[i]*X_list, 'r-', label=u'线性回归拟合', lw=2.0)
#     plt.xlabel(u'沪深300指数', fontsize=13)
#     plt.ylabel(R_fund.columns[i], fontsize=13)
#     plt.xticks(fontsize=13)
#     plt.yticks(fontsize=13)
#     plt.legend(fontsize=13)
#     plt.grid()
# plt.show()
#
# # 5. 计算2018-2020年3年平均的特雷诺比率
# TR_3years = TR(Rp=R_mean, Rf=R_f, beta=betas)
# print('2018年至2020年3年平均的特雷诺比率\n', round(TR_3years, 4))


'''calmar ratio'''
# 1. 定义卡玛比率计算函数
def CR(Rp, MDD):
    '''定义一个计算卡玛比率的函数
    Rp: 表示投资组合的年化收益率。
    MDD: 表示投资组合的最大回撤率'''
    calmar_ratio = Rp / MDD  # 卡玛比率的数学表达式
    return calmar_ratio

# 2. 定义最大回撤率计算函数
def MDD(data):
    '''定义一个计算投资组合最大回撤率的函数
    data: 代表某只基金的净值数据，以序列或者数据框格式输入'''
    n = len(data)  # 计算期间的交易天数
    DD = np.zeros((n-1, n-1))  # 创建n-1行、n-1列数组，用于存放回撤率数据
    for i in range(n-1):
        Pi = data.iloc[i+1]  # 第i个交易日的基金净值
        for j in range(i+1, n):
            Pj = data.iloc[j]  # 被套的第j个交易日的基金净值
            DD[i, j-1] = (Pi - Pj) / Pi  # 依次计算并存放期间的每个回撤率数据
    Max_DD = np.max(DD)  # 计算基金净值的最大回撤率
    return Max_DD

# fund = pd.read_excel(
#     r'国内4只开放式股票型基金净值数据（2018-2020）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# fund.plot(figsize=(9,6), grid=True)
# plt.show()
#
# R_fund = np.log(fund / fund.shift(1))  # 基金日收益率
# R_fund = R_fund.dropna()  # 删除缺失值
#
# R_mean = R_fund.mean() * 252  # 3年年均年化收益率
# Sigma = R_fund.std() * np.sqrt(252)  # 3年年化波动率
#
# R_f = 0.015  # 1年期银行存款基准利率（无风险利率）
#
# # 3. 提取各基金净值序列
# fund_zhonghai = fund["中海量化策略基金"]
# fund_nanfang = fund["南方新蓝筹基金"]
# fund_jiaoyin = fund["交银精选基金"]
# fund_tianhong = fund["天弘惠利基金"]
#
# # 4. 计算各基金最大回撤率
# MDD_zhonghai = MDD(data=fund_zhonghai)
# MDD_nanfang = MDD(data=fund_nanfang)
# MDD_jiaoyin = MDD(data=fund_jiaoyin)
# MDD_tianhong = MDD(data=fund_tianhong)
#
# # 输出最大回撤率
# print('2018年至2020年中海量化策略基金的最大回撤率', round(MDD_zhonghai, 4))
# print('2018年至2020年南方新蓝筹基金的最大回撤率', round(MDD_nanfang, 4))
# print('2018年至2020年交银精选基金的最大回撤率', round(MDD_jiaoyin, 4))
# print('2018年至2020年天弘惠利基金的最大回撤率', round(MDD_tianhong, 4))
#
# # 5. 计算各基金卡玛比率
# CR_zhonghai = CR(Rp=R_mean['中海量化策略基金'], MDD=MDD_zhonghai)
# CR_nanfang = CR(Rp=R_mean['南方新蓝筹基金'], MDD=MDD_nanfang)
# CR_jiaoyin = CR(Rp=R_mean['交银精选基金'], MDD=MDD_jiaoyin)
# CR_tianhong = CR(Rp=R_mean['天弘惠利基金'], MDD=MDD_tianhong)
#
# # 输出卡玛比率
# print('2018年至2020年中海量化策略基金的卡玛比率', round(CR_zhonghai, 4))
# print('2018年至2020年南方新蓝筹基金的卡玛比率', round(CR_nanfang, 4))
# print('2018年至2020年交银精选基金的卡玛比率', round(CR_jiaoyin, 4))
# print('2018年至2020年天弘惠利基金的卡玛比率', round(CR_tianhong, 4))


'''information ratio'''
# 1. 定义信息比率计算函数
def IR(Rp, Rb, TE):
    '''定义一个计算信息比率的函数
    Rp: 表示投资组合的年化收益率。
    Rb: 表示基准组合的年化收益率。
    TE: 表示跟踪误差'''
    information_ratio = (Rp - Rb) / TE  # 信息比率的数学表达式
    return information_ratio

# fund = pd.read_excel(
#     r'国内4只开放式股票型基金净值数据（2018-2020）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# fund.plot(figsize=(9,6), grid=True)
# plt.show()
#
# R_fund = np.log(fund / fund.shift(1))  # 基金日收益率
# R_fund = R_fund.dropna()  # 删除缺失值
#
# R_mean = R_fund.mean() * 252  # 3年年均年化收益率
# Sigma = R_fund.std() * np.sqrt(252)  # 3年年化波动率
#
# R_f = 0.015  # 1年期银行存款基准利率（无风险利率）
#
# HS300 = pd.read_excel(
#     r'沪深300指数日收盘价（2018-2020年）.xlsx',
#     sheet_name="Sheet1",
#     header=0,
#     index_col=0
# )
# R_HS300 = np.log(HS300 / HS300.shift(1))  # 沪深300日收益率
# R_HS300 = R_HS300.dropna()  # 删除缺失值
#
# # 2. 计算每只基金的年化跟踪误差
# TE_fund = np.zeros_like(R_mean)
# for i in range(len(R_mean)):
#     # 计算基金跟踪偏离度并以数组格式存放
#     TD = np.array(R_fund.iloc[:, i]) - np.array(R_HS300.iloc[:, 0])
#     TE_fund[i] = TD.std() * np.sqrt(252)  # 计算并存放每只基金的年化跟踪误差
#     print(R_fund.columns[i], '跟踪误差', round(TE_fund[i], 4))
#
# # 3. 计算沪深300指数的年化收益率
# R_mean_HS300 = R_HS300.mean() * 252
# R_mean_HS300 = float(R_mean_HS300)
#
# # 4. 计算2018-2020年3年平均的信息比率
# IR_3years = IR(Rp=R_mean, Rb=R_mean_HS300, TE=TE_fund)
# print('2018年至2020年3年平均的信息比率\n', round(IR_3years, 4))


