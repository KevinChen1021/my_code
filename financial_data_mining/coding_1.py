# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:27:22 2026

@author: KevinChen
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Date and Time:

YOUR NAME:
YOUR ID:
"""

"""
Task One: Make sure you have install all the modules need for this class

"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Exercise One
"""

# =============================================================================
# MODULE 1: ENVIRONMENT & SYSTEM AUDIT 
# =============================================================================

# 1.0 Fill all the blanks to import the necessary modules
import os
import sys
import pandas as pd
import numpy as np
import yfinance as yf
import scipy.stats as stats
import numpy_financial as npf
import matplotlib.pyplot as plt


# 1.1 Task: Get current working directory and create a new folder 'Class_Exercise'
# the print out should be something like "Current Directory: abc/def/ghi

# [Placeholder: Use os.mkdir or os.makedirs to create the folder and os.chdir to enter it]
current_dir = os.getcwd()
path = os.path.join(os.path.expanduser("~"), "Desktop", "my_python", "Class_Exercise")
if not os.path.exists(path):
    os.makedirs(path)
os.chdir(path)
print(f"Current Directory:{path}")

# 1.2 Task: System Check
# [Placeholder: Print Python version using sys.version]
print(f"Python version:{sys.version}")

# [Placeholder: Print versions of pandas, numpy, and yfinance using .__version__]
print(f"pandas:{pd.__version__}")
print(f"numpy:{np.__version__}")
print(f"yfinance:{yf.__version__}")

# 1.3 Task: The dir() Investigation
# [Placeholder: Use dir(npf) to see available functions in numpy_financial]
print("Functions in npf", dir(npf))

# =============================================================================
# MODULE 2: DATA ENGINEERING & CLEANING 
# =============================================================================

# 2.1 Task: Multi-Ticker Download
# Download Adjusted Close prices for 'AAPL', 'MSFT', and 'GOOGL' from 2022-01-01 to today
tickers = ['AAPL', 'MSFT', 'GOOGL']
# [Placeholder: Use yf.download to get ONLY the 'Close' prices]
start_time = "2024-1-1"
end_time = "2026-3-19"

data = yf.download(tickers=tickers, start = start_time, end = end_time)["Close"]
print(data.head())

# 2.2 Task: Data Cleaning
# [Placeholder: Check for missing values using .isnull().sum()]
missing_value = data.isnull().sum()
print("Missing values before cleaning:\n", missing_value)

# [Placeholder: Use forward fill .ffill() to handle any NaNs]
data = data.ffill().dropna()

# 2.3 Task: Quarterly Returns Calculation
# Building on the logic from chapter four from the second class
# [Placeholder: Create a 'Quarter' column using df.index.quarter]
log_return = np.log(data/data.shift(1))
log_return["Year"] = log_return.index.year
log_return["Quarter"] = log_return.index.quarter

# [Placeholder: Calculate log returns and group by ['Year', 'Quarter']]
quarter_return = np.exp(log_return.groupby(["Year", "Quarter"]).sum()) - 1

# =============================================================================
# MODULE 3: COMPARATIVE ANALYSIS & PITCH 
# =============================================================================

# 3.1 Task: The Statistical Duel
# [Placeholder: Select two stocks and perform stats.ttest_ind on their daily returns]
returns = data.pct_change().dropna()
t_stat, p_value = stats.ttest_ind(returns["AAPL"], returns["MSFT"])
print(p_value)

# [Placeholder: Write an if-else statement to print if the difference is significant (p &lt; 0.05)]
if p_value < 0.05:
    print("significant")
else:
    print("not significant")

# 3.2 Task: Sharpe Ratio Calculation
# Sharpe = (Mean Return - Risk Free Rate) / Std Dev
risk_free_rate = 0.01 / 252 # Daily equivalent of 1% annual rate


# [Placeholder: Calculate the Daily Sharpe Ratio for all three stocks]
annual_return = 0.04
daily_return = (1 + annual_return)**(1/252) - 1
excess_return = returns - daily_return

sharpe_ratio = (excess_return.mean() / excess_return.std()) * np.sqrt(252)

print(sharpe_ratio)

# 3.3 Task: Visualizing the Growth
# [Placeholder: Calculate Cumulative Returns: (1 + returns).cumprod()]
cum_return= (1 + returns).cumprod()
plt.figure(figsize=(12, 8))

for ticker in tickers:
    plt.plot(cum_return[ticker], label=ticker)

plt.title("growth")
plt.xlabel("date")
plt.ylabel("value")
plt.show()

# [Placeholder: Plot the Cumulative Returns of all three stocks in one chart with a legend]


# 3.4 Task: Final Export
# [Placeholder: Save your results to 'portfolio_summary.csv' and 'portfolio_summary.pkl']


print("Exercise Complete. Please ensure all plots show and files are saved in your directory.")
