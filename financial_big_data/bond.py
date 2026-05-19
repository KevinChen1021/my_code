import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif']=['FangSong']
mpl.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
# 以上准备工作


'''债券市场概览1：债券存量规模 and GDP'''
# bond_GDP=pd.read_excel('债券存量规模与GDP（2010-2020年）.xlsx',sheet_name="Sheet1",header=0,index_col=0) #导入外部数据
#
# bond_GDP.plot(kind='bar',figsize=(9,6),fontsize=13,grid=True) #可视化
# plt.ylabel(u'金额', fontsize=11) #增加纵坐标轴标签
# plt.show()


#债券市场概览2：债券市场分布
# # 导入外部数据
# bond=pd.read_excel('2020年末存量债券的市场分布情况.xlsx', sheet_name="Sheet1",header=0,index_col=0)
# # 绘制饼图
# plt.figure(figsize=(9,6))
# plt.pie(x=bond['债券余额（亿元）'], labels=bond.index)
# plt.axis('equal')  # 使饼图呈现正圆形
# plt.legend(loc=2, fontsize=13)  # 图例放置在左上方
# plt.title(u'2020年年末存量债券的市场分布图', fontsize=13)
# plt.show()


'''单一贴现率债券价格计算函数'''
def Bondprice_onediscount(C,M,m,y,t):
    '''定义一个基于单一贴现率计算债券价格的函数。
    C: 代表债券的票面利率，如果输入0则表示零息债券
    M: 代表债券的本金（面值）。
    m: 代表债券利息每年支付的频次。
    y.: 代表单一贴现率。
    t: 代表定价日至后续每一期票息支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    if C==0:
        price=np.exp(-y*t)*M
    else:
        coupon=np.ones_like(t)*(M*C/m)
        NPV_coupon=np.sum(coupon*np.exp(-y*t))
        NPV_par=M*np.exp(-y*t[-1])
        price=NPV_coupon+NPV_par
    return price


'''债券定价案例'''
# #20贴现国债27的票面利率
# C_TB2027=0
# #20贴现国债27的贴现率及本金将直接调用该变量
# par=100
# T_TB2027=0.5
# #20贴现国债27的期限
# m_TB2027=0
# #20贴现国债27每年支付利息的频次
# y_TB2027=0.01954
# #20贴现国债27的贴现率
#
# #计算债券价格
# value_TB2027=Bondprice_onediscount(C=C_TB2027,M=par,m=m_TB2027,y=y_TB2027,t=T_TB2027)
# print("2020年6月8日20贴现国债27的价格",round(value_TB2027,4))


'''债券YTM计算函数'''
def YTM(P,C,M,m,t):
    '''定义一个计算针对零息债券到期收益率的函数
    P: 代表观察到的债券市场价格。
    C: 代表债券的票面利率。
    M: 代表债券的本金。
    m: 代表债券利息每年支付的频次。
    t: 代表定价日至后续每一期票息支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    import scipy.optimize as so  #导入SciPy的子模块optimize
    def f(y):  #需要再自定义一个函数
        coupon=np.ones_like(t)*M*C/m  #创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-y*t))  #计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-y*t[-1])  #计算本金在定价日的现值
        value=NPV_coupon+NPV_par  #定价日的债券现金流现值之和
        return value-P  #债券现金流现值之和减去债券市场价格
    if C==0:
        y=(np.log(M/P))/t  #计算零息债券的到期收益率
    else:
        y=so.fsolve(f, x0=0.1)  #针对带票息债券，第2个参数是任意输入的初始值
    return y

'''债券YTM计算的案例'''
# par=100
# #09附息国债11的市场价格
# P_TB0911=104.802
# #09附息国债11的票面利率
# C_TB0911=0.0369
# #09附息国债11票息支付的频次
# m_TB0911=2
# #09附息国债11的剩余期限
# T_TB0911=4
#
# #定价日至每期票息支付日的期限数组
# Tlist_TB0911=np.arange(1,m_TB0911*T_TB0911+1)/m_TB0911
#
# #计算到期收益率（数组格式）
# Bond_yield=YTM(P=P_TB0911,C=C_TB0911,M=par,m=m_TB0911,t=Tlist_TB0911)
# #转换为单一的浮点型
# Bond_yield=float(Bond_yield)
# print('2020年6月11日09附息国债11的到期收益率',round(Bond_yield,6))


'''基于不同期限贴现率的债券定价'''
def Bondprice_diftdiscount(C,M,m,y,t):
    '''定义一个基于不同期限现贴现率计算债券价格的函数。
    C: 代表债券的票面利率，如果输入0则表示零息债券。
    M: 代表债券的本金。
    m: 代表不同期限的贴现率，用数组格式输入；零息债券可直接输入数字。
    y: 代表定价日至后续每一期票息支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    if C==0:
        price=np.exp(-y*t)*M  #针对零息债券
    else:
        coupon=np.ones_like(y)*M*C/m  #创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-y*t))  #计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-y[-1]*t[-1])  #计算本金在定价日的现值
        price=NPV_coupon+NPV_par  #计算定价日的债券价格
    return price


'''利用票息剥离法计算零息利率'''
# # 第1步：输入参数并定义函数
# import numpy as np
# P=np.array([99.5508, 99.0276, 100.8104, 102.1440, 102.2541])  # 不同期限债券价格
# T=np.array([0.25, 0.5, 1.0, 1.5, 2.0])  # 债券的期限结构
# C=np.array([0, 0, 0.0258, 0.0357, 0.0336])  # 债券票面利率数组
# m=2  # 第4只和第5只债券付息次数
# par=100
#
# def f(R):
#     from numpy import exp
#     R1,R2,R3,R4,R5=R
#     B1 = P[0]*exp(R1*T[0]) - par
#     B2 = P[1]*exp(R2*T[1]) - par
#     B3 = P[2]*exp(R3*T[2]) - par*(1+C[2])
#     B4 = par*(C[3]*exp(-R2*T[1])/m + C[3]*exp(-R3*T[2])/m + (1+C[3]/m)*exp(-R4*T[3])) - P
#     B5 = par*(C[-1]*exp(-R2*T[1])/m + C[-1]*exp(-R3*T[2])/m + C[-1]*exp(-C[3]*T[3])/m + (1+C[-1]/m)*exp(-R5*T[-1])) - P[-1]
#     return np.array([B1,B2,B3,B4,B5])
#
# # 第2步：求解联立方程组
# import scipy.optimize as so
# r0=[0.1, 0.1, 0.1, 0.1, 0.1]  # 初始猜测的零息利率
# rates=so.fsolve(func=f, x0=r0)  # 计算不同期限的零息利率
#
# print('0.25年期的零息利率（连续复利）', round(rates[0],6))
# print('0.5年期的零息利率（连续复利）', round(rates[1],6))
# print('1年期的零息利率（连续复利）', round(rates[2],6))
# print('1.5年期的零息利率（连续复利）', round(rates[3],6))
# print('2年期的零息利率（连续复利）', round(rates[4],6))
#
# # 第3步：可视化零息利率
# import matplotlib.pyplot as plt
# plt.figure(figsize=(9,6))
# plt.plot(T,rates,'b-')
# plt.plot(T,rates,'ro')
# plt.xlabel(u'期限(年)', fontsize=13)
# plt.ylabel(u'利率', fontsize=13)
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'运用票息剥离法得到的零息曲线', fontsize=13)
# plt.grid()
# plt.show()


#缺少数据怎么办：插值处理
# import scipy.interpolate as si  #导入SciPy的子模块interpolate
# P=np.array([99.5508, 99.0276, 100.8104, 102.1440, 102.2541])  # 不同期限债券价格
# T=np.array([0.25, 0.5, 1.0, 1.5, 2.0])  # 债券的期限结构
# C=np.array([0, 0, 0.0258, 0.0357, 0.0336])  # 债券票面利率数组
# m=2  # 第4只和第5只债券付息次数
# par=100
# #运用已有数据构建插值函数并且运用3阶样条曲线插值法
# func=si.interp1d(x=T,y=rates,kind="cubic")
# #创建包含0.75年、1.25年和1.75年期限的数组
# T_new=np.array([0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0])
# #计算基于插值法的零息利率
# rates_new=func(T_new)
# #运用for语句快速输出相关结果
# for i in range(len(T_new)):
#     print(T_new[i],'年期限的零息利率',round(rates_new[i],6))
#
# plt.figure(figsize=(9,6))
# plt.plot(T_new,rates_new,'o')
# plt.plot(T_new,rates_new,'-')
# plt.xlabel(u'期限(年)', fontsize=13)
# plt.xticks(fontsize=13)
# plt.ylabel(u'利率', fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'基于3阶样条曲线插值方法得到的零息曲线', fontsize=13)
# plt.grid()
# plt.show()


'''计算麦考利久期'''
import numpy as np

def Mac_Duration(C,M,m,y,t):
    '''定义一个计算债券麦考利久期的函数
    C: 代表债券的票面利率。
    M: 代表债券的面值。
    m: 代表债券票息每年支付的频次。
    y: 代表债券的到期收益率（连续复利）。
    t: 代表定价日至后续每一期现金流支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    if C==0:
        duration=t  #针对零息债券，计算零息债券的麦考利久期
    else:
        coupon=np.ones_like(t)*M*C/m  #创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-y*t))  #计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-y*t[-1])  #计算本金在定价日的现值
        Bond_value=NPV_coupon+NPV_par  #计算定价日的债券价格
        cashflow=coupon  #现金流数组并初始设定等于票息
        cashflow[-1]=M*(1+C/m)  #现金流数组最后的元素调整为票息与本金之和
        weight=cashflow*np.exp(-y*t)/Bond_value  #计算时间的权重
        duration=np.sum(t*weight)  #计算带票息债券的麦考利久期
    return duration


'''麦考利久期计算案例'''
# par=100
# #09附息国债11的票面利率
# C_TB0911=0.0369
# #09附息国债11的票息支付频次
# m_TB0911=2
# #09附息国债11的到期收益率
# y_TB0911=0.024
# #09附息国债11的剩余期限（年）
# T_TB0911=4
# #09附息国债11现金流支付期限数组
# Tlist_TB0911=np.arange(1,m_TB0911*T_TB0911+1)/m_TB0911
# #计算麦考利久期
# D1_TB0911=Mac_Duration(C=C_TB0911,M=par,m=m_TB0911,y=y_TB0911,t=Tlist_TB0911)
# print('2020年6月12日09附息国债11的麦考利久期',round(D1_TB0911,4))


'''考察coupon、YTM和久期间的关系'''
# par=100
# #09附息国债11的票面利率
# C_TB0911=0.0369
# #09附息国债11的票息支付频次
# m_TB0911=2
# #09附息国债11的到期收益率
# y_TB0911=0.024
# #09附息国债11的剩余期限（年）
# T_TB0911=4
# #09附息国债11现金流支付期限数组
# Tlist_TB0911=np.arange(1,m_TB0911*T_TB0911+1)/m_TB0911
# # 第1步：计算不同票面利率、到期收益率对应的麦考利久期
# C_list=np.linspace(0.02,0.06,200)  # 票面利率在[2%,6%]区间进行等差取值
# y_list=np.linspace(0.01,0.05,200)  # 到期收益率在[1%,5%]区间进行等差取值
#
# D_list1=np.ones_like(C_list)  # 创建存放对应不同票面利率的麦考利久期初始数组
# D_list2=np.ones_like(y_list)  # 创建存放对应不同到期收益率的麦考利久期初始数组
#
# # 用for语句计算对应不同票面利率的麦考利久期
# for i in range(len(C_list)):
#     D_list1[i]=Mac_Duration(C=C_list[i],M=par,m=m_TB0911,y=y_TB0911,t=Tlist_TB0911)
#
# # 用for语句计算对应不同到期收益率的麦考利久期
# for i in range(len(y_list)):
#     D_list2[i]=Mac_Duration(C=C_TB0911,M=par,m=m_TB0911,y=y_list[i],t=Tlist_TB0911)
#
# # 第2步：可视化票面利率、到期收益率与麦考利久期的关系（1x2子图）
# plt.figure(figsize=(11,6))
#
# # 第1行第1列的子图
# plt.subplot(1,2,1)
# plt.plot(C_list, D_list1,'r-',lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'票面利率',fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'麦考利久期',fontsize=13)
# plt.title(u'票面利率与麦考利久期的关系图',fontsize=14)
# plt.grid()
#
# # 第1行第2列的子图（与第1个子图的y轴同刻度）
# plt.subplot(1,2,2,sharey=plt.subplot(1,2,1))
# plt.plot(y_list, D_list2,'b-',lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'到期收益率',fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'到期收益率与麦考利久期的关系图',fontsize=14)
# plt.grid()
#
# plt.show()


'''修正久期'''
import numpy as np

def Mod_Duration(C,M,m1,m2,y,t):
    '''定义一个计算债券修正久期的函数
    C: 代表债券的票面利率。
    M: 代表债券的面值。
    m1: 代表债券票息每年支付的频次。
    m2: 代表债券到期收益率每年复利频次，通常m2等于m1。
    y: 代表每年复利m2次的到期收益率。
    t: 代表定价日至后续每一期现金流支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    if C==0:
        Macaulay_duration=t  #针对零息债券，计算零息债券的麦考利久期
    else:
        r=m2*np.log(1+y/m2)  #计算等价的连续复利的到期收益率
        coupon=np.ones_like(t)*M*C/m1  #创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-r*t))  #计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-r*t[-1])  #计算本金在定价日的现值
        price=NPV_coupon+NPV_par  #计算定价日的债券价格
        cashflow=coupon  #先将现金流设定等于票息
        cashflow[-1]=M*(1+C/m1)  #数组最后的元素等于票息与本金之和
        weight=cashflow*np.exp(-r*t)/price  #计算时间的权重
        Macaulay_duration=np.sum(t*weight)  #计算带票息债券的麦考利久期
    Modified_duration=Macaulay_duration/(1+y/m2)  #计算债券的修正久期
    return Modified_duration


'''修正久期计算案例'''
# # 6.3.2节的自定义函数
# def Rm(Rc,m):
#     '''定义一个已知复利频次和连续复利率，计算等价的复利率的函数
#     Rc: 代表连续复利率。
#     m: 代表复利频次'''
#     r=m*(np.exp(Rc/m)-1)  # 计算等价的复利频次为m的利率
#     return r
#
# # 计算等价的每年复利2次的到期收益率
# par=100
# #09附息国债11的票面利率
# C_TB0911=0.0369
# #09附息国债11的票息支付频次
# m_TB0911=2
# #09附息国债11的到期收益率
# y_TB0911=0.024
# #09附息国债11的剩余期限（年）
# T_TB0911=4
# #09附息国债11现金流支付期限数组
# Tlist_TB0911=np.arange(1,m_TB0911*T_TB0911+1)/m_TB0911
# y1_TB0911=Rm(Rc=y_TB0911,m=m_TB0911)
# print("计算09附息国债11每年复利2次的到期收益率",round(y1_TB0911,6))
#
# # 计算修正久期
# D2_TB0911=Mod_Duration(C=C_TB0911,M=m_TB0911,m1=m_TB0911,m2=m_TB0911,y=y1_TB0911,t=Tlist_TB0911)
# print("2020年6月12日09附息国债11的修正久期",round(D2_TB0911,4))


'''美元久期'''
import numpy as np

def Dollar_Duration(C,M,m1,m2,y,t):
    '''定义一个计算债券美元久期的函数
    C: 代表债券的票面利率。
    M: 代表债券的面值。
    m1: 代表债券票息每年支付的频次。
    m2: 代表债券到期收益率每年复利频次，通常m2等于m1。
    y: 代表每年复利m2次的债券到期收益率。
    t: 代表定价日至后续每一期现金流支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    r=m2*np.log(1+y/m2)  # 计算等价的连续复利到期收益率
    if C==0:
        price=M*np.exp(-r*t)  # 计算零息债券的价格
        Macaulay_D=t  # 计算零息债券的麦考利久期
    else:
        coupon=np.ones_like(t)*M*C/m1  # 创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-r*t))  # 计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-r*t[-1])  # 计算本金在定价日的现值
        price=NPV_coupon+NPV_par  # 计算定价日的债券价格
        cashflow=coupon  # 先将现金流设定等于票息
        cashflow[-1]=M*(1+C/m1)  # 数组最后的元素等于票息与本金之和
        weight=cashflow*np.exp(-r*t)/price  # 计算时间的权重
        Macaulay_D=np.sum(t*weight)  # 计算带票息债券的麦考利久期
    Modified_D=Macaulay_D/(1+y/m2)  # 计算债券的修正久期
    Dollar_D=price*Modified_D  # 计算债券的美元久期
    return Dollar_D


'''美元久期计算案例'''
# # 6.3.2节的自定义函数
# def Rm(Rc,m):
#     '''定义一个已知复利频次和连续复利率，计算等价的复利率的函数
#     Rc: 代表连续复利率。
#     m: 代表复利频次'''
#     r=m*(np.exp(Rc/m)-1)  # 计算等价的复利频次为m的利率
#     return r
# par=100
# #09附息国债11的票面利率
# C_TB0911=0.0369
# #09附息国债11的票息支付频次
# m_TB0911=2
# #09附息国债11的到期收益率
# y_TB0911=0.024
# #09附息国债11的剩余期限（年）
# T_TB0911=4
# #09附息国债11现金流支付期限数组
# Tlist_TB0911=np.arange(1,m_TB0911*T_TB0911+1)/m_TB0911
# y1_TB0911=Rm(Rc=y_TB0911,m=m_TB0911)
# # 计算美元久期
# D3_TB0911=Dollar_Duration(C=C_TB0911,M=par,m1=m_TB0911,m2=m_TB0911,y=y1_TB0911,t=Tlist_TB0911)
# print("2020年6月12日09附息国债11的美元久期",round(D3_TB0911,2))


'''凸度'''
import numpy as np

def Convexity(C,M,m,y,t):
    '''定义一个计算债券凸性的函数
    C: 代表债券的票面利率。
    M: 代表债券的面值。
    m: 代表债券票息每年支付的频次。
    y: 代表债券的到期收益率（连续复利）。
    t: 代表定价日至后续每一期现金流支付日的期限长度，用数组格式输入；零息债券可直接输入数字'''
    if C==0:
        convexity=np.power(t,2)  #针对零息债券，计算零息债券的凸性
    else:
        coupon=np.ones_like(t)*M*C/m  #创建每一期票息金额的数组
        NPV_coupon=np.sum(coupon*np.exp(-y*t))  #计算每一期票息在定价日的现值之和
        NPV_par=M*np.exp(-y*t[-1])  #计算本金在定价日的现值
        price=NPV_coupon+NPV_par  #计算定价日的债券价格
        cashflow=coupon  #先将现金流设定等于票息
        cashflow[-1]=M*(1+C/m)  #数组最后的元素等于票息与本金之和
        weight=cashflow*np.exp(-y*t)/price  #计算每期现金流时间的权重
        convexity=np.sum(np.power(t,2)*weight)  #计算带票息债券的凸性
    return convexity


'''凸度计算案例'''
# #计算债券凸性
# def Rm(Rc,m):
#     '''定义一个已知复利频次和连续复利率，计算等价的复利率的函数
#     Rc: 代表连续复利率。
#     m: 代表复利频次'''
#     r=m*(np.exp(Rc/m)-1)  # 计算等价的复利频次为m的利率
#     return r
# par=100
# #09附息国债11的票面利率
# C_TB0911=0.0369
# #09附息国债11的票息支付频次
# m_TB0911=2
# #09附息国债11的到期收益率
# y_TB0911=0.024
# #09附息国债11的剩余期限（年）
# T_TB0911=4
# #09附息国债11现金流支付期限数组
# Tlist_TB0911=np.arange(1,m_TB0911*T_TB0911+1)/m_TB0911
# y1_TB0911=Rm(Rc=y_TB0911,m=m_TB0911)
# Convexity_TB0911=Convexity(C=C_TB0911,M=par,m=m_TB0911,y=y_TB0911,t=Tlist_TB0911)
# print("2020年6月12日09附息国债11的凸性",round(Convexity_TB0911,4))


'''债券信用风险测量（违约概率）'''
def prob(y1,y2,R,T):
    '''定义一个计算违约概率并且计算连续复利的概率的函数
    y1: 代表无风险零息利率，并且是连续复利。
    y2: 代表存在信用风险的债券到期收益率，并且是连续复利。
    R: 代表债券的违约回收率。
    T: 代表债券的期限（年）'''
    A=(np.exp(-y2*T)-R*np.exp(-y1*T))/(1-R)  #式(7-22)中的圆括号内的表达式
    prob=-np.log(A)/T-y1  #计算连续复利的违约概率
    return prob


'''违约概率计算案例'''
# #16宜章养老债的剩余期限
# T_yz=3
# #14冀建投的剩余期限
# T_jj=5
# #16宜章养老债的到期收益率
# y_yz=0.073611
# #14冀建投的到期收益率
# y_jj=0.042471
# #16宜章养老债的违约回收率
# R_yz=0.381
# #14冀建投的违约回收率
# R_jj=0.696
# #3年期无风险零息利率
# rate_3y=0.02922
# #5年期无风险零息利率
# rate_5y=0.029811
#
# #16宜章养老债的违约概率
# default_yz=prob(y1=rate_3y,y2=y_yz,R=R_yz,T=T_yz)
# #14冀建投的违约概率
# default_jj=prob(y1=rate_5y,y2=y_jj,R=R_jj,T=T_jj)
#
# print('16宜章养老债连续复利的违约概率',round(default_yz,4))
# print('14冀建投连续复利的违约概率',round(default_jj,4))
#
# # 14冀建投到期收益率的数组
# y_jj_list=np.linspace(0.03,0.06,100)
# # 计算不同的到期收益率对应的违约概率
# default_jj_list1=prob(y1=rate_5y,y2=y_jj_list,R=R_jj,T=T_jj)
#
# # 14冀建投违约回收率的数组
# R_jj_list=np.linspace(0.4,0.8,100)
# # 计算不同的违约回收率对应的违约概率
# default_jj_list2=prob(y1=rate_5y,y2=y_jj,R=R_jj_list,T=T_jj)
#
# # 可视化债券到期收益率、违约回收率对违约概率的影响
# plt.figure(figsize=(11,6))
#
# # 第1行第1列的子图
# plt.subplot(1,2,1)
# plt.plot(y_jj_list, default_jj_list1,'r-',lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'债券到期收益率',fontsize=13)
# plt.yticks(fontsize=13)
# plt.ylabel(u'违约概率',fontsize=13,rotation=90)
# plt.title(u'债券到期收益率与违约概率的关系图',fontsize=14)
# plt.grid()
#
# # 第1行第2列的子图
# plt.subplot(1,2,2)
# plt.plot(R_jj_list, default_jj_list2,'b-',lw=2.5)
# plt.xticks(fontsize=13)
# plt.xlabel(u'债券违约回收率',fontsize=13)
# plt.yticks(fontsize=13)
# plt.title(u'债券违约回收率与违约概率的关系图',fontsize=14)
# plt.grid()
#
# plt.show()