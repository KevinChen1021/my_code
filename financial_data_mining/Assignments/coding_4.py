'''Question 1: Advanced Value at Risk (VaR) and Distribution Analysis
Objective: This question tests on standard risk metric calculations, statistical normality tests, and adjusting risk models for non-normal distributions 
(fat tails/asymmetry).

Question:
Assume you are managing a $100,000 portfolio consisting entirely of one stock.

1.Data Preparation: Use the provided data to calculate the daily percentage returns. Drop any missing values.
2.Standard VaR: Assuming the stock returns follow a standard normal distribution, calculate the 1-day and 10-day Value at Risk (VaR) at a 99% confidence level.
3.Normality Testing: Calculate the sample skewness and excess kurtosis of the daily returns. Perform either a Shapiro-Wilk or Anderson-Darling test on the returns. 
Output the test statistic and p-value, and briefly explain whether the data supports the normality assumption. '''

import pandas as pd
infile = "WMT12.pkl"
df = pd.read_pickle(infile)

# task 1: calculate daily percentage returns and drop missing values
df["ret"] = df["price"].pct_change().dropna()

# task 2: calculate 1-day and 10-day VaR at 99% confidence level
import numpy as np
import scipy.stats as stats
confidence_level = 0.99
z_score = stats.norm.ppf(1 - confidence_level)
portfolio_value = 100000
daily_volatility = df["ret"].std()
VaR_1_day = portfolio_value * daily_volatility * z_score
VaR_10_day = VaR_1_day * np.sqrt(10)

#task 3: calculate skewness, excess kurtosis, and perform normality test
skewness = df["ret"].skew()
kurtosis = df["ret"].kurtosis()

alpha = 0.05
if stats.shapiro(df["ret"])[1] < alpha:
    normality_result = "Reject null hypothesis - data is not normally distributed"
else:
    normality_result = "Fail to reject null hypothesis - data is normally distributed"


'''Question 2: Monte Carlo Simulation and Option Pricing
Objective: This question tests the ability to generate random variables, construct a geometric Brownian motion simulation using loops, visualize data, 
and apply the simulation to price a financial derivative.

Question:
You are tasked with forecasting terminal stock prices and pricing a European Call Option using Monte Carlo simulations. Use the following parameters: 
Initial stock price S0=50, expected annual return μ= 0.12, annualized volatility σ= 0.25, time to maturity T = 1 year, and risk-free rate r = 0.05.

1.Simulation Setup: Set the random seed to 12345. Simulate 5,000 distinct paths of the stock price over 100 time steps (dt = T/100).
2.Visualization: Extract the terminal prices (the price of the stock at the final step for all 5,000 simulations) and plot them using a histogram. 
3.Call Option Pricing: Using the terminal prices generated from your simulation, price a European Call Option with a strike price of X = 55. 
Calculate the payoff for each simulated path, 
and determine the current price of the call option by discounting the average payoff back to present value using the risk-free rate.
'''


#task1: simulation setup
S0 = 50
mu = 0.12
sigma = 0.25
T = 1
r = 0.05
np.random.seed(12345)
n_simulations = 5000
n_steps = 100
dt = T / n_steps
strike = 55

terminal_prices = np.zeros(n_simulations)
for i in range(n_simulations):
    S = S0
    for j in range(n_steps):
        Z = np.random.standard_normal()
        S *= np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    terminal_prices[i] = S

#task2: visualization
import matplotlib.pyplot as plt
plt.hist(terminal_prices, bins=50, edgecolor='black')
plt.title('Histogram of Terminal Stock Prices')
plt.xlabel('Terminal Price')
plt.ylabel('Frequency')
plt.show()

#task3: call option pricing
payoffs = np.maximum(terminal_prices - strike, 0)
option_price = np.exp(-r * T) * np.mean(payoffs)
print('European call option price (Monte Carlo):', option_price)








