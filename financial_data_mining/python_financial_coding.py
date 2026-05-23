import os
os.chdir("C:\\Users\\KevinChen\\Desktop\\my_python")

import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
from math import exp, log, sqrt, pi
import numpy_financial as npf
from scipy.stats import norm
import statsmodels.api as sm
import scipy.optimize
from scipy.optimize import minimize
# from scipy.optimize import fmax
import datetime
import sqlite3

'''showing the functions of a package'''
# print(dir(npf))


'''time value of money'''


'''annuity'''
'''fixed or growing'''
'''perpetuity or not'''
'''due or not'''
# def pv_growing_annuity(c, r, g, n):
#     return (c/r * 1 - (1+g)**n/(1+r)**n)
# def fv_growing_annuity(c, r, g, n):
#     return (c/r)*((1+r)**n - (1+g)**n)


'''first annuity paid after k years'''
# def pv_perpetuity_delayed(c, r, k):
#     return(1/(1+r)**(k-1))*(c/r)


'''NPV and IRR'''
# cashflow = [-100, 50, 60, 70]
# npv = npf.npv(0.05, cashflow)
# irr = npf.irr(cashflow)
# print(irr)


'''download data'''
# df_IBM = yf.download("IBM", "2023-01-01", "2025-12-31")
'''calculating daily returns'''
# df_IBM["ret"] = df_IBM["Close"].pct_change()
'''add a column and name it'''
# df_IBM["ticker"] = 'ibm'
'''saving the file'''
'''save your data to a pickle format'''
# df_IBM.to_pickle("ibm.pickle")
'''save to a csv format'''
# df_IBM.to_csv()
'''drop blank data'''
# ret = df_IBM.dropna()
'''testing whether the mean is statistically equal to 0'''
# ret_mean = ret.mean()
# print(stats.ttest_1samp(ret, 0))


'''convert daily return to yearly return'''
'''default index of yfinance dataframe: date'''
# aa = pd.DataFrame(df_IBM["Close"].pct_change().dropna() + 1)
# aa["yyyy"] = aa.index.year
# aa.columns = ["retPlus1", "yyyy"]
# retAnnual = aa.retPlus1.groupby(aa.yyyy).prod()-1
'''convert daily return to monthly return'''
# aa["yyyymm"] = aa.index.year * 100 + aa.index.month
# retMontly = aa.retPlus1.groupby(aa.yyyymm).prod() - 1
# retMontly.mean()
# retMontly.std()


'''Fama-French 3-factors'''
# infile = "http://datayyy.com/data_pickle/ff3Daily.pickle"
# ff = pd.read_pickle(infile)
# print(ff.head())


'''t-test'''
'''ttest_ind and ttest_1samp'''
# begdate = '2020-1-1'
# enddate = '2021-12-31'
# def ret_f(ticker, begdate, enddate):
#     df = yf.download(ticker, begdate, enddate)
#     ret = df["Close"].pct_change().dropna()
#     return ret
# a = ret_f("IBM", begdate, enddate)
# b = ret_f("NVDA", begdate, enddate)
# print(stats.ttest_ind(a, b))


'''return distribution visualization'''
# [n, bins, patches] = plt.hist(b, 100)
# mu = b.mean()
# sigma = b.std()
# x = norm.pdf(bins,mu,sigma)
# plt.plot(bins, x, color='red',lw=2)
# plt.title("IBM return dist")
# plt.xlabel("return")
# plt.ylabel("frequency")
# plt.show()


'''bond and stock valuation'''
'''effective rate: annually'''

'''this is EAR in annually compounded'''
'''formula should be remembered'''
def effective_annual_rate(APR, n_period):
    EAR = (1 + APR/n_period)**n_period - 1
    return EAR

# print(round(effect(0.1, 2), 5))

'''this is to change APR to one that is different periodically compounded'''
'''in order to compare bonds with different payment frequency'''
'''second effective rate'''

def effectiveRate(APR1, m1, m2):
    EAR2 = (1 + APR1/m1)**(m1/m2) - 1
    return EAR2

# print(effectiveRate(0.1, 2, 4))

'''APR2 = EAR2 * m2'''
'''APR is a kind of stated interest rate'''
'''IRR, we use npf.irr() to calculate'''
# cash_flow = [-100, 39, 59, 37, 29]
# irr1 = npf.irr(cash_flow)
# print(irr1)


'''single annual rate to continuous compounding rate'''
'''EAR limited'''
def RmToRC(Rm, freq):
    Rc = freq * log(1 + Rm)
    return Rc


'''credit rate of bonds'''
# path = "http://datayyy.com/data_pickle/"
# infile = path + "spreadBasedOnCreditRating.pkl"
# spread = pd.read_pickle(infile)


'''time structure of bonds'''
# time = [3/12, 6/12, 2, 3, 5, 10, 20]
# rate = [0.47, 0.6, 1.18, 1.53, 2, 2.53, 3.12]
# plt.title("term structure of interest rate")
# plt.xlabel("time")
# plt.ylabel("risk-free rate")
# plt.plot(time, rate)
# plt.show()


'''pricing zero coupon bond'''
# annual interest rate is 5%
# ten years:12*10
'''every monnth you deposit 100, lasting 10 years'''
# npf.pv(0.05/12, 12*10, -100, 15692.93)


'''calculating YTM'''
'''npf params: rate, period, pmt, pv, fv; when=begin/end(default end)'''
pv = -600
fv = 1000
nYear = 10
freq = 2 
couponRate = 0.04
# npf.rate(nYear*freq, fv*couponRate/freq, pv, fv)


'''calculating duration (Marcauly)'''
'''focus on the formula'''
def bondPrice(year, rate, couponRate, freq):
    bondPrice = npf.pv(rate/freq, year*freq, fv*couponRate/freq, fv)
    return -bondPrice

def Duration(year, fv, rate, coouponRate, freq):
    n = year*freq
    coupon = fv*couponRate/freq
    B = bondPrice(year, rate, couponRate, freq)
    D = 0
    for i in range(1, n + 1):
        t = i/freq
        w = npf.pv(rate/freq, i, 0, coupon)/B
        D += w * t
        if i == n:
            w = npf.pv(rate/freq, i, 0, fv)/B
            D += w*t
            return round(D, 4), round(B, 4)
'''modified duration:calculated from Marcauly duration'''
'''Dmodified = D/(1 + YTM/freq)'''
# d1_modified = d1[0] / (1 + 0.1/2)


'''pricing a stock: 2 periods'''
# dividends = [1.8, 2.07, 2.2277, 2.48, 2.68, 2.7877]
# R = 0.102
# g = 0.03
# p1 = npf.npv(R, dividends[0:-1])/(1+R)
# p2 = -npf.pv(R, 5, 0, 2.7877)/(R - g)


'''CAPM model'''
stock_return = [0.065, 0.0265, -0.0593, -0.001, 0.0345]
mkt_return = [0.055, -0.09, -0.041, 0.045, 0.022]

'''linear regression'''
'''Y = alpha + beta*X'''
'''method 1:stats.linregress(X, Y)'''
# (beta, alpha, r_value, p_value, std_err) = stats.linregress(mkt_return, stock_return)
# print("Pearson correlation value = ", r_value)
# print("P_value = ", p_value)
'''method 2: using OLS(Y, X)'''
# mkt_return = sm.add_constant(mkt_return)
# results = sm.OLS(stock_return, mkt_return).fit()
# print(results.summary())

'''linear regression model visualization'''
# np.random.seed(123456)
# alpha = 1
# beta = 0.8
# n = 20
# x = np.arange(n)
# y = alpha + beta*x + np.random.rand(n)
# z = alpha + beta*x
# plt.plot(x, y)
# plt.plot(x, z)
# plt.show()


'''join: left, right, inner, outer(union)'''
'''default:inner'''
'''recalling SQL'''
# df1 = pd.DataFrame({'a':['foo', 'bar'], 'b':[1, 2]})
# df2 = pd.DataFrame({'a':['foo', 'baz'], 'c':[3, 4]})
# df_left = df1.merge(df2, how='left', on='a')
# df_inner = df1.merge(df2, how='inner', on='a')


'''distinguishing Close and Adj Close'''
'''use stock prices from 2 stocks to measure the CAPM'''
# ibm = yf.download("IBM")
# sp500 = yf.download("^GSPC")
'''creating new column called ret in IBM Dataframe'''
# ibm['ret'] = ibm['Close'].pct_change()
# sp500['mktRet'] = sp500['Close'].pct_change()
# df = pd.merge(ibm, sp500, left_index=True, right_index=True)
'''drop blank data'''
# df = df.dropna()
# y = df['ret']
# x = df['mktRet']


'''T-density distribution(t distribution)'''
'''confidence interval = 1 - alpha'''
'''alpha: significance level'''

# a = range(-30, 30)
# dfreedom = 30
# x = []
# y = []
'''drawing T probability density function'''
# for i in a:
#     b = i/10
#     x.append(b)
#     y.append(stats.t.pdf(b, dfreedom))
    
# plt.plot(x, y)
# plt.title("T-density")
# plt.show()
'''pdf: probability density function'''
'''cdf: cumulative density function'''
'''ppf: inverse function of cdf(given probability, got value)'''


'''using the statsmodels function'''
# import statsmodels.api as sm

# y = [1, 2, 3, 4, 2, 3, 4]
# x = range(1, len(y) + 1)

# x = sm.add_constant(x)
# results = sm.OLS(y, x).fit()
# print(results.summary())
'''params: intercept, slope'''


'''multivariable models and performance measures'''

'''Fama French'''
# ibm = yf.download("IBM", "2010-01-01", "2020-12-31", multi_level_index=False)
# # ibm= pd.read_pickle('ibm.pkl')

# #calculate the returns of IBM
# ibm["ret"] = ibm["Close"].pct_change()

# infile = 'http://datayyy.com/data_pickle/ff3daily.pkl'
# ff3 = pd.read_pickle(infile)

# df = ibm.merge(ff3, left_on=ibm.index, right_on=ff3.index)
# df = df.dropna()

# pd.set_option('display.max_columns',None)

# y = df['ret'] - df.RF
# x = df[["MKT_RF", "SMB", "HML"]]

# x = sm.add_constant(x)
# results = sm.OLS(y, x).fit()
# print(results.summary())



'''F-test'''
'''recalling t test and t distribution'''
# df_1 = 473
# alpha = 0.05
# tCritical = stats.t.ppf(alpha,df_1)
# print(tCritical)
'''F-density distribution'''
# x = np.arange(0, 4, 0.01)
# df1 = 20
# df2 = 10

'''y is the probability density distribution'''
'''f distribution has 2 params'''
# y = stats.f.pdf(x, df1, df2)
# plt.title("f_distribution")
# plt.xlabel("x values")
# plt.ylabel("F probability density distribution")
# plt.plot(x, y)
# plt.show()

'''y is the cumulative density distribution'''
# y = stats.f.cdf(x, df1, df2)
# plt.title("f_distribution")
# plt.xlabel("x values")
# plt.ylabel("F cumulative density distribution")
# plt.plot(x, y)
# plt.show()


# sp500 = yf.download("^GSPC", start="2010-01-01", end="2020-12-31", multi_level_index=False)
# ibm = yf.download("ibm", start="2010-01-01", end="2020-12-31", multi_level_index=False)
'''multi_level_index: 是否扁平化处理'''
# ibm['year'] = ibm.index.year
# sp500['mktRet'] = sp500['Close'].pct_change()
# df = ibm.merge(sp500, left_index=True, right_index=True)
# df = df.dropna()

# years = np.unique(df.year)
# betas = []
'''np.unique:排序 + 去重'''

'''to get rolling annual beta'''
# for year in years:
#     df2 = df[df.year == year]
'''keeping the data in the year being traversed'''
#     y = df2["ret"]
#     x = df2['mktRet']
#     x = sm.add_constant(x)
#     results = sm.OLS(y, x).fit()
#     beta = round(results.params[1], 3)
'''params: intercept, slope'''
#     betas.append(beta)
'''beta in CAPM  =  OLS slope in single linear regression'''    

# annualBetas = pd.DataFrame([years, betas]).T
'''pd.DataFrame(): setting different rows(the horizontal one)'''
# annualBetas.columns = ["years", "beta"]
'''setting column index called years and beta'''


'''performance measures'''

'''1: Sharpe ratio'''
'''excess return / total risk'''
# df3 = ibm.merge(ff3, left_index=True, right_index=True)

# meanRet = df3["ret"].mean()
# std = df3["ret"].std()
# meanRF = df3["RF"].mean()
# sharpe = (meanRet - meanRF)/std
# print(f"IBM sharpe ratio is {sharpe}")

'''sharpe ratio in the last 5 years(not rolling)'''

# ibm.shape
'''return:(number of rows; number of columns)'''
# df2 = ibm.tail(1260)    
# df3 = df2.merge(ff3, left_index=True, right_index=True)

# meanRet = df3.ret.mean()
# std = df3.ret.std()
# meanRF = df3.RF.mean()
# sharpe = (meanRet - meanRF)/std  
# print(f"IBM sharpe ratio is {sharpe}")    


'''calculate sharpe ratio at the annual level'''
# ibm['logRet'] = np.log(ibm["Close"].pct_change() + 1)
# annualRet = np.exp(ibm["logRet"].groupby(ibm['year']).sum())
# annualRet2 = pd.DataFrame(annualRet)
# annualRet2.columns = ["annualRet"]

# infile = 'http://datayyy.com/data_pickle/ff3annual.pkl'
# ff3_2 = pd.read_pickle(infile)

# df4 = annualRet2.merge(ff3_2, left_index=True, right_index=True)

# meanRet = round(df4.annualRet.std(), 5)
# std = round(df4.RF.std(), 5)
# meanRF = round(df4.RF.mean(), 5)
# sharpe = round((meanRet - meanRF)/std, 5)

# print(f"IBM sharpe ratio is {sharpe}")


'''2: Treynor Ratio'''
'''excess return / beta'''
# X = np.stack((df4.annualRet, df4.MKT_RF), axis = 0)
# cov = np.cov(X)
# beta = cov[0, 1]/cov[1, 1]

# meanRet = df4.annualRet.mean()
# treynor = (meanRet - meanRF)/beta


'''3: LPSD(下行标准差)'''
# mean = 0.1
# Rf = 0.02
# std = 0.2
# n = 100

# x = np.random.normal(loc = mean,scale = std, size = n)
# std2 = x.std()
# y = x[x-Rf < 0]
'''selecting the x satisfying specific conditions into y'''
# total = 0.0
# for r in y:
#     total += (r - Rf)**2
# LPSD = np.sqrt(total/(63))

'''LPSD in general cases'''
# def LPSD_f(returns, Rm):
#     import numpy as np
#     y = returns[returns < Rm]
#     total = 0.0
#     m = len(y)
#     for r in y:
#         total += (r - Rm)**2
#     var = total/(m-1)
#     LPSD = np.sqrt(var)
#     return LPSD


# annualRiskFree = 0.01
# path = 'http://datayyy.com/data_pickle/'
# infile = path + "ibmMonthly.pkl"
# df5 = pd.read_pickle(infile)
# df5['ret'] = df5["Close"].pct_change()
# rf = annualRiskFree/12
# LPSD = LPSD_f(df.ret, rf)
# print(f"LPSD is: {LPSD}")



'''hypotehsis test'''

# path = 'http://datayyy.com/data_pickle'
# infile = path + "usGDPquarterly.pkl"
# GDP = pd.read_pickle(infile)
# infile2 = path + "ff3monthly.pkl"
# ff3 = pd.read_pickle(infile2)
# print(ff3.head())


'''normal distribution'''
'''pdf, cdf, ppf, random number generator'''
# x = 0.5
# y = stats.norm.cdf(x)
# print(y)


'''alpha = 5%(confidence interval = 95%)'''
# alpha = 0.05
# x = np.arange(-3, 3, 0.15)
# y = stats.norm.pdf(x)

# z1 = stats.norm.ppf(alpha)
# z2 = stats.norm.ppf(1 - alpha)
# plt.vlines(x = z1, ymin = 0, ymax = 0.4, color = 'green', ls='-', label = 'partial height')
# plt.vlines(x = z2, ymin = 0, ymax = 0.4, color = 'green', ls='-', label = 'partial height')
# plt.axhline(y = 0.25, xmin = 0.25, xmax = 0.75, ls='-', color = 'r')
# plt.figtext(0.4, 0.50, "95% CI")
# plt.title("Normal Distribution PDF")
# plt.xlabel("values")
# plt.ylabel("density")
# plt.show()


'''example of two-sided test'''
'''stats.ppf(): to find the critical value'''
# mean = 0.15
# std = 0.03
# n = 300
# x = np.random.normal(mean,std,n)

# sample_mean = np.mean(x)
# alpha = 0.05
# stdErr = std/np.sqrt(n)
# z = stats.norm.ppf(0.5 * alpha)
# marginalErr = abs(z)*stdErr

# lowerBound = sample_mean - marginalErr
# upperBound = sample_mean + marginalErr
# print(f"lowerBound = {lowerBound} and upperBound: {upperBound}")



'''test the equal variances of two samples'''
'''F-test: to test equal variances(sigma1 = sigma2?)'''

# infile = 'http://datayyy.com/data_csv/sleep.csv'
# df = pd.read_csv(infile)

# group1 = df[df.group == 1]
# group2 = df[df.group == 2]
# var1 = group1["extra"].var()
# var2 = group2["extra"].var()

# Fvalue = max(var1, var2)/min(var1, var2)
# df1 = group1.shape[0] - 1
# df2 = group2.shape[0] - 1

# alpha = 0.05
# Fcritical = stats.f.ppf(1 - alpha, df1, df2)
# print(Fcritical)

# if Fvalue > Fcritical:
#     print("reject H0")
# else:
#     print("accept H0")
'''the second and easier method:Levene function'''
# stats.levene(group1.extra, group2.extra)


'''chi-square distribution'''
'''chi-test:to test equal distributions of 2 populations'''


'''test of equal means'''
# mean1 = group1.extra.mean()
# mean2 = group2.extra.mean()

#stats.ttest_ind(a=group1.extra, b=group2.extra, equal_var=True)
#stats.ttest_ind(a=group1.extra, b=group2.extra, equal_var=False)


'''to test if IBM has the same return as SP500'''
# df1 = pd.read_pickle('ibm.pkl')
# df2 = pd.read_pickle('sp500.pkl')

# df1["IBMret"] = df1["Close"].pct_change()
# df2["SP500ret"] = df2["Close"].pct_change()

# df = df1.merge(df2 ,left_on=df1.index, right_on=df2.index)
# df = df.dropna()


# stats.ttest_ind(a = df.IBMret, b = df.SP500ret)
# stats.levene(df.IBMret, df.SP500ret)


'''to test constant annual variance(use IBM as an example)'''
'''stats.levene or F-test'''

# df1['year'] = df.index.year
# ret2012 = df1[df.year==2012].dropna()
# ret2013 = df1[df.year==2013].dropna()
# ret2014 = df1[df.year==2014].dropna()

# stats.levene(ret2012.IBMret, ret2013.IBMret, ret2014.IBMret)



'''time-series test'''
'''Durbin-Watson autocorrelation test'''
'''<2,positively correalated; >2 negatively correlated'''
'''=2: no autocorrelation'''



'''Granger Causality test : what causes what?'''
'''example:chiaken or egg first?'''
# infile = 'http://datayyy.com/data_pickle/chickEgg.pickle'
# df = pd.read_pickle(infile)

# df["chicken_lag1"] = df.chicken.shift(1)
# df["chicken_lag2"] = df.chicken.shift(2)
# df["chicken_lag3"] = df.chicken.shift(3)
# df["egg_lag1"] = df.egg.shift(1)
# df["egg_lag2"] = df.egg.shift(2)
# df["egg_lag3"] = df.egg.shift(3)

# df = df.dropna()
# y = df["egg"]
# x = df[['egg_lag1', 'egg_lag2', 'egg_lag3']]
# x = sm.add_constant(x)
# results = sm.OLS(y, x).fit()
# print(results.summary())

'''相比于蛋解释蛋，加上鸡的信息后，能不能更好地解释蛋'''
'''如果能，那么鸡 granger causes蛋'''
'''怎么看能不能更好地解释：看R2（拟合优度）'''

# x = df[['egg_lag1', 'egg_lag2', 'egg_lag3', "chicken_lag1", "chicken_lag2", "chicken_lag3"]]
# results = sm.OLS(y, x).fit()
# print(results.summary())


'''也要做反向检验，做一组：蛋能否granger causes鸡'''
# y = df["chicken"]
# x = df[['egg_lag1', 'egg_lag2', 'egg_lag3', "chicken_lag1", "chicken_lag2", "chicken_lag3"]]
# results = sm.OLS(y, x).fit()
# print(results.summary())


'''interpolation technique'''
#import pandas as pd 
#import numpy as np 
#nn=np.nan
#x=pd.Series([1,2,nn,nn,6]) 
#print(x)
#print(x.interpolate())


'''test of january effect'''
# # converting to monthly return
# df1['logRet'] = np.log(df1["Close"].pct_change() + 1)
# df['YYYYMM'] = df.index.year * 100 + df.index.month
# retM = np.exp(df['logRet'].groupby(df['YYYYMM']).sum()) - 1

# retM = pd.DataFrame(retM)
# retM.columns = ['retM']

# janRet = []
# nonJanRet = []

# for i in retM.index:
#     mm = i-int(i/1e2)*100#提取末两位数
#     ret = retM[retM.index==i].retM
#     if mm == 1:
#         print(i)
#         janRet.append(ret.values)
#     else:
#         nonJanRet.append(ret.values)

# janRet = pd.DataFrame(janRet)
# nonJanRet = pd.DataFrame(nonJanRet)

# results = stats.ttest_ind(janRet, nonJanRet)
# print(results)



'''###################################################################'''
'''midterm examination'''
'''###################################################################'''



'''porfolio theory'''
'''correlation coefficient; covariance'''
'''相关系数更好：协方差不具有传递性'''


'''random times series with a correlation'''
# np.random.seed(123456)
# n = 1000
# rho = 0.3
# x1 = np.random.normal(size = n)
# x2 = np.random.normal(size = n)
# y1 = x1
# y2 = rho * x1 + np.sqrt(1-rho**2) * x2
# print(np.corrcoef(y1, y2))


'''2-stock variance formula'''

def var2stock(wA, wB, varA, varB, covAB):
    wB = 1 - wA
    var = wA**2*varA + wB**2*varB + 2*wA*wB*covAB
    return var

'''calculate the volatility of returns of a given stock'''
def volatility_stock(ticker, date1, date2):
    df = yf.download(ticker, start = date1, end = date2)
    df['ret'] = df["Adj Close"].pct_change()
    std = df.std()
    return std


'''optimization'''
'''stochastic gradient descent'''
# x = np.arange(-5, 5, 0.01)
# a = 3.2
# b = 5.0
# y = a + b*x**2
# plt.plot(x, y)
# plt.title("function shape of y")
# plt.ylabel("y")
# plt.xlabel("x")
# plt.show()

'''convection function minimization'''
def func(x):
    return 3.2 + 5*x**2
# this defines the objective function you want to minimize

x0 = 100
# purpose: optimization algorithms need a place to start

# result = minimize(func, x0, method="nelder-mead", tol=1e-6)
'''tol:the range that python stop searching'''
# print(result)


'''Lambda function'''
'''a definition of multivariable function8'''
# fun = lambda x: (x[0] - 10)**2 + (x[1]-25)**2
# x = (11, 27)
# fun(x)

'''two input parameters and lambda function'''
# fun1 = lambda x: (x[0] - 1)**2 + (x[1]-2.5)**2

# bounds = ((0, None), (0, None))#规定两个参数的下界与上界
# cons = ({'type': 'ineq', 'fun': lambda x : x[0] - 2*x[1]**2}, 
#               {'type': 'ineq', 'fun': lambda x : -x[0] - 2*x[1] + 6},
#               {'type': 'ineq', 'fun': lambda x : x[0] - 2*x[1] + 2})
# # fun >= 0

# results = minimize(fun1, (2, 0), method = 'SLSQP',  bounds = bounds, constraints = cons)
'''SLSQP:序列最小二乘规划'''

'''scipy.optimize.brent() function from optimize module'''
'''用brent方法去寻找极值'''
# a = 3.4
# b = 2
# c = 0.8
# def f(x):
#     return a - b * np.exp(-(x - c)**2)

# x = np.arange(-3, 3, 0.1)
# y = f(x)
# '''find the minimum'''
# solution = scipy.optimize.brent(f)
# print(solution)


'''n-stock performance'''

'''calculate the sharpe ratio of multiple stocks'''
# tickers = ('IBM', 'WMT', 'C')
# begdate = '2010-1-1'
# enddate = '2012-12-31'

# rf = 0.02

# n = len(tickers)

#step1: annual return of the portfolio
# def ret_annual(ticker, begdate, enddate):
#     df = yf.download(ticker, begdate, enddate)
#     df['logret'] = np.log(1 + df['Close'].pct_change())
#     df['year'] = df.index.year
#     retAnnual = np.exp(df['logret'].groupby(df['year']).sum() - 1)
#     retAnnual = pd.DataFrame(retAnnual)
#     retAnnual.columns = ['ret_' + ticker]
#     return retAnnual    
    
#step2: estimate portfolio variance
# def porfolio_var(R, w):
#     cor = np.corrcoef(R.T)
#     std_dev = np.std(R, axis=0)
#     var = 0
#     for i in np.arange(n):
#         for j in np.arange(n):
#             var += w[i]*w[j]*std_dev[i]*std_dev[j]*cor[i, j]
#     return var

#step3: construct a function to calculate sharpe ratio
# def sharperatio(R, w):
#     var = porfolio_var(R, w)
#     mean_return = np.mean(R, axis=0)
#     ret = np.array(mean_return)
#     return (np.dot(w,ret) - rf)/np.sqrt(var)

#step4: give n-1 weights which will return a sharpe ratio
'''基于前n-1个权重自动算出第n个权重，然后据此计算完整的夏普比率'''
'''因为所有权重和为1，自由度只有 n-1。优化器只需搜索 n-1 个权重，最后一个自动确定，自动满足和为1'''
# def sharperatio_n_minus_1_stocks(R, w):
#     w2 = np.append(w, 1-sum(w))
#     return sharperatio(R, w2)


# x2 = ret_annual(tickers[0], begdate, enddate)
# for ticker in tickers[1:]:
#     x_ = ret_annual(ticker, begdate, enddate)
#     x2 = x2.merge(x_, left_on=x2.index, right_on=x_.index)
#     x2.index = x2['key_0']
#     del x2['key_0']

# R = np.array(x2)
# print(f"efficient portfolio (mean-variance) :ticker used {tickers}")
# print('Sharpe ratio for an equal-weighted portfolios')
# equal_w = np.ones(n, dtype=float)*1.0/n
# sharpe_equal_weights = sharperatio(R, equal_w)

# print(f"sharpe ratio with equal weight = {sharpe_equal_weights}")
'''we use equal weights sharpe ratio as a benchmark'''

# for n stocks, we could choose n-1 weights
'''maximize object function'''


# w0 = np.ones(n-1, dtype=float)*1.0/n
# w1=fmax(sharperatio_n_minus_1_stocks, w0)
'''以w0（等权重）为基准，对sharperatio_n_minus_1_stocks函数进行fmax优化'''
# optimal_w = np.append(w1, 1-sum(w1))

# optimal_sharpe_ratio = sharperatio(R, optimal_w)

#print out the results under the optimized weights
# print(f"optimal weight are {optimal_w}")
# print(f"final sharpe ratio is {optimal_sharpe_ratio}")




'''options and futures'''

'''call options'''
'''strike price and underlying price'''
def payoff_call(strike, underlying):
    return (strike - underlying + abs(strike - underlying))/2
'''graph'''
# underlying= 50
# strike = np.arange(0, 100, 5)
# payoff = payoff_call(strike, underlying)
# plt.plot(strike, payoff)
# plt.title("payoff of long call")
# plt.xlabel("stock price")
# plt.ylabel("payoff")
# plt.show()

'''c:premium of a option'''
def profit_loss_call(strike, underlying, c):
    return (strike - underlying + abs(strike - underlying))/2 - c

'''put options'''
def payoff_put(strike, underlying):
    return (abs(underlying - strike) + underlying - strike)/2


'''European option vs American option'''
'''american option:more flexible'''


'''Black-Scholes-Merton call'''
'''c/p = option price(premium)'''

'''收到股票的期望现值 - 支付行权价的期望现值 = 期权价'''
def bs_call(stockPrice, exercisePrice, time, rate, sigma):
    d1 = (log(stockPrice/exercisePrice) + (rate+ sigma*sigma/2)*time)/(sigma * sqrt(time))
    d2 = d1 - sigma*sqrt(time)
    c = stockPrice*stats.norm.cdf(d1) - exercisePrice*exp(-rate*time)*stats.norm.cdf(d2)
    return c

def bs_put(stockPrice, exercisePrice, time, rate, sigma):
    d1 = (log(stockPrice/exercisePrice) + (rate+ sigma*sigma/2)*time)/(sigma * sqrt(time))
    d2 = d1 - sigma*sqrt(time)
    p = - stockPrice*stats.norm.cdf(-d1) + exercisePrice*exp(-rate*time)*stats.norm.cdf(-d2)
    return p

'''implied volatility:current option price into bs model to get a volitility(sigma)'''
'''"risk neutral hypothesis"'''
'''using loop to get closer to the reality'''
def implied_vol_call(S, X, T, r, c):
    for i in range(200):
        sigma = 0.005 * (i + 1)
        d1 = (log(S/X) + (r+ sigma*sigma/2)*T)/(sigma * sqrt(T))
        d2 = d1 - sigma*sqrt(T)
        diff = c - (S*stats.norm.cdf(d1) - X*exp(-r*T)*stats.norm.cdf(d2))
        if abs(diff) <= 0.01:
            print("i, sigma, diff")
            sigma = round(sigma, 7)
            diff = round(diff, 7)
            return(i, sigma, diff)

# print(implied_vol_call(10, 10, 0.5, 0.01, 2))


def implied_vol_put_min(S, X, T, r, p):
    implied_vol = 1.0
    min_value = 100.0
    for i in np.arange(1, 10000):
        sigma = 0.0001 * (i + 1) 
        d1 = (log(S/X) + (r+ sigma*sigma/2)*T)/(sigma * sqrt(T))
        d2 = d1 - sigma*sqrt(T)
        put = - S*stats.norm.cdf(-d1) + X*exp(-r*T)*stats.norm.cdf(-d2)
        abs_diff = abs(put - p)
        if abs_diff <= min_value:
            min_value = abs_diff
            implied_vol = sigma
            k = i
        put_out = put
    print("k, implied_vol, put, abs_diff")
    return(k, implied_vol, put_out, min_value)
            

'''exchange rate'''
'''if there is a exchange rate volatility in the market'''
'''we need to calculate the return based on the future exchange rate'''
'''exchange rate futures arbitrage'''

'''you need to pay in three months'''
obligationForeign = 1.9

'''future exchange rate'''
f = 1.26
'''given today's exchange rate'''
s0 = 1.25

'''different interest rates'''
# rHome = 0.01
# rForeign = 0.02

# T = 3/12

# todayObligationForeign = obligationForeign * exp(-rForeign*T)
# usBorrow = todayObligationForeign * s0
# costDollarBorrow = usBorrow *exp(rHome*T)
# profit = f *obligationForeign - costDollarBorrow
# print(profit)


'''option Greeks'''
'''Delta, Gamma, Theta, Vega, Rho'''
'''an example of Delta(which is norm.cdf(d1))'''

def bsCall(S, X, T, r, sigma):
        d1 = (log(S/X) + (r + sigma*sigma/2)*T)/(sigma * sqrt(T))
        d2 = d1 - sigma*sqrt(T)
        return S*stats.norm.cdf(d1) - X*exp(-r*T)*stats.norm.cdf(d2)

'''the first method:use math formula(no bias)'''
def delta1_f(S, X, T, r, sigma):
    d1 = (log(S/X) + (r + sigma*sigma/2)*T)/(sigma * sqrt(T))
    delta = stats.norm.cdf(d1)
    return(delta)

'''second method: approaching(have bias)'''
'''we borrow the grid method idea from before'''
def delta2_f(S, X, T, r, sigma):
    tiny = 1e-5
    s1 = S
    s2 = S + tiny
    c1 = bsCall(s1, X, T, r, sigma)
    c2 = bsCall(s2, X, T, r, sigma)
    delta = (c2 - c1)/(s2 - s1)
    return delta

delta1 = delta1_f(10, 10, 0.5, 0.01, 0.02)
delta2 = delta2_f(10, 10, 0.5, 0.01, 0.02)
print(delta1, delta2)


'''volatility smile: strike price and implied volatility'''
'''implied volatility is not constant across different strike prices'''

# infile = "callsfor15mar2024.txt"
# calls = pd.read_table(infile)

ticker = 'IBM'
r = 0.0003
begdate = "2024-1-1"
enddate = "2024-3-1"
enddate2 = datetime.date(2024,3,1)

def implied_vol_call_min(S, X, T, r, c):
    implied_vol = 1.0
    min_value = 100
    for i in range(10000):
        sigma = 0.0001 * (i + 1)
        d1 = (log(S/X) + (r + sigma*sigma/2)*T)/(sigma * sqrt(T))
        d2 = d1 - sigma*sqrt(T)
        c2 = S * stats.norm.cdf(d1) - X*exp(-r*T) * stats.norm.cdf(d2)
        abs_diff = abs(c2 - c)
        if abs_diff < min_value:
            min_value = abs_diff
            implied_vol = sigma
    return implied_vol


#to get the stock data
#df = yf.download(ticker, begdate, enddate)
# df = pd.read_pickle("ibm.pkl")

# # to get the option data
# first_contract = calls["Contract Name"].iloc[0]
# date_str = first_contract[len(ticker):len(ticker) +6]

# exp_date0 = int("20" + date_str)

# s = float(df["Close"].iloc[-1])

# y = int(exp_date0/10000)
# m = int(exp_date0/100) - y*100
# d = exp_date0 - y*10000 - m*100

# #get the exact expiring date
# exp_date = datetime.date(y, m, d)
# T = (exp_date - enddate2).days/252.0

# #run a loop to estimate the implied volatility for each option
# n = len(calls["Strike"]) # the number of strikes

# #initialization
# strike = []
# implied_vol = []
# call2 = []
# x_old = 0

# for i in range(n):
#     x = calls["Strike"].iloc[i]
#     c = (calls["Bid"].iloc[i] + calls["Ask"].iloc[i])/2

#     if c > 0:
#         print(f"i: {i}, call price: {c}")
#         if x != x_old:
#             vol = implied_vol_call_min(s, x, T, r, c)
#             strike.append(x)
#             implied_vol.append(vol)
#             call2.append(c)
#             print(x, c, vol)
#             x_old = x

# # plotting the volatility smile
# plt.plot(strike, implied_vol, marker = "o", linestyle = "-")
# plt.title("volatility smile")
# plt.xlabel("strike price")
# plt.ylabel("implied volatility")
# plt.grid(True)
# plt.show()



'''sqlite basics'''
'''connect to a database'''
conn = sqlite3.connect(':memory:')

cursor = conn.cursor()

'''create some mock data'''
cursor.execute('''
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    dept_name TEXT
)
''')

cursor.execute('''
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    dept_id INTEGER,
)
''')

cursor.executemany('INSERT INTO departments VALUES (?, ?)', [
    ('10','ENG'),
    ('20','HR'),
    ('30','MKT')
    ])

cursor.executemany('INSERT INTO employees VALUES (?, ?, ?)', [
    ('1', 'Alice', '10'),
    ('2', 'Bob', '20'),
    ('3', 'Charlie', 'None')
])

inner_join_query = '''
    SELECT employees.name, departments.dept_name
    FROM employees
    INNER JOIN departments ON employees.dept_id = departments.id
'''

cursor.execute(inner_join_query)

df = pd.read_sql_query(inner_join_query, conn)
df.to_csv("results.csv", index=False)

# do not forget to close the connection
conn.close()