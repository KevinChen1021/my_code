import argparse
import json
from pathlib import Path

from build_chapters_1_3 import OUTPUT_DIR, add_topic, markdown, notebook
from build_chapters_4_8_and_assignments import assignment_header, chapter_header


def chapter_9():
    cells = [
        chapter_header(
            9,
            "Portfolio Theory",
            [
                "Covariance, correlation, and diversification",
                "Two-asset portfolio variance",
                "N-asset matrix notation",
                "Minimum-variance and maximum-Sharpe portfolios",
                "Risk-return utility",
            ],
        )
    ]
    add_topic(
        cells,
        "9.1 Correlated Return Series",
        "Correlation is a unit-free measure of co-movement. The lecture construction creates two normal series with a target correlation.",
        """
import numpy as np

rng = np.random.default_rng(123456)
n = 5000
target_correlation = 0.30
x1 = rng.standard_normal(n)
x2 = rng.standard_normal(n)

# y2 将共同冲击与独立冲击组合，理论相关系数为 rho
y1 = x1
y2 = target_correlation * x1 + np.sqrt(1 - target_correlation**2) * x2

covariance = np.cov(y1, y2, ddof=1)[0, 1]
correlation = np.corrcoef(y1, y2)[0, 1]
print("Sample covariance =", round(float(covariance), 4))
print("Sample correlation =", round(float(correlation), 4))
""",
        "The sample correlation should be close to 0.30; small differences are sampling noise.",
    )
    add_topic(
        cells,
        "9.2 Two-Asset Portfolio Risk",
        "Portfolio variance contains two individual variance terms and one covariance term. Lower correlation creates a stronger diversification benefit.",
        """
import numpy as np

def two_asset_volatility(weight_a, vol_a, vol_b, correlation):
    weight_b = 1 - weight_a
    covariance = correlation * vol_a * vol_b
    variance = (
        weight_a**2 * vol_a**2
        + weight_b**2 * vol_b**2
        + 2 * weight_a * weight_b * covariance
    )
    return np.sqrt(variance)

weight_a, vol_a, vol_b = 0.60, 0.20, 0.12
for rho in (1.0, 0.3, -0.3):
    # 相关系数下降时，组合波动率通常下降
    risk = two_asset_volatility(weight_a, vol_a, vol_b, rho)
    print(f"rho={rho:+.1f}: portfolio volatility={risk:.2%}")
""",
        "The same assets and weights produce less portfolio risk when their correlation is lower.",
    )
    add_topic(
        cells,
        "9.3 N-Asset Portfolio in Matrix Form",
        "For weights w and covariance matrix Sigma, expected return is w' mu and variance is w' Sigma w.",
        """
import numpy as np

expected_returns = np.array([0.08, 0.11, 0.06])
volatilities = np.array([0.16, 0.22, 0.10])
correlations = np.array([
    [1.00, 0.45, 0.20],
    [0.45, 1.00, 0.10],
    [0.20, 0.10, 1.00],
])
weights = np.array([0.40, 0.35, 0.25])

# 协方差矩阵 = 相关系数矩阵 × 两侧标准差
covariance = np.outer(volatilities, volatilities) * correlations
portfolio_return = weights @ expected_returns
portfolio_variance = weights @ covariance @ weights

print("Weights sum =", round(float(weights.sum()), 6))
print("Expected return =", round(float(portfolio_return), 4))
print("Volatility =", round(float(np.sqrt(portfolio_variance)), 4))
""",
        "Matrix notation scales the two-asset formula to any number of assets.",
    )
    add_topic(
        cells,
        "9.4 Constrained Portfolio Optimization",
        "SLSQP can enforce full investment and long-only bounds while minimizing variance or maximizing the Sharpe ratio.",
        """
import numpy as np
from scipy.optimize import minimize

mu = np.array([0.08, 0.11, 0.06])
covariance = np.array([
    [0.0256, 0.01584, 0.0032],
    [0.01584, 0.0484, 0.0022],
    [0.0032, 0.0022, 0.0100],
])
risk_free = 0.025
n_assets = len(mu)

def variance(weights):
    return weights @ covariance @ weights

def negative_sharpe(weights):
    portfolio_return = weights @ mu
    portfolio_volatility = np.sqrt(variance(weights))
    return -(portfolio_return - risk_free) / portfolio_volatility

# 等式约束要求权重之和为 1；bounds 禁止卖空
constraints = {"type": "eq", "fun": lambda w: w.sum() - 1}
bounds = [(0, 1)] * n_assets
initial = np.full(n_assets, 1 / n_assets)

minimum_variance = minimize(variance, initial, method="SLSQP", bounds=bounds, constraints=constraints)
maximum_sharpe = minimize(negative_sharpe, initial, method="SLSQP", bounds=bounds, constraints=constraints)

print("Minimum-variance weights =", np.round(minimum_variance.x, 4))
print("Maximum-Sharpe weights =", np.round(maximum_sharpe.x, 4))
print("Maximum Sharpe =", round(float(-maximum_sharpe.fun), 4))
""",
        "The two objectives generally select different portfolios because minimum variance ignores expected return.",
    )
    add_topic(
        cells,
        "9.5 Risk-Return Utility",
        "A mean-variance investor can summarize preference with U = E(R) - 0.5 A sigma-squared, where A measures risk aversion.",
        """
portfolios = [
    {"name": "Conservative", "return": 0.065, "volatility": 0.08},
    {"name": "Balanced", "return": 0.090, "volatility": 0.14},
    {"name": "Aggressive", "return": 0.125, "volatility": 0.24},
]

for risk_aversion in (2, 6):
    utilities = []
    for portfolio in portfolios:
        # A 越大，波动率平方受到的惩罚越重
        utility = portfolio["return"] - 0.5 * risk_aversion * portfolio["volatility"]**2
        utilities.append((utility, portfolio["name"]))
    best = max(utilities)
    print(f"A={risk_aversion}: preferred={best[1]}, utility={best[0]:.4f}")
""",
        "More risk-averse investors assign a larger penalty to volatility and may prefer a lower-risk portfolio.",
    )
    return notebook(cells)


def chapter_10():
    cells = [
        chapter_header(
            10,
            "Options and Futures",
            [
                "Call and put payoffs",
                "Black-Scholes-Merton valuation",
                "Put-call parity",
                "Implied volatility and volatility smiles",
                "Trading strategies and Greeks",
                "Currency forward arbitrage",
            ],
        )
    ]
    add_topic(
        cells,
        "10.1 Option Payoff and Profit",
        "Payoff excludes the initial premium; profit includes it. Buyer and seller positions have opposite terminal profit.",
        """
import numpy as np

terminal_prices = np.array([30, 40, 50, 60, 70], dtype=float)
strike, call_premium, put_premium = 50, 4.5, 3.5

call_payoff = np.maximum(terminal_prices - strike, 0)
put_payoff = np.maximum(strike - terminal_prices, 0)
call_profit = call_payoff - call_premium
put_profit = put_payoff - put_premium

for price, call, put in zip(terminal_prices, call_profit, put_profit):
    print(f"S_T={price:.0f}: long-call profit={call:.2f}, long-put profit={put:.2f}")
""",
        "A call benefits from prices above the strike; a put benefits from prices below the strike.",
    )
    add_topic(
        cells,
        "10.2 Black-Scholes-Merton and Put-Call Parity",
        "European call and put prices should satisfy C + K exp(-rT) = S + P when assumptions and inputs are consistent.",
        """
from math import exp, log, sqrt
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    put = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return call, put

S, K, T, r, sigma = 40, 40, 0.5, 0.01, 0.20
call, put = black_scholes(S, K, T, r, sigma)

# 两个复制组合的现值应当相同
left = call + K * exp(-r * T)
right = S + put
print("Call =", round(call, 4), "Put =", round(put, 4))
print("Parity difference =", round(left - right, 10))
""",
        "The parity difference is numerically zero, which checks both formulas at once.",
    )
    add_topic(
        cells,
        "10.3 Implied Volatility",
        "Implied volatility reverses an option-pricing model: find sigma that reproduces the observed market price.",
        """
from math import exp, log, sqrt
from scipy.optimize import brentq
from scipy.stats import norm

def call_price(S, K, T, r, sigma):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)

def implied_volatility(S, K, T, r, market_price):
    # 根是“模型价格 - 市场价格 = 0”
    objective = lambda sigma: call_price(S, K, T, r, sigma) - market_price
    return brentq(objective, 1e-6, 5.0)

S, T, r = 100, 0.5, 0.02
quotes = [(90, 12.80), (100, 6.00), (110, 3.15)]
for strike, market_price in quotes:
    iv = implied_volatility(S, strike, T, r, market_price)
    print(f"K={strike}: implied volatility={iv:.2%}")
""",
        "Different implied volatilities across strikes produce the volatility-smile or skew pattern.",
    )
    add_topic(
        cells,
        "10.4 Option Strategies",
        "A straddle buys a call and a put at the same strike; a covered call combines stock ownership with a short call.",
        """
import numpy as np

terminal_prices = np.arange(30, 71, 10)
strike, call_premium, put_premium, stock_price = 50, 4.5, 3.5, 50

# Straddle 需要价格大幅向任一方向变化
straddle = np.maximum(terminal_prices - strike, 0) + np.maximum(strike - terminal_prices, 0) - call_premium - put_premium

# Covered call 的上涨收益被执行价封顶
covered_call = terminal_prices - stock_price - np.maximum(terminal_prices - strike, 0) + call_premium

for price, s_profit, c_profit in zip(terminal_prices, straddle, covered_call):
    print(f"S_T={price}: straddle={s_profit:.2f}, covered call={c_profit:.2f}")
""",
        "The straddle is a volatility position, whereas the covered call exchanges upside potential for premium income.",
    )
    add_topic(
        cells,
        "10.5 Delta and Gamma",
        "Delta is the first derivative of option value with respect to stock price; gamma is the second derivative.",
        """
from math import exp, log, sqrt
from scipy.stats import norm

def call_price(S, K, T, r, sigma):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)

S, K, T, r, sigma = 40, 40, 0.5, 0.01, 0.20
d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
delta = norm.cdf(d1)
gamma = norm.pdf(d1) / (S * sigma * sqrt(T))

bump = 0.01
# 中心差分用 S+h、S、S-h 近似二阶导数
numerical_gamma = (
    call_price(S + bump, K, T, r, sigma)
    - 2 * call_price(S, K, T, r, sigma)
    + call_price(S - bump, K, T, r, sigma)
) / bump**2

print("Delta =", round(delta, 6))
print("Closed-form gamma =", round(gamma, 6))
print("Numerical gamma =", round(numerical_gamma, 6))
""",
        "The analytical and finite-difference gamma values should agree closely.",
    )
    add_topic(
        cells,
        "10.6 Currency Forward No-Arbitrage",
        "Covered interest parity links spot and forward exchange rates through domestic and foreign interest rates.",
        """
from math import exp

spot = 1.25
domestic_rate = 0.01
foreign_rate = 0.02
T = 3 / 12
market_forward = 1.26

# 连续复利下的无套利远期汇率
fair_forward = spot * exp((domestic_rate - foreign_rate) * T)
mispricing = market_forward - fair_forward

print("Fair forward =", round(fair_forward, 6))
print("Market minus fair =", round(mispricing, 6))
""",
        "A market forward above the covered-interest-parity value indicates the direction of a potential arbitrage before transaction costs.",
    )
    return notebook(cells)


def chapter_11():
    cells = [
        chapter_header(
            11,
            "Value at Risk",
            [
                "Parametric normal VaR",
                "Multi-day scaling and sign conventions",
                "Normality tests and modified VaR",
                "Historical VaR and expected shortfall",
                "Portfolio VaR",
            ],
        )
    ]
    add_topic(
        cells,
        "11.1 Parametric One-Day and Ten-Day VaR",
        "VaR is reported here as a positive loss amount. Under iid normal returns, volatility scales with the square root of time.",
        """
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(1101)
returns = rng.normal(0.0004, 0.018, 1000)
position = 100_000
confidence = 0.99
z = norm.ppf(confidence)
mean, volatility = returns.mean(), returns.std(ddof=1)

# 左尾收益分位数为负；取负号后把 VaR 报告成正的损失金额
var_1_day = -position * (mean - z * volatility)
mean_10_day = (1 + mean) ** 10 - 1
var_10_day = -position * (mean_10_day - z * volatility * np.sqrt(10))

print("1-day VaR =", round(var_1_day, 2))
print("10-day VaR =", round(var_10_day, 2))
""",
        "Ten-day VaR is larger, but it is not exactly ten times one-day VaR because volatility uses square-root-of-time scaling.",
    )
    add_topic(
        cells,
        "11.2 Normality and Modified VaR",
        "Shapiro-Wilk tests normality. Cornish-Fisher modified VaR adjusts the normal quantile for skewness and excess kurtosis.",
        """
import numpy as np
from scipy import stats

rng = np.random.default_rng(1102)
# t 分布产生较厚尾部，用于展示正态假设可能失效
returns = 0.0004 + 0.012 * rng.standard_t(df=5, size=900)
confidence = 0.99
position = 100_000
z = stats.norm.ppf(1 - confidence)

skewness = stats.skew(returns, bias=False)
excess_kurtosis = stats.kurtosis(returns, fisher=True, bias=False)
test = stats.shapiro(returns)

# Cornish-Fisher 展开修正左尾分位数
adjusted_z = (
    z
    + (z**2 - 1) * skewness / 6
    + (z**3 - 3 * z) * excess_kurtosis / 24
    - (2 * z**3 - 5 * z) * skewness**2 / 36
)
modified_var = -position * (returns.mean() + adjusted_z * returns.std(ddof=1))

print("Skewness =", round(float(skewness), 4))
print("Excess kurtosis =", round(float(excess_kurtosis), 4))
print("Shapiro p-value =", round(float(test.pvalue), 8))
print("Modified VaR =", round(float(modified_var), 2))
""",
        "A small p-value rejects normality; modified VaR then incorporates observed asymmetry and tail thickness.",
    )
    add_topic(
        cells,
        "11.3 Historical VaR and Expected Shortfall",
        "Historical simulation uses the empirical loss tail. Expected shortfall averages losses beyond the VaR cutoff.",
        """
import numpy as np

rng = np.random.default_rng(1103)
returns = 0.0003 + 0.011 * rng.standard_t(df=6, size=1500)
position = 100_000
confidence = 0.99
tail_probability = 1 - confidence

# quantile 返回左尾收益；损失金额使用负号
tail_cutoff = np.quantile(returns, tail_probability)
historical_var = -position * tail_cutoff
expected_shortfall = -position * returns[returns <= tail_cutoff].mean()

print("Historical VaR =", round(float(historical_var), 2))
print("Expected shortfall =", round(float(expected_shortfall), 2))
print("Tail observations =", int((returns <= tail_cutoff).sum()))
""",
        "Expected shortfall should exceed VaR because it averages outcomes deeper in the loss tail.",
    )
    add_topic(
        cells,
        "11.4 Portfolio VaR",
        "Portfolio VaR must use portfolio volatility, including covariance. It is generally not the weighted average of standalone VaRs.",
        """
import numpy as np
from scipy.stats import norm

weights = np.array([0.50, 0.30, 0.20])
volatilities = np.array([0.018, 0.014, 0.010])
correlations = np.array([
    [1.00, 0.55, 0.20],
    [0.55, 1.00, 0.15],
    [0.20, 0.15, 1.00],
])
position = 1_000_000
confidence = 0.99

covariance = np.outer(volatilities, volatilities) * correlations
portfolio_volatility = np.sqrt(weights @ covariance @ weights)
portfolio_var = position * norm.ppf(confidence) * portfolio_volatility
weighted_standalone = position * norm.ppf(confidence) * (weights @ volatilities)

print("Portfolio VaR =", round(float(portfolio_var), 2))
print("Weighted standalone VaR =", round(float(weighted_standalone), 2))
print("Diversification benefit =", round(float(weighted_standalone - portfolio_var), 2))
""",
        "Positive but imperfect correlations create a diversification benefit relative to weighted standalone risks.",
    )
    return notebook(cells)


def chapter_12():
    cells = [
        chapter_header(
            12,
            "Monte Carlo Simulation",
            [
                "Random generators, seeds, and resampling",
                "Geometric Brownian motion",
                "Risk-neutral option pricing",
                "Correlated simulations",
                "Simulation VaR",
                "Sobol sequences and return forecasting",
            ],
        )
    ]
    add_topic(
        cells,
        "12.1 Random Seeds, Permutations, and Bootstrap",
        "A fixed seed makes an experiment reproducible. Permutation samples without replacement; bootstrap samples with replacement.",
        """
import numpy as np

rng = np.random.default_rng(12345)
data = np.array([1, 2, 3, 4, 5])

uniform_draws = rng.uniform(0, 1, 5)
normal_draws = rng.standard_normal(5)
without_replacement = rng.choice(data, size=4, replace=False)
bootstrap = rng.choice(data, size=8, replace=True)

print("Uniform =", np.round(uniform_draws, 4))
print("Normal =", np.round(normal_draws, 4))
print("Without replacement =", without_replacement)
print("Bootstrap =", bootstrap)
""",
        "Re-running the cell produces identical draws because the generator starts from the same seed.",
    )
    add_topic(
        cells,
        "12.2 Geometric Brownian Motion Paths",
        "GBM models multiplicative stock-price changes and keeps simulated prices positive.",
        """
import numpy as np

S0, mu, sigma, T = 50, 0.12, 0.25, 1.0
n_paths, n_steps = 5000, 100
dt = T / n_steps
rng = np.random.default_rng(12345)

shocks = rng.standard_normal((n_paths, n_steps))
# 每一步的对数收益包含漂移修正 -0.5*sigma^2
log_increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
paths = S0 * np.exp(np.cumsum(log_increments, axis=1))
terminal_prices = paths[:, -1]

print("Mean terminal price =", round(float(terminal_prices.mean()), 4))
print("Median terminal price =", round(float(np.median(terminal_prices)), 4))
print("5% and 95% quantiles =", np.round(np.quantile(terminal_prices, [0.05, 0.95]), 4))
""",
        "The mean terminal price is influenced by the real-world expected return mu and is useful for forecasting scenarios.",
    )
    add_topic(
        cells,
        "12.3 Monte Carlo European Call Pricing",
        "Derivative pricing uses risk-neutral drift r, not the stock's forecast return mu.",
        """
import numpy as np

S0, K, r, sigma, T = 50, 55, 0.05, 0.25, 1.0
n_simulations = 100_000
rng = np.random.default_rng(12345)

z = rng.standard_normal(n_simulations)
# 风险中性世界中漂移使用无风险利率 r
terminal_prices = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)
payoffs = np.maximum(terminal_prices - K, 0)
option_price = np.exp(-r * T) * payoffs.mean()
standard_error = np.exp(-r * T) * payoffs.std(ddof=1) / np.sqrt(n_simulations)

print("Call price =", round(float(option_price), 4))
print("Monte Carlo standard error =", round(float(standard_error), 6))
""",
        "The discounted average payoff estimates the no-arbitrage call value; the standard error measures simulation noise.",
    )
    add_topic(
        cells,
        "12.4 Correlated Asset Simulation",
        "Cholesky decomposition transforms independent shocks into shocks with a target correlation matrix.",
        """
import numpy as np

rng = np.random.default_rng(1204)
target = np.array([
    [1.00, 0.60, 0.25],
    [0.60, 1.00, 0.10],
    [0.25, 0.10, 1.00],
])
independent = rng.standard_normal((20_000, 3))

# L @ L.T 等于目标相关矩阵
cholesky = np.linalg.cholesky(target)
correlated = independent @ cholesky.T
sample = np.corrcoef(correlated, rowvar=False)

print("Target correlation:")
print(target)
print("Simulated correlation:")
print(np.round(sample, 3))
""",
        "The simulated correlation matrix converges toward the target matrix as the number of draws grows.",
    )
    add_topic(
        cells,
        "12.5 Monte Carlo VaR",
        "Simulation VaR estimates the portfolio loss quantile from generated scenarios and can accommodate richer return models.",
        """
import numpy as np

rng = np.random.default_rng(1205)
position = 1_000_000
confidence = 0.99
n_simulations = 100_000

# 使用厚尾 t 分布展示模拟法不必局限于正态分布
simulated_returns = 0.0003 + 0.012 * rng.standard_t(df=6, size=n_simulations)
losses = -position * simulated_returns
var = np.quantile(losses, confidence)
expected_shortfall = losses[losses >= var].mean()

print("Simulation VaR =", round(float(var), 2))
print("Simulation expected shortfall =", round(float(expected_shortfall), 2))
""",
        "The simulated expected shortfall exceeds VaR because it averages the worst one percent of scenarios.",
    )
    add_topic(
        cells,
        "12.6 Sobol Sequence and Long-Horizon Returns",
        "Sobol points cover a unit square more evenly than ordinary random draws. Long-horizon forecasts blend arithmetic and geometric means.",
        """
import numpy as np
from scipy import stats

sobol = stats.qmc.Sobol(d=2, scramble=True, seed=1206)
# random_base2 保持 Sobol 序列的平衡性质
points = sobol.random_base2(m=8)
center_distance = np.linalg.norm(points.mean(axis=0) - 0.5)

annual_returns = np.array([0.12, -0.08, 0.20, 0.05, 0.10, -0.03])
arithmetic_mean = annual_returns.mean()
geometric_mean = stats.gmean(1 + annual_returns) - 1
n_history, n_forecast = len(annual_returns), 3
weight = min(n_forecast / n_history, 1)
blended_forecast = weight * geometric_mean + (1 - weight) * arithmetic_mean

print("Sobol sample mean =", np.round(points.mean(axis=0), 4))
print("Distance from square center =", round(float(center_distance), 4))
print("Arithmetic mean =", round(float(arithmetic_mean), 4))
print("Geometric mean =", round(float(geometric_mean), 4))
print("Blended forecast =", round(float(blended_forecast), 4))
""",
        "Sobol coverage supports numerical integration, while the blended return forecast reduces horizon-dependent bias.",
    )
    return notebook(cells)


def chapter_13():
    cells = [
        chapter_header(
            13,
            "Exotic Options",
            [
                "Path-independent and path-dependent contracts",
                "Asian average-price options",
                "Barrier options",
                "Chooser options",
                "Monte Carlo comparison of exotic payoffs",
            ],
        )
    ]
    cells.append(
        markdown(
            """
## 13.1 Exotic Option Map

- **Asian option:** payoff depends on an average price.
- **Barrier option:** activation or cancellation depends on whether a barrier is crossed.
- **Lookback option:** payoff depends on a path maximum or minimum.
- **Compound option:** the underlying asset is another option.
- **Chooser option:** the holder later chooses whether the contract becomes a call or put.

Path dependence determines whether the full simulated price path must be stored.
"""
        )
    )
    add_topic(
        cells,
        "13.2 Asian Average-Price Call",
        "An arithmetic-average Asian call pays max(average path price - strike, 0), reducing sensitivity to a single terminal observation.",
        """
import numpy as np

S0, K, r, sigma, T = 40, 40, 0.05, 0.20, 1.0
n_paths, n_steps = 50_000, 50
dt = T / n_steps
rng = np.random.default_rng(1302)

shocks = rng.standard_normal((n_paths, n_steps))
increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
paths = S0 * np.exp(np.cumsum(increments, axis=1))

# 亚洲期权使用路径平均价格，而普通欧式期权只使用最后价格
average_prices = paths.mean(axis=1)
asian_payoffs = np.maximum(average_prices - K, 0)
european_payoffs = np.maximum(paths[:, -1] - K, 0)

asian_price = np.exp(-r * T) * asian_payoffs.mean()
european_price = np.exp(-r * T) * european_payoffs.mean()
print("Asian call =", round(float(asian_price), 4))
print("European call =", round(float(european_price), 4))
""",
        "Averaging dampens extremes, so this Asian call is typically cheaper than the corresponding European call.",
    )
    add_topic(
        cells,
        "13.3 Up-and-Out Barrier Call",
        "An up-and-out call becomes worthless if the stock price reaches or exceeds the barrier before maturity.",
        """
import numpy as np

S0, K, barrier, r, sigma, T = 40, 40, 50, 0.05, 0.20, 1.0
n_paths, n_steps = 60_000, 100
dt = T / n_steps
rng = np.random.default_rng(1303)

shocks = rng.standard_normal((n_paths, n_steps))
increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
paths = S0 * np.exp(np.cumsum(increments, axis=1))

# 任一时点触及 barrier，knocked_out 就为 True
knocked_out = np.max(paths, axis=1) >= barrier
vanilla_payoffs = np.maximum(paths[:, -1] - K, 0)
barrier_payoffs = np.where(knocked_out, 0, vanilla_payoffs)

barrier_price = np.exp(-r * T) * barrier_payoffs.mean()
vanilla_price = np.exp(-r * T) * vanilla_payoffs.mean()
print("Knockout frequency =", round(float(knocked_out.mean()), 4))
print("Up-and-out call =", round(float(barrier_price), 4))
print("Vanilla call =", round(float(vanilla_price), 4))
""",
        "The knockout feature removes valuable payoff scenarios, making the barrier call cheaper than the vanilla call.",
    )
    add_topic(
        cells,
        "13.4 Simple Chooser Option",
        "At the choice date, the holder selects the more valuable remaining European call or put.",
        """
import numpy as np
from scipy.stats import norm

def option_values(S, K, remaining_time, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * remaining_time) / (sigma * np.sqrt(remaining_time))
    d2 = d1 - sigma * np.sqrt(remaining_time)
    call = S * norm.cdf(d1) - K * np.exp(-r * remaining_time) * norm.cdf(d2)
    put = K * np.exp(-r * remaining_time) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return call, put

S0, K, r, sigma, maturity, choice_time = 40, 40, 0.05, 0.20, 1.0, 0.25
rng = np.random.default_rng(1304)
n_paths = 100_000

# 先模拟到选择时点，再比较剩余 call 与 put 的价值
z = rng.standard_normal(n_paths)
S_choice = S0 * np.exp((r - 0.5 * sigma**2) * choice_time + sigma * np.sqrt(choice_time) * z)
call, put = option_values(S_choice, K, maturity - choice_time, r, sigma)
chooser_price = np.exp(-r * choice_time) * np.maximum(call, put).mean()

print("Chooser option price =", round(float(chooser_price), 4))
print("Call chosen frequency =", round(float((call >= put).mean()), 4))
""",
        "The right to choose adds flexibility, so a chooser option is worth more than either fixed choice alone at inception.",
    )
    add_topic(
        cells,
        "13.5 Path-Dependence Comparison",
        "Using common random numbers makes payoff differences easier to attribute to contract design rather than simulation noise.",
        """
import numpy as np

S0, K, barrier, r, sigma, T = 40, 40, 50, 0.05, 0.20, 1.0
n_paths, n_steps = 30_000, 50
dt = T / n_steps
rng = np.random.default_rng(1305)

shocks = rng.standard_normal((n_paths, n_steps))
paths = S0 * np.exp(np.cumsum((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks, axis=1))
discount = np.exp(-r * T)

european = discount * np.maximum(paths[:, -1] - K, 0).mean()
asian = discount * np.maximum(paths.mean(axis=1) - K, 0).mean()
barrier_payoff = np.where(paths.max(axis=1) >= barrier, 0, np.maximum(paths[:, -1] - K, 0))
barrier_call = discount * barrier_payoff.mean()

print("European =", round(float(european), 4))
print("Asian =", round(float(asian), 4))
print("Up-and-out =", round(float(barrier_call), 4))
""",
        "All three contracts share the same simulated paths, revealing how averaging and knockout clauses alter value.",
    )
    return notebook(cells)


def assignment_4():
    cells = [
        assignment_header(
            4,
            "Advanced VaR and Monte Carlo Option Pricing",
            [
                "Daily returns, parametric VaR, and normality testing",
                "GBM terminal-price simulation",
                "Risk-neutral European call pricing",
            ],
        )
    ]
    add_topic(
        cells,
        "Question 1: VaR and Distribution Analysis",
        "The original assignment uses WMT data. This reproducible version generates a fat-tailed return sample and applies the same required workflow.",
        """
import numpy as np
from scipy import stats

rng = np.random.default_rng(4041)
portfolio_value = 100_000
confidence = 0.99

# 用厚尾收益模拟股票价格，再由价格反算日收益率
daily_returns = 0.0004 + 0.012 * rng.standard_t(df=6, size=1000)
prices = 100 * np.cumprod(1 + daily_returns)
returns = prices[1:] / prices[:-1] - 1

z = stats.norm.ppf(confidence)
mean = returns.mean()
volatility = returns.std(ddof=1)
var_1_day = -portfolio_value * (mean - z * volatility)
var_10_day = -portfolio_value * ((1 + mean) ** 10 - 1 - z * volatility * np.sqrt(10))

skewness = stats.skew(returns, bias=False)
excess_kurtosis = stats.kurtosis(returns, fisher=True, bias=False)
shapiro = stats.shapiro(returns)

print("1-day VaR =", round(float(var_1_day), 2))
print("10-day VaR =", round(float(var_10_day), 2))
print("Skewness =", round(float(skewness), 4))
print("Excess kurtosis =", round(float(excess_kurtosis), 4))
print("Shapiro statistic =", round(float(shapiro.statistic), 6))
print("Shapiro p-value =", round(float(shapiro.pvalue), 8))
print("Normality supported =", bool(shapiro.pvalue >= 0.05))
""",
        "The normality conclusion follows the p-value, while positive VaR values are reported as loss magnitudes.",
    )
    add_topic(
        cells,
        "Question 2: Monte Carlo Forecast and Call Pricing",
        "The stock forecast uses the stated expected return mu. The option price uses a separate risk-neutral simulation with drift r.",
        """
import numpy as np

S0, mu, sigma, T, r, strike = 50, 0.12, 0.25, 1.0, 0.05, 55
n_simulations, n_steps = 5000, 100
dt = T / n_steps
rng = np.random.default_rng(12345)
shocks = rng.standard_normal((n_simulations, n_steps))

# 真实世界路径用于价格预测
forecast_increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
forecast_paths = S0 * np.exp(np.cumsum(forecast_increments, axis=1))
forecast_terminal = forecast_paths[:, -1]

# 期权定价必须在风险中性世界把漂移替换为 r
pricing_increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
pricing_paths = S0 * np.exp(np.cumsum(pricing_increments, axis=1))
pricing_terminal = pricing_paths[:, -1]
payoffs = np.maximum(pricing_terminal - strike, 0)
option_price = np.exp(-r * T) * payoffs.mean()

print("Forecast terminal mean =", round(float(forecast_terminal.mean()), 4))
print("Forecast terminal median =", round(float(np.median(forecast_terminal)), 4))
print("European call price =", round(float(option_price), 4))
""",
        "Using common shocks exposes the effect of changing only the drift from mu to r for valuation.",
    )
    return notebook(cells)


def main(output_dir=OUTPUT_DIR):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    notebooks = {
        "chapter_9.ipynb": chapter_9(),
        "chapter_10.ipynb": chapter_10(),
        "chapter_11.ipynb": chapter_11(),
        "chapter_12.ipynb": chapter_12(),
        "chapter_13.ipynb": chapter_13(),
        "assignment_4.ipynb": assignment_4(),
    }
    for filename, content in notebooks.items():
        path = output_dir / filename
        path.write_text(json.dumps(content, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()
    main(args.output_dir)
