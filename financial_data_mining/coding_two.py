# -*- coding: utf-8 -*-
"""
Created on Date and Time:

YOUR NAME:陈晗之
YOUR ID:2312410011
"""

"""
Make sure you have install all the modules need for this class

"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Exercise Two
"""
#define your directory first
import os
os.chdir("C:\\Users\\KevinChen\\Desktop\\my_python")


# =============================================================================
# MODULE 1: Bond Valuation and Sensitivity Analysis
# =============================================================================
import numpy_financial as npf

def bond_price(fv, coupon_rate, ytm, years, freq):
    # Your code here
    bondPrice = -npf.pv(ytm/freq, years*freq, fv*coupon_rate/freq, fv)
    return bondPrice
    pass

def calculate_duration(fv, coupon_rate, ytm, years, freq):
    # Your code here
    n = years*freq
    coupon = fv * coupon_rate/freq
    B = bond_price(fv, coupon_rate, ytm, years, freq)
    D = 0
    for i in range(1, n + 1):
        t = i/freq
        if i == n:
            cf = coupon + fv
        else:
            cf = coupon
        weight = -npf.pv(ytm/freq, i, 0, cf) / B
        D += weight * t        
    return D

# Parameters
fv = 1000
coupon = 0.07
years = 10
freq = 2

# Calculate for YTM = 5% and 8%

ytm1 = 0.05
print(calculate_duration(fv, coupon, ytm1, years, freq))
ytm2 = 0.08
print(calculate_duration(fv, coupon, ytm2 , years, freq))


# =============================================================================
# MODULE 2: CAPM Beta Estimation for Tech Stocks
# =============================================================================
import yfinance as yf
import pandas as pd
import statsmodels.api as sm

# 1. Download Data

AAPL = yf.download("AAPL", start = "2025-01-01", end = "2025-12-31")
sp500 = yf.download("^GSPC", start = "2025-01-01", end = "2025-12-31")


# 2. Calculate Returns

AAPL['AAPLret'] = AAPL['Close'].pct_change()
sp500['MktRet'] = sp500['Close'].pct_change()

# 3. Merge DataFrames

df = pd.merge(AAPL['AAPLret'], sp500['MktRet'], left_index=True, right_index=True)
df = df.dropna()

# 4. Define Y and X (add a constant to X)
X = df['MktRet']
Y = df['AAPLret']

X = sm.add_constant(X)

# 5. Fit OLS Model and Print Summary

result = sm.OLS(Y, X).fit()
print(result.summary())

model = result

beta = model.params['MktRet']
r_sq = model.rsquared
p_val = model.pvalues['MktRet']
print(beta, r_sq, p_val)


if p_val < 0.05:
    print("significant")
else:
    print("insignificant")













