# Source Code Coverage Matrix

This audit treats the instructor's classroom script as an independent source, not merely an appendix to the slides.

## Reconciled Major Modules

| Source lines | Classroom code family | Destination | Reconciliation |
|---|---|---|---|
| 19-45 | Package inspection; annuities; delayed perpetuity; NPV and IRR | Chapters 2-3 | Integrated |
| 48-107 | Data download workflow; returns; ticker column; CSV/pickle; missing values; aggregation; t-tests; histogram | Chapter 4 | Integrated |
| 110-207 | Effective rates; APR conversion; continuous compounding; credit spreads; term structure; bond price; YTM; duration; stock valuation | Chapter 5 | Integrated |
| 210-292 | CAPM; linregress; OLS; regression chart; joins; adjusted prices; t distribution | Chapters 6 and 8 | Integrated |
| 295-474 | Fama-French regression; F distribution; rolling beta; Sharpe; Treynor; LPSD | Chapter 7 | Integrated |
| 475-673 | Confidence intervals; F/Levene/t tests; Durbin-Watson; bidirectional Granger; interpolation; January effect | Chapter 8 | Integrated |
| 680-848 | Portfolio variance, constrained optimization, and maximum-Sharpe portfolios | Chapter 7 extension / later portfolio chapter | Core Sharpe optimization integrated; full portfolio theory reserved |
| 849-1065 | Option payoffs, Black-Scholes, implied volatility, FX futures, Greeks, volatility smile | Later options chapter; Assignment 3 previews | Not part of Chapters 1-8 |
| 1067-1115 | SQLite joins | Later database topic; Assignment 3 | Assignment example integrated |
| 1117-1380 | Parametric, historical, modified VaR, expected shortfall, and portfolio volatility | Later risk-management chapter | Not part of Chapters 1-8 |
| 1381-1580 | Monte Carlo, stock paths, option simulation, barrier option, simulation VaR | Later simulation chapter | Not part of Chapters 1-8 |
| 1582-end | Long-horizon arithmetic/geometric return comparison | Later forecasting topic | Not part of Chapters 1-8 |

## Raw Labeled-Block Inventory

The table below is an automated fine-grained inventory. Short inline comments may be flagged separately even when their surrounding module is integrated; use the reconciled table above for chapter-level coverage.

| Source line | Classroom topic | Destination | Status before detailed reconciliation |
|---:|---|---|---|
| 19 | showing the functions of a package | Chapter 2 | Covered |
| 23 | time value of money | Chapter 3 | Covered |
| 26 | annuity | Chapter 3 | Covered |
| 27 | fixed or growing | Manual review | Covered |
| 28 | perpetuity or not | Chapter 3 | Covered |
| 29 | due or not | Manual review | Review/Add |
| 36 | first annuity paid after k years | Chapter 3 | Covered |
| 41 | NPV and IRR | Chapter 3 | Review/Add |
| 48 | download data | Chapter 4 | Review/Add |
| 50 | calculating daily returns | Chapter 4 | Covered |
| 52 | add a column and name it | Manual review | Covered |
| 54 | saving the file | Manual review | Covered |
| 55 | save your data to a pickle format | Manual review | Covered |
| 57 | save to a csv format | Manual review | Covered |
| 59 | drop blank data | Manual review | Covered |
| 61 | testing whether the mean is statistically equal to 0 | Manual review | Covered |
| 66 | convert daily return to yearly return | Chapter 4 | Covered |
| 67 | default index of yfinance dataframe: date | Manual review | Covered |
| 72 | convert daily return to monthly return | Chapter 4 | Covered |
| 79 | Fama-French 3-factors | Manual review | Covered |
| 85 | t-test | Chapter 4 | Covered |
| 86 | ttest_ind and ttest_1samp | Manual review | Covered |
| 98 | return distribution visualization | Chapter 4 | Covered |
| 110 | bond and stock valuation | Chapter 5 | Covered |
| 111 | effective rate: annually | Chapter 5 | Covered |
| 113 | this is EAR in annually compounded | Manual review | Covered |
| 114 | formula should be remembered | Manual review | Covered |
| 121 | this is to change APR to one that is different periodically compounded | Manual review | Covered |
| 122 | in order to compare bonds with different payment frequency | Manual review | Covered |
| 123 | second effective rate | Chapter 5 | Covered |
| 131 | APR2 = EAR2 * m2 | Manual review | Review/Add |
| 132 | APR is a kind of stated interest rate | Manual review | Covered |
| 133 | IRR, we use npf.irr() to calculate | Manual review | Review/Add |
| 139 | single annual rate to continuous compounding rate | Manual review | Covered |
| 140 | EAR limited | Manual review | Review/Add |
| 146 | credit rate of bonds | Chapter 5 | Covered |
| 152 | time structure of bonds | Manual review | Covered |
| 162 | pricing zero coupon bond | Chapter 5 | Covered |
| 163 | annual interest rate is 5% | Manual review | Covered |
| 164 | ten years:12*10 | Manual review | Covered |
| 165 | every monnth you deposit 100, lasting 10 years | Manual review | Covered |
| 169 | calculating YTM | Chapter 5 | Review/Add |
| 170 | npf params: rate, period, pmt, pv, fv; when=begin/end(default end) | Manual review | Covered |
| 179 | calculating duration (Marcauly) | Chapter 5 | Review/Add |
| 180 | focus on the formula | Manual review | Covered |
| 198 | modified duration:calculated from Marcauly duration | Chapter 5 | Covered |
| 199 | Dmodified = D/(1 + YTM/freq) | Chapter 5 | Review/Add |
| 202 | pricing a stock: 2 periods | Chapter 5 | Covered |
| 210 | CAPM model | Chapter 6 | Covered |
| 214 | linear regression | Chapter 6 | Covered |
| 215 | Y = alpha + beta*X | Manual review | Covered |
| 216 | method 1:stats.linregress(X, Y) | Manual review | Covered |
| 220 | method 2: using OLS(Y, X) | Manual review | Review/Add |
| 225 | linear regression model visualization | Chapter 6 | Covered |
| 238 | join: left, right, inner, outer(union) | Chapter 6 | Covered |
| 239 | default:inner | Manual review | Covered |
| 240 | recalling SQL | Manual review | Review/Add |
| 247 | distinguishing Close and Adj Close | Chapter 6 | Covered |
| 248 | use stock prices from 2 stocks to measure the CAPM | Chapter 6 | Covered |
| 251 | creating new column called ret in IBM Dataframe | Manual review | Review/Add |
| 255 | drop blank data | Manual review | Covered |
| 261 | T-density distribution(t distribution) | Manual review | Covered |
| 262 | confidence interval = 1 - alpha | Manual review | Covered |
| 263 | alpha: significance level | Manual review | Covered |
| 269 | drawing T probability density function | Manual review | Covered |
| 270 | for i in a: | Manual review | Review/Add |
| 271 | b = i/10 | Manual review | Review/Add |
| 272 | x.append(b) | Manual review | Covered |
| 273 | y.append(stats.t.pdf(b, dfreedom)) | Manual review | Covered |
| 278 | pdf: probability density function | Manual review | Covered |
| 279 | cdf: cumulative density function | Manual review | Covered |
| 280 | ppf: inverse function of cdf(given probability, got value) | Manual review | Covered |
| 283 | using the statsmodels function | Manual review | Review/Add |
| 292 | params: intercept, slope | Manual review | Covered |
| 295 | multivariable models and performance measures | Chapter 7 | Covered |
| 297 | Fama French | Chapter 7 | Covered |
| 321 | F-test | Manual review | Covered |
| 322 | recalling t test and t distribution | Manual review | Covered |
| 327 | F-density distribution | Manual review | Review/Add |
| 332 | y is the probability density distribution | Manual review | Covered |
| 333 | f distribution has 2 params | Manual review | Review/Add |
| 341 | y is the cumulative density distribution | Manual review | Covered |
| 352 | multi_level_index: 是否扁平化处理 | Manual review | Review/Add |
| 360 | np.unique:排序 + 去重 | Manual review | Covered |
| 362 | to get rolling annual beta | Chapter 6 | Covered |
| 363 | for year in years: | Manual review | Covered |
| 364 | df2 = df[df.year == year] | Manual review | Covered |
| 365 | keeping the data in the year being traversed | Manual review | Covered |
| 366 | y = df2["ret"] | Manual review | Review/Add |
| 367 | x = df2['mktRet'] | Manual review | Review/Add |
| 368 | x = sm.add_constant(x) | Manual review | Review/Add |
| 369 | results = sm.OLS(y, x).fit() | Manual review | Review/Add |
| 370 | beta = round(results.params[1], 3) | Manual review | Covered |
| 371 | params: intercept, slope | Manual review | Covered |
| 372 | betas.append(beta) | Manual review | Covered |
| 373 | beta in CAPM = OLS slope in single linear regression | Chapter 6 | Covered |
| 376 | pd.DataFrame(): setting different rows(the horizontal one) | Manual review | Covered |
| 378 | setting column index called years and beta | Manual review | Covered |
| 381 | performance measures | Chapter 7 | Covered |
| 383 | 1: Sharpe ratio | Chapter 7 | Covered |
| 384 | excess return / total risk | Manual review | Covered |
| 393 | sharpe ratio in the last 5 years(not rolling) | Chapter 7 | Covered |
| 396 | return:(number of rows; number of columns) | Manual review | Covered |
| 407 | calculate sharpe ratio at the annual level | Chapter 7 | Covered |
| 426 | 2: Treynor Ratio | Chapter 7 | Covered |
| 427 | excess return / beta | Manual review | Covered |
| 436 | 3: LPSD(下行标准差) | Chapter 7 | Covered |
| 445 | selecting the x satisfying specific conditions into y | Manual review | Covered |
| 451 | LPSD in general cases | Chapter 7 | Review/Add |
| 475 | hypotehsis test | Chapter 8 | Review/Add |
| 485 | normal distribution | Chapter 8 | Covered |
| 486 | pdf, cdf, ppf, random number generator | Manual review | Covered |
| 492 | alpha = 5%(confidence interval = 95%) | Manual review | Covered |
| 509 | example of two-sided test | Manual review | Covered |
| 510 | stats.ppf(): to find the critical value | Manual review | Covered |
| 528 | test the equal variances of two samples | Chapter 8 | Covered |
| 529 | F-test: to test equal variances(sigma1 = sigma2?) | Chapter 8 | Covered |
| 547 | if Fvalue > Fcritical: | Manual review | Review/Add |
| 548 | print("reject H0") | Manual review | Covered |
| 549 | else: | Manual review | Covered |
| 550 | print("accept H0") | Manual review | Covered |
| 551 | the second and easier method:Levene function | Manual review | Covered |
| 555 | chi-square distribution | Manual review | Covered |
| 556 | chi-test:to test equal distributions of 2 populations | Manual review | Covered |
| 559 | test of equal means | Chapter 8 | Covered |
| 567 | to test if IBM has the same return as SP500 | Manual review | Covered |
| 582 | to test constant annual variance(use IBM as an example) | Later: Risk Management | Covered |
| 583 | stats.levene or F-test | Manual review | Covered |
| 594 | time-series test | Chapter 8 | Covered |
| 595 | Durbin-Watson autocorrelation test | Manual review | Covered |
| 596 | <2,positively correalated; >2 negatively correlated | Manual review | Review/Add |
| 597 | =2: no autocorrelation | Manual review | Covered |
| 601 | Granger Causality test : what causes what? | Chapter 8 | Covered |
| 602 | example:chiaken or egg first? | Manual review | Review/Add |
| 620 | 相比于蛋解释蛋，加上鸡的信息后，能不能更好地解释蛋 | Manual review | Review/Add |
| 621 | 如果能，那么鸡 granger causes蛋 | Chapter 8 | Covered |
| 622 | 怎么看能不能更好地解释：看R2（拟合优度） | Manual review | Review/Add |
| 629 | 也要做反向检验，做一组：蛋能否granger causes鸡 | Chapter 8 | Covered |
| 636 | interpolation technique | Chapter 8 | Review/Add |
| 645 | test of january effect | Chapter 8 | Covered |
| 657 | for i in retM.index: | Manual review | Covered |
| 658 | mm = i-int(i/1e2)*100#提取末两位数 | Manual review | Review/Add |
| 659 | ret = retM[retM.index==i].retM | Manual review | Covered |
| 660 | if mm == 1: | Manual review | Review/Add |
| 661 | print(i) | Manual review | Covered |
| 662 | janRet.append(ret.values) | Manual review | Covered |
| 663 | else: | Manual review | Covered |
| 664 | nonJanRet.append(ret.values) | Manual review | Covered |
| 674 | ################################################################### | Manual review | Review/Add |
| 675 | midterm examination | Manual review | Review/Add |
| 676 | ################################################################### | Manual review | Review/Add |
| 680 | porfolio theory | Later: Portfolio Theory | Review/Add |
| 681 | correlation coefficient; covariance | Later: Risk Management | Covered |
| 682 | 相关系数更好：协方差不具有传递性 | Manual review | Review/Add |
| 685 | random times series with a correlation | Manual review | Covered |
| 696 | 2-stock variance formula | Later: Portfolio Theory | Covered |
| 703 | calculate the volatility of returns of a given stock | Manual review | Covered |
| 711 | optimization | Later: Portfolio Theory | Covered |
| 712 | stochastic gradient descent | Manual review | Review/Add |
| 723 | convection function minimization | Manual review | Review/Add |
| 726 | this defines the objective function you want to minimize | Manual review | Covered |
| 729 | purpose: optimization algorithms need a place to start | Later: Portfolio Theory | Covered |
| 732 | tol:the range that python stop searching | Manual review | Covered |
| 736 | Lambda function | Chapter 1 | Covered |
| 737 | a definition of multivariable function8 | Chapter 7 | Review/Add |
| 742 | two input parameters and lambda function | Chapter 1 | Covered |
| 752 | SLSQP:序列最小二乘规划 | Manual review | Covered |
| 754 | scipy.optimize.brent() function from optimize module | Chapter 2 | Covered |
| 755 | 用brent方法去寻找极值 | Manual review | Review/Add |
| 764 | find the minimum | Manual review | Review/Add |
| 769 | n-stock performance | Later: Portfolio Theory | Review/Add |
| 771 | calculate the sharpe ratio of multiple stocks | Chapter 7 | Covered |
| 780 | step1: annual return of the portfolio | Chapter 4 | Covered |
| 790 | step2: estimate portfolio variance | Later: Risk Management | Covered |
| 800 | step3: construct a function to calculate sharpe ratio | Chapter 7 | Covered |
| 807 | step4: give n-1 weights which will return a sharpe ratio | Chapter 7 | Covered |
| 808 | 基于前n-1个权重自动算出第n个权重，然后据此计算完整的夏普比率 | Manual review | Review/Add |
| 809 | 因为所有权重和为1，自由度只有 n-1。优化器只需搜索 n-1 个权重，最后一个自动确定，自动满足和为1 | Manual review | Review/Add |
| 829 | we use equal weights sharpe ratio as a benchmark | Chapter 7 | Covered |
| 831 | for n stocks, we could choose n-1 weights | Manual review | Covered |
| 832 | maximize object function | Manual review | Covered |
| 837 | 以w0(等权重)为基准,对sharperatio_n_minus_1_stocks函数进行fmax优化 | Chapter 7 | Review/Add |
| 842 | print out the results under the optimized weights | Manual review | Covered |
| 849 | options and futures | Later: Options and Futures | Review/Add |
| 851 | call options | Later: Options and Futures | Review/Add |
| 852 | strike price and underlying price | Manual review | Covered |
| 855 | graph | Manual review | Covered |
| 865 | c:premium of a option | Manual review | Review/Add |
| 869 | put options | Later: Options and Futures | Review/Add |
| 874 | European option vs American option | Manual review | Review/Add |
| 875 | american option:more flexible | Manual review | Review/Add |
| 878 | Black-Scholes-Merton call | Later: Options and Futures | Review/Add |
| 879 | c/p = option price(premium) | Manual review | Covered |
| 881 | 收到股票的期望现值 - 支付行权价的期望现值 = 期权价 | Manual review | Review/Add |
| 894 | implied volatility:current option price into bs model to get a volitility(sigma) | Later: Options and Futures | Covered |
| 895 | "risk neutral hypothesis" | Chapter 8 | Covered |
| 896 | using loop to get closer to the reality | Manual review | Review/Add |
| 930 | exchange rate | Later: Options and Futures | Review/Add |
| 931 | if there is a exchange rate volatility in the market | Later: Options and Futures | Covered |
| 932 | we need to calculate the return based on the future exchange rate | Later: Options and Futures | Covered |
| 933 | exchange rate futures arbitrage | Later: Options and Futures | Review/Add |
| 935 | you need to pay in three months | Manual review | Covered |
| 938 | future exchange rate | Later: Options and Futures | Covered |
| 940 | given today's exchange rate | Later: Options and Futures | Covered |
| 943 | different interest rates | Manual review | Covered |
| 956 | option Greeks | Later: Options and Futures | Review/Add |
| 957 | Delta, Gamma, Theta, Vega, Rho | Manual review | Review/Add |
| 958 | an example of Delta(which is norm.cdf(d1)) | Manual review | Covered |
| 965 | the first method:use math formula(no bias) | Manual review | Covered |
| 971 | second method: approaching(have bias) | Manual review | Covered |
| 972 | we borrow the grid method idea from before | Manual review | Covered |
| 987 | volatility smile: strike price and implied volatility | Later: Options and Futures | Covered |
| 988 | implied volatility is not constant across different strike prices | Later: Options and Futures | Covered |
| 1014 | to get the stock data | Manual review | Covered |
| 1043 | for i in range(n): | Manual review | Covered |
| 1044 | x = calls["Strike"].iloc[i] | Manual review | Review/Add |
| 1045 | c = (calls["Bid"].iloc[i] + calls["Ask"].iloc[i])/2 | Manual review | Review/Add |
| 1047 | if c > 0: | Manual review | Review/Add |
| 1048 | print(f"i: {i}, call price: {c}") | Manual review | Covered |
| 1049 | if x != x_old: | Manual review | Review/Add |
| 1050 | vol = implied_vol_call_min(s, x, T, r, c) | Manual review | Review/Add |
| 1051 | strike.append(x) | Manual review | Review/Add |
| 1052 | implied_vol.append(vol) | Manual review | Review/Add |
| 1053 | call2.append(c) | Manual review | Review/Add |
| 1054 | print(x, c, vol) | Manual review | Covered |
| 1055 | x_old = x | Manual review | Review/Add |
| 1067 | sqlite basics | Later: Databases | Review/Add |
| 1068 | connect to a database | Manual review | Review/Add |
| 1073 | create some mock data | Manual review | Covered |
| 1074 | CREATE TABLE departments ( id INTEGER PRIMARY KEY, dept_name TEXT ) | Manual review | Covered |
| 1081 | CREATE TABLE employees ( id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, ) | Manual review | Covered |
| 1101 | SELECT employees.name, departments.dept_name FROM employees INNER JOIN departments ON employees.dept_id = departments.id | Chapter 6 | Covered |
| 1112 | do not forget to close the connection | Manual review | Covered |
| 1119 | to get the value of 100 shares of IBM stock | Manual review | Covered |
| 1130 | to calculate VaR next day for 100 shares of IBM stock | Later: Risk Management | Covered |
| 1149 | simplified VaR calculation | Later: Risk Management | Review/Add |
| 1155 | modified VaR calculation | Later: Risk Management | Covered |
| 1156 | not all the returns are normally distributed, we need to consider skewness and kurtosis | Manual review | Covered |
| 1171 | 10days VaR | Later: Risk Management | Review/Add |
| 1197 | shapiro wilk test | Manual review | Covered |
| 1198 | test if the data is normally distributed | Manual review | Covered |
| 1200 | anderson darling test | Manual review | Covered |
| 1201 | test if the data is from a specific distribution | Manual review | Covered |
| 1204 | normality test for WMT's daily returns | Chapter 4 | Covered |
| 1210 | VaR for the next day by sorting | Later: Risk Management | Review/Add |
| 1225 | 10 day VaR by sorting | Later: Risk Management | Review/Add |
| 1242 | calculate skewness and kurtosis | Manual review | Review/Add |
| 1261 | nVaR for one day | Later: Risk Management | Review/Add |
| 1270 | modified VaR based on 4 moments | Later: Risk Management | Covered |
| 1281 | expected shortfall | Later: Risk Management | Review/Add |
| 1295 | volitility of 2-stock portfolio | Manual review | Covered |
| 1306 | to randomly generate two datasets to calculate the volatility of the portfolio | Manual review | Covered |
| 1329 | a real-world example: calculate the volatility of a portfolio of IBM and WMT stocks | Manual review | Covered |
| 1351 | volatility of a portfolio | Manual review | Covered |
| 1369 | vol of n-stock portfolio (simulated returns) | Manual review | Covered |
| 1381 | monte carlo simulation | Later: Monte Carlo Simulation | Review/Add |
| 1386 | randomly select 10 stocks among NYSE stocks | Manual review | Review/Add |
| 1396 | roll a dice function | Later: Monte Carlo Simulation | Covered |
| 1406 | the permutation steps in randomization | Manual review | Review/Add |
| 1413 | simulation of stock terminal price movements | Later: Monte Carlo Simulation | Covered |
| 1439 | call simulation | Later: Monte Carlo Simulation | Covered |
| 1466 | path of stock price change | Later: Monte Carlo Simulation | Covered |
| 1494 | correlated random series | Later: Monte Carlo Simulation | Covered |
| 1509 | calculating mean and std then simulate | Manual review | Covered |
| 1533 | up and out call | Later: Monte Carlo Simulation | Covered |
| 1560 | linking two methods for VaR using simulation | Later: Risk Management | Covered |
| 1568 | method 1: using the mean and std to calculate VaR | Later: Risk Management | Covered |
| 1572 | method 2: monte carlo simulation | Later: Monte Carlo Simulation | Review/Add |
| 1582 | long-term return comparison | Manual review | Covered |
| 1583 | choose aristic return or geometric return? | Manual review | Covered |
