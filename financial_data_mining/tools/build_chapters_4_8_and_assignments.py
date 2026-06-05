import json
from pathlib import Path

from build_chapters_1_3 import OUTPUT_DIR, add_topic, code, markdown, notebook


def chapter_header(number, title, topics):
    items = "\n".join(f"{i}. {topic}" for i, topic in enumerate(topics, 1))
    return markdown(
        f"""
# Chapter {number}: {title}

This atlas follows the lecture sequence and uses deterministic financial data so
that every code module can run without an internet connection.

## Learning map

{items}

**Code availability:** Yes. Every code cell imports its own dependencies,
contains Chinese exam-oriented comments, and produces an interpretable result.

## How to Study This Chapter

- **First pass:** Read the concept and formula sections without running code.
- **Second pass:** Predict the output and fill in the commented key lines before execution.
- **Third pass:** Run each module independently and explain the result in one sentence.
- **Final review:** Compare related methods and identify when each method should or should not be used.

## Chapter Checklist

- Can I define every variable and state its unit?
- Can I reproduce the main formula or workflow without looking?
- Can I identify the code lines most likely to appear as blanks?
- Can I interpret the output economically or statistically?
- Can I name at least one common implementation error?
"""
    )


def chapter_4():
    cells = [
        chapter_header(
            4,
            "Open Financial Data and Return Engineering",
            [
                "Open-data sources and file formats",
                "Reading CSV data",
                "Simple and log returns",
                "Missing-value treatment",
                "Daily-to-monthly and annual aggregation",
                "One-sample and two-sample return tests",
            ],
        ),
        markdown(
            """
## 4.1 Open Data Workflow

Typical sources include Yahoo Finance, FRED, SEC filings, and academic factor
libraries. A robust workflow is **retrieve -> inspect -> clean -> transform ->
validate -> save**. CSV is portable and human-readable; pickle preserves Python
data types but should only be loaded from trusted sources.
"""
        ),
    ]
    add_topic(
        cells,
        "4.2 Reading and Inspecting CSV Data",
        "The lecture uses `pandas.read_csv`. This self-contained example creates the same table in memory and demonstrates the essential inspection steps.",
        """
'''
本单元模拟从 CSV 读取股票价格，并检查字段、行数和前几条记录。
StringIO 把字符串当作文件使用，因此无需依赖外部路径。
'''
import csv
import io

csv_text = '''Date,Close,Volume
2026-01-02,100.00,1200000
2026-01-05,101.50,1350000
2026-01-06,99.80,1280000
2026-01-07,102.20,1410000
'''

# DictReader 使用首行作为列名，并将每行转换为字典
rows = list(csv.DictReader(io.StringIO(csv_text)))

# 金融计算前应把文本价格转换为浮点数
close_prices = [float(row["Close"]) for row in rows]

print("Columns =", list(rows[0]))
print("Number of observations =", len(rows))
print("First row =", rows[0])
print("Mean close =", round(sum(close_prices) / len(close_prices), 2))
""",
        "The table contains four dated observations. Explicit type conversion prevents accidental string arithmetic.",
    )
    add_topic(
        cells,
        "4.3 Simple Returns and Log Returns",
        """
Simple return is $R_t=P_t/P_{t-1}-1$. Log return is
$r_t=\\ln(P_t/P_{t-1})=\\ln(1+R_t)$. Log returns add across time,
while simple returns compound.
""",
        """
'''
本单元根据价格序列计算百分比收益率和对数收益率。
考试填空常见位置是相邻价格的除法、减 1，以及自然对数转换。
'''
import numpy as np

prices = np.array([100.0, 101.5, 99.8, 102.2])

# 相邻价格相除后减 1，得到简单收益率
simple_returns = prices[1:] / prices[:-1] - 1

# 对价格比取自然对数，得到可加总的对数收益率
log_returns = np.log(prices[1:] / prices[:-1])

# exp(对数收益率)-1 可还原简单收益率
recovered_simple = np.exp(log_returns) - 1

print("Simple returns =", np.round(simple_returns, 6))
print("Log returns =", np.round(log_returns, 6))
print("Conversion check =", np.allclose(simple_returns, recovered_simple))
""",
        "The conversion check is true. Both definitions describe the same one-period price movement in different forms.",
    )
    add_topic(
        cells,
        "4.4 Missing Prices and Forward Fill",
        """
Price gaps may arise from data-source alignment or non-trading observations.
Forward fill can be reasonable for an isolated missing **price**, but missing
returns should not be filled without an economic justification.
""",
        """
'''
本单元用 NumPy 实现价格序列的前向填充。
关键逻辑：遇到 NaN 时，用最近一个有效价格替代。
'''
import numpy as np

prices = np.array([100.0, np.nan, 101.5, np.nan, 103.0])
filled = prices.copy()

for i in range(1, len(filled)):
    # np.isnan 判断当前价格是否缺失
    if np.isnan(filled[i]):
        # 前向填充使用上一期已经确认有效的价格
        filled[i] = filled[i - 1]

returns = filled[1:] / filled[:-1] - 1

print("Original prices =", prices)
print("Forward-filled prices =", filled)
print("Returns after cleaning =", np.round(returns, 6))
""",
        "Forward-filled dates generate zero returns because the observed price is carried forward rather than economically re-estimated.",
    )
    add_topic(
        cells,
        "4.5 Aggregating Daily Returns",
        """
Returns must be compounded, not averaged. For a period containing daily returns
$R_d$, the period return is $\\prod(1+R_d)-1$. Equivalently, sum daily log
returns and transform back.
""",
        """
'''
本单元把带月份标签的日收益率复利为月收益率。
group label 与收益率一一对应，适合考试中的分组累计题。
'''
import numpy as np

daily_returns = np.array([0.01, -0.005, 0.004, 0.012, -0.003, 0.006])
month_labels = np.array([202601, 202601, 202601, 202602, 202602, 202602])

monthly_returns = {}
for month in np.unique(month_labels):
    # 布尔条件选出同一个月的全部日收益率
    selected = daily_returns[month_labels == month]

    # 月收益率必须对 (1+日收益率) 连乘后再减 1
    monthly_returns[int(month)] = np.prod(1 + selected) - 1

print("Monthly compounded returns =")
for month, value in monthly_returns.items():
    print(month, f"{value:.4%}")
""",
        "Each monthly result preserves compounding and can be verified using the sum of daily log returns.",
    )
    add_topic(
        cells,
        "4.6 Tests of Mean Returns",
        """
A one-sample t-test compares a sample mean with a target such as zero. An
independent two-sample test compares two assets. Welch's version does not assume
equal variances.
""",
        """
'''
本单元用固定模拟收益率完成单样本和双样本 t 检验。
p 值低于显著性水平 alpha 时拒绝原假设。
'''
import numpy as np
from scipy import stats

rng = np.random.default_rng(2026)
ibm_returns = rng.normal(0.0006, 0.012, 252)
msft_returns = rng.normal(0.0009, 0.014, 252)
alpha = 0.05

# 单样本检验 H0：IBM 平均日收益率等于 0
one_sample = stats.ttest_1samp(ibm_returns, popmean=0)

# Welch t 检验 H0：两只股票平均收益率相等
two_sample = stats.ttest_ind(ibm_returns, msft_returns, equal_var=False)

print("IBM mean =", round(float(ibm_returns.mean()), 6))
print("One-sample p-value =", round(float(one_sample.pvalue), 6))
print("Two-sample p-value =", round(float(two_sample.pvalue), 6))
print("Two-sample decision =", "Reject H0" if two_sample.pvalue < alpha else "Do not reject H0")
""",
        "The conclusion is based on the p-value rather than the visual difference between sample means.",
    )
    add_topic(
        cells,
        "4.7 Saving, Reloading, and Dropping Missing Data",
        """
The classroom script adds a ticker column, removes incomplete observations, and
saves both CSV and pickle files. CSV is portable; pickle preserves Python
objects and should be loaded only from trusted sources.
""",
        """
'''
本单元补充源代码中的 ticker、dropna、CSV 和 pickle 保存流程。
使用临时目录，运行后自动清理，不修改用户工作目录。
'''
import csv
import math
import pickle
import tempfile
from pathlib import Path

records = [
    {"Date": "2026-01-02", "Close": 100.0, "Return": None, "Ticker": "IBM"},
    {"Date": "2026-01-05", "Close": 101.5, "Return": 0.015, "Ticker": "IBM"},
    {"Date": "2026-01-06", "Close": 99.8, "Return": -0.016749, "Ticker": "IBM"},
]

# dropna 的核心逻辑：只保留 Return 不是缺失值的记录
clean_records = [row for row in records if row["Return"] is not None]

with tempfile.TemporaryDirectory() as folder:
    csv_path = Path(folder) / "ibm_daily.csv"
    pickle_path = Path(folder) / "ibm_daily.pkl"

    # CSV 写入需要先指定列名 fieldnames
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(clean_records)

    # pickle 直接序列化 Python 对象并保留数据类型
    with pickle_path.open("wb") as file:
        pickle.dump(clean_records, file)

    with pickle_path.open("rb") as file:
        reloaded = pickle.load(file)

    print("Clean row count =", len(clean_records))
    print("CSV created =", csv_path.exists())
    print("Reloaded pickle =", reloaded)
""",
        "The missing first return is removed, and the cleaned records can be restored from pickle with their numeric types intact.",
    )
    return notebook(cells)


def chapter_5():
    cells = [
        chapter_header(
            5,
            "Bond and Stock Valuation",
            [
                "APR, effective rates, and continuous compounding",
                "Zero-coupon and coupon bond prices",
                "Yield to maturity",
                "Macaulay and modified duration",
                "Dividend discount stock valuation",
            ],
        )
    ]
    add_topic(
        cells,
        "5.1 Effective Rates and APR Conversion",
        "APR is a quoted annual rate. The effective annual rate reflects intra-year compounding: $EAR=(1+APR/m)^m-1$.",
        """
'''
本单元实现 EAR、不同频率的有效利率和对应 APR。
利率频率转换必须保持同一年度增长因子不变。
'''
def effective_annual_rate(apr, frequency):
    # APR 除以频率得到每个复利期的有效利率
    return (1 + apr / frequency) ** frequency - 1

def equivalent_period_rate(apr1, frequency1, frequency2):
    # 先保持年度增长因子，再转换为目标频率下的单期利率
    return (1 + apr1 / frequency1) ** (frequency1 / frequency2) - 1

def equivalent_apr(apr1, frequency1, frequency2):
    # 目标 APR = 目标单期有效利率 × 目标频率
    return equivalent_period_rate(apr1, frequency1, frequency2) * frequency2

print("EAR =", round(effective_annual_rate(0.10, 2), 6))
print("Quarterly period rate =", round(equivalent_period_rate(0.10, 2, 4), 6))
print("Equivalent quarterly APR =", round(equivalent_apr(0.10, 2, 4), 6))
""",
        "A 10% APR compounded semiannually has a 10.25% effective annual rate.",
    )
    add_topic(
        cells,
        "5.2 Continuous Compounding",
        "A discrete effective rate $R_m$ converts to a continuous annual rate using $R_c=m\\ln(1+R_m)$.",
        """
'''
本单元比较离散复利与连续复利终值。
正确转换后，两种计息方式应产生相同终值。
'''
from math import exp, log

def periodic_to_continuous(period_rate, frequency):
    # 连续年利率等于频率乘以单期增长因子的自然对数
    return frequency * log(1 + period_rate)

period_rate = 0.10
frequency = 1
years = 2
continuous_rate = periodic_to_continuous(period_rate, frequency)

discrete_fv = 100 * (1 + period_rate) ** (frequency * years)
continuous_fv = 100 * exp(continuous_rate * years)

print("Continuous rate =", round(continuous_rate, 6))
print("Discrete FV =", round(discrete_fv, 4))
print("Continuous FV =", round(continuous_fv, 4))
""",
        "The future values match because the rate conversion preserves the growth factor.",
    )
    add_topic(
        cells,
        "5.3 Zero-Coupon and Coupon Bond Pricing",
        "A bond price equals the present value of coupons plus the present value of face value. A zero-coupon bond has only the final face-value cash flow.",
        """
'''
本单元对零息债和附息债进行定价。
YTM 和票息支付次数必须转换为相同的每期频率。
'''
def zero_coupon_price(face_value, ytm, years, frequency=1):
    # 每期折现率为 ytm/frequency，总期数为 years*frequency
    return face_value / (1 + ytm / frequency) ** (years * frequency)

def coupon_bond_price(face_value, coupon_rate, ytm, years, frequency):
    periods = years * frequency
    coupon = face_value * coupon_rate / frequency
    price = 0.0

    for period in range(1, periods + 1):
        # 每一期票息都按对应期数折现
        price += coupon / (1 + ytm / frequency) ** period

    # 到期面值单独折现后加入债券价格
    price += face_value / (1 + ytm / frequency) ** periods
    return price

print("Zero-coupon price =", round(zero_coupon_price(1000, 0.05, 10, 2), 2))
print("Coupon bond price =", round(coupon_bond_price(1000, 0.08, 0.06, 10, 2), 2))
""",
        "The coupon bond sells above par because its coupon rate exceeds its YTM.",
    )
    add_topic(
        cells,
        "5.4 Yield to Maturity",
        "YTM is the discount rate that equates the market price with the present value of promised bond cash flows.",
        """
'''
本单元使用 numpy_financial.rate 反求债券每期收益率，再年化为名义 YTM。
现价使用负号，因为买入债券是当前现金流出。
'''
import numpy_financial as npf

face_value = 1000
market_price = 600
coupon_rate = 0.04
years = 10
frequency = 2

# 每期票息 = 面值 × 年票息率 ÷ 每年支付次数
coupon = face_value * coupon_rate / frequency

# rate 返回每个半年期的内部收益率
periodic_ytm = npf.rate(years * frequency, coupon, -market_price, face_value)

# 名义年化 YTM = 每期收益率 × 每年期数
annual_ytm = periodic_ytm * frequency

print("Periodic YTM =", f"{periodic_ytm:.4%}")
print("Annualized YTM =", f"{annual_ytm:.4%}")
""",
        "The deeply discounted bond has a YTM substantially above its 4% coupon rate.",
    )
    add_topic(
        cells,
        "5.5 Macaulay and Modified Duration",
        "Macaulay duration is the present-value-weighted average time of cash flows. Modified duration approximates percentage price sensitivity.",
        """
'''
本单元逐期计算现金流现值权重，并得到 Macaulay 与修正久期。
最后一期现金流必须同时包含票息和面值。
'''
def bond_price_and_duration(face_value, coupon_rate, ytm, years, frequency):
    periods = years * frequency
    coupon = face_value * coupon_rate / frequency
    present_values = []
    times = []

    for period in range(1, periods + 1):
        # 最后一期现金流增加面值偿还
        cash_flow = coupon + (face_value if period == periods else 0)
        pv = cash_flow / (1 + ytm / frequency) ** period
        present_values.append(pv)
        times.append(period / frequency)

    price = sum(present_values)

    # 久期 = 各现金流时间 × 现值权重 的总和
    macaulay = sum(t * pv / price for t, pv in zip(times, present_values))

    # 修正久期用于近似价格百分比变化
    modified = macaulay / (1 + ytm / frequency)
    return price, macaulay, modified

price, macaulay, modified = bond_price_and_duration(1000, 0.07, 0.05, 10, 2)
estimated_change = -modified * 0.002

print("Price =", round(price, 2))
print("Macaulay duration =", round(macaulay, 4))
print("Modified duration =", round(modified, 4))
print("Estimated price change for +20 bps =", f"{estimated_change:.4%}")
""",
        "The negative sign captures the inverse relation between bond price and yield.",
    )
    add_topic(
        cells,
        "5.6 Multi-Stage Dividend Discount Model",
        "Stock value equals the present value of forecast dividends plus the discounted terminal price, where $P_n=D_{n+1}/(r-g)$.",
        """
'''
本单元计算有限预测期股利与终值的现值。
终值使用下一期股利，因此需要把最后一期股利乘以 (1+g)。
'''
def multi_stage_stock_value(dividends, required_return, perpetual_growth):
    explicit_value = 0.0

    for year, dividend in enumerate(dividends, start=1):
        # 每期股利按 required_return 折现回 0 期
        explicit_value += dividend / (1 + required_return) ** year

    # 终值位于最后一个预测期，分子是下一期股利
    next_dividend = dividends[-1] * (1 + perpetual_growth)
    terminal_value = next_dividend / (required_return - perpetual_growth)
    discounted_terminal = terminal_value / (1 + required_return) ** len(dividends)

    return explicit_value + discounted_terminal

dividends = [1.80, 2.07, 2.277, 2.48193, 2.680]
value = multi_stage_stock_value(dividends, 0.182, 0.03)
print("Estimated stock value =", round(value, 2))
""",
        "Most of a growth stock's value may come from the terminal component, so the required return and growth assumptions matter greatly.",
    )
    add_topic(
        cells,
        "5.7 Credit Spreads and the Price-YTM Relationship",
        """
Credit spreads are commonly quoted in basis points, where 100 basis points
equal one percentage point. A corporate yield can be approximated as the
risk-free yield plus a rating spread. Bond price moves inversely with YTM.
""",
        """
'''
本单元补充老师源代码中的信用利差与价格-YTM关系。
1 个基点等于 0.0001，50 个基点等于 0.50%。
'''
def coupon_bond_price(face_value, coupon_rate, ytm, years, frequency):
    periods = years * frequency
    coupon = face_value * coupon_rate / frequency
    return sum(
        (coupon + (face_value if period == periods else 0))
        / (1 + ytm / frequency) ** period
        for period in range(1, periods + 1)
    )

risk_free_yield = 0.035
spread_basis_points = 50

# 基点转换为小数利率：除以 10,000
credit_spread = spread_basis_points / 10_000
corporate_ytm = risk_free_yield + credit_spread

ytm_values = [0.04, 0.05, 0.06, 0.07, corporate_ytm]
prices = [coupon_bond_price(1000, 0.06, ytm, 10, 2) for ytm in ytm_values]

print("Credit spread =", f"{credit_spread:.2%}")
print("Corporate YTM =", f"{corporate_ytm:.2%}")
for ytm, price in zip(ytm_values, prices):
    print(f"YTM={ytm:.2%}, price={price:.2f}")
""",
        "As YTM increases, the present value of fixed bond cash flows falls. The basis-point conversion is essential when adding a credit spread.",
    )
    return notebook(cells)


def ols_code(factors=1):
    factor_names = ["Market", "SMB", "HML", "MOM", "RMW", "CMA"][:factors]
    names_literal = repr(factor_names)
    return f"""
'''
本单元使用矩阵公式估计多元线性回归，避免依赖特定回归软件。
X 第一列加入常数 1，对应回归截距 alpha。
'''
import numpy as np

rng = np.random.default_rng(300 + {factors})
n = 360
factor_names = {names_literal}
factors = rng.normal(0, 0.01, (n, len(factor_names)))
true_betas = np.linspace(1.10, 0.25, len(factor_names))
asset_excess_return = 0.0002 + factors @ true_betas + rng.normal(0, 0.008, n)

# np.column_stack 加入常数列，形成 [1, factor1, factor2, ...]
X = np.column_stack([np.ones(n), factors])

# 最小二乘解 beta_hat = (X'X)^(-1)X'y；lstsq 数值更稳定
coefficients = np.linalg.lstsq(X, asset_excess_return, rcond=None)[0]
fitted = X @ coefficients
residuals = asset_excess_return - fitted

# R-squared = 1 - SSE/SST
r_squared = 1 - np.sum(residuals**2) / np.sum((asset_excess_return - asset_excess_return.mean())**2)

# 调整 R-squared 对因子数量进行惩罚
p = len(factor_names)
adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)

print("Factor names =", factor_names)
print("Estimated [alpha, betas] =", np.round(coefficients, 4))
print("R-squared =", round(float(r_squared), 4))
print("Adjusted R-squared =", round(float(adjusted_r_squared), 4))
"""


def chapter_6():
    cells = [
        chapter_header(
            6,
            "Capital Asset Pricing Model",
            [
                "Simple linear regression",
                "CAPM alpha and beta",
                "Merging asset and market returns",
                "Statistical significance of beta",
                "Rolling beta and portfolio beta",
            ],
        )
    ]
    add_topic(
        cells,
        "6.1 Simple Linear Regression",
        "A one-factor model is $y=\\alpha+\\beta x+\\epsilon$. The slope measures the change in the dependent variable associated with a one-unit change in the factor.",
        ols_code(1),
        "The estimated market coefficient is close to the simulated true beta, and R-squared measures explained variation.",
    )
    add_topic(
        cells,
        "6.2 CAPM Alpha and Beta",
        "CAPM time-series regression is $R_i-R_f=\\alpha+\\beta(R_m-R_f)+\\epsilon$. Beta is systematic market risk; alpha is abnormal return.",
        """
'''
本单元用协方差公式和 OLS 矩阵公式分别估计 CAPM beta。
单因子回归中，beta 也等于 Cov(Ri,Rm)/Var(Rm)。
'''
import numpy as np

rng = np.random.default_rng(606)
market_excess = rng.normal(0.0004, 0.011, 300)
stock_excess = 0.00015 + 1.25 * market_excess + rng.normal(0, 0.012, 300)

# 协方差矩阵 [0,1] 为协方差，[0,0] 为市场方差
covariance_matrix = np.cov(market_excess, stock_excess, ddof=1)
beta_covariance = covariance_matrix[0, 1] / covariance_matrix[0, 0]

# OLS 需要常数列来估计 alpha
X = np.column_stack([np.ones(len(market_excess)), market_excess])
alpha_ols, beta_ols = np.linalg.lstsq(X, stock_excess, rcond=None)[0]

print("Beta from covariance =", round(float(beta_covariance), 4))
print("OLS alpha =", round(float(alpha_ols), 6))
print("OLS beta =", round(float(beta_ols), 4))
""",
        "The two beta estimates match because the model contains one explanatory factor and an intercept.",
    )
    add_topic(
        cells,
        "6.3 Joining Asset and Market Data by Date",
        "CAPM requires aligned observations. An inner join retains only dates available in both the stock and market datasets.",
        """
'''
本单元用日期字典演示 inner join，避免网络和文件依赖。
只有同时出现在股票和市场数据中的日期才进入回归样本。
'''
stock_returns = {
    "2026-01-02": 0.010,
    "2026-01-05": -0.004,
    "2026-01-06": 0.006,
}
market_returns = {
    "2026-01-02": 0.007,
    "2026-01-06": 0.003,
    "2026-01-07": -0.002,
}

# 集合交集找到两个数据源共有的交易日
common_dates = sorted(set(stock_returns) & set(market_returns))

# 按相同日期顺序构造对齐样本
joined = [(date, stock_returns[date], market_returns[date]) for date in common_dates]

print("Common dates =", common_dates)
print("Joined observations =", joined)
""",
        "January 5 and January 7 are removed because each appears in only one source.",
    )
    add_topic(
        cells,
        "6.4 Testing Whether Beta Differs from Zero",
        "A t-statistic divides the estimated beta minus its null value by its standard error. Reject $H_0:\\beta=0$ when the two-sided p-value is below alpha.",
        """
'''
本单元从 OLS 残差计算 beta 标准误、t 值和双侧 p 值。
自由度等于样本量减去估计参数个数。
'''
import numpy as np
from scipy import stats

rng = np.random.default_rng(607)
x = rng.normal(0, 0.01, 180)
y = 0.0001 + 1.10 * x + rng.normal(0, 0.009, 180)
X = np.column_stack([np.ones(len(x)), x])
coefficients = np.linalg.lstsq(X, y, rcond=None)[0]
residuals = y - X @ coefficients

# 残差方差 = SSE / (n-k)
degrees_of_freedom = len(y) - X.shape[1]
residual_variance = np.sum(residuals**2) / degrees_of_freedom

# 系数协方差矩阵 = 残差方差 × (X'X)^(-1)
coefficient_covariance = residual_variance * np.linalg.inv(X.T @ X)
beta_standard_error = np.sqrt(coefficient_covariance[1, 1])

# t 值 = (估计 beta - 原假设 beta) / 标准误
t_value = coefficients[1] / beta_standard_error
p_value = 2 * (1 - stats.t.cdf(abs(t_value), degrees_of_freedom))

print("Estimated beta =", round(float(coefficients[1]), 4))
print("t-value =", round(float(t_value), 4))
print("p-value =", round(float(p_value), 8))
print("Decision =", "Reject H0" if p_value < 0.05 else "Do not reject H0")
""",
        "A small p-value indicates that market exposure is statistically different from zero.",
    )
    add_topic(
        cells,
        "6.5 Rolling Beta and Portfolio Beta",
        "Rolling or subperiod beta reveals time variation. Portfolio beta is the value-weighted average of component betas.",
        """
'''
本单元按年度分别估计 beta，并计算投资组合 beta。
每个年度都必须重新构造 X 和 y，不能直接复用全样本回归。
'''
import numpy as np

rng = np.random.default_rng(608)
years = np.repeat([2023, 2024, 2025], 120)
market = rng.normal(0.0003, 0.011, len(years))
true_yearly_betas = {2023: 0.8, 2024: 1.1, 2025: 1.4}
stock = np.array([
    true_yearly_betas[year] * market[i] + rng.normal(0, 0.008)
    for i, year in enumerate(years)
])

estimated_betas = {}
for year in np.unique(years):
    # 布尔掩码选出当前年度的股票和市场收益率
    mask = years == year
    X = np.column_stack([np.ones(mask.sum()), market[mask]])
    estimated_betas[int(year)] = np.linalg.lstsq(X, stock[mask], rcond=None)[0][1]

component_betas = np.array([0.8, 1.2, 1.5])
weights = np.array([0.25, 0.50, 0.25])

# 投资组合 beta = 各资产权重与 beta 的点积
portfolio_beta = weights @ component_betas

print("Annual betas =", {k: round(float(v), 3) for k, v in estimated_betas.items()})
print("Portfolio beta =", round(float(portfolio_beta), 3))
""",
        "The annual estimates track changing systematic risk, while the portfolio beta summarizes current weighted exposure.",
    )
    add_topic(
        cells,
        "6.6 Alternative Regression and Join Methods",
        """
The classroom script compares `scipy.stats.linregress` with OLS and demonstrates
left, right, inner, and outer joins. These are different interfaces to recurring
data-analysis tasks.
""",
        """
'''
本单元补充 linregress 与四种连接方式。
回归参数顺序必须是 linregress(x, y)，斜率才表示 x 对 y 的解释。
'''
from scipy import stats

market = [0.055, -0.090, -0.041, 0.045, 0.022]
stock = [0.065, 0.0265, -0.0593, -0.001, 0.0345]

# x 放市场收益，y 放股票收益
regression = stats.linregress(market, stock)
print("linregress alpha =", round(regression.intercept, 4))
print("linregress beta =", round(regression.slope, 4))
print("R-squared =", round(regression.rvalue**2, 4))

left = {"foo": 1, "bar": 2}
right = {"foo": 3, "baz": 4}

# inner 只保留双方共有键
inner_keys = sorted(set(left) & set(right))

# left 保留左表全部键；right 保留右表全部键；outer 取并集
left_keys = sorted(left)
right_keys = sorted(right)
outer_keys = sorted(set(left) | set(right))

print("Inner keys =", inner_keys)
print("Left keys =", left_keys)
print("Right keys =", right_keys)
print("Outer keys =", outer_keys)
""",
        "The regression slope is CAPM beta when market return is the independent variable. Join type determines which unmatched observations survive.",
    )
    return notebook(cells)


def chapter_7():
    cells = [
        chapter_header(
            7,
            "Multifactor Models and Performance Measures",
            [
                "Fama-French three-factor regression",
                "Carhart four-factor and Fama-French five-factor models",
                "R-squared, adjusted R-squared, and the F-test",
                "Sharpe, Treynor, Sortino, and Jensen alpha",
                "Preparing factor data and date indices",
            ],
        )
    ]
    add_topic(cells, "7.1 Fama-French Three-Factor Model", "The model explains excess return using market, size (SMB), and value (HML) factors.", ols_code(3), "The coefficients are factor exposures; adjusted R-squared is preferable when comparing models with different factor counts.")
    add_topic(cells, "7.2 Four- and Five-Factor Models", "Carhart adds momentum (MOM). The five-factor model adds profitability (RMW) and investment (CMA).", ols_code(6), "The expanded model estimates six factor exposures. Extra factors should be retained only when they add explanatory value.")
    add_topic(
        cells,
        "7.3 Overall F-Test for a Factor Model",
        "The overall F-test evaluates whether all slope coefficients are jointly zero. A small p-value means at least one factor contributes explanatory power.",
        """
'''
本单元从 R-squared 构造整体 F 统计量。
k 是斜率因子数，不包括常数项；n-k-1 是残差自由度。
'''
from scipy import stats

n = 477
k = 3
r_squared = 0.022
alpha = 0.05

# F = (R2/k) / ((1-R2)/(n-k-1))
f_value = (r_squared / k) / ((1 - r_squared) / (n - k - 1))

# F 检验位于右尾，因此使用 1-CDF 计算 p 值
p_value = 1 - stats.f.cdf(f_value, k, n - k - 1)
critical_value = stats.f.ppf(1 - alpha, k, n - k - 1)

print("F-value =", round(float(f_value), 4))
print("Critical F =", round(float(critical_value), 4))
print("p-value =", round(float(p_value), 6))
print("Decision =", "Reject H0" if p_value < alpha else "Do not reject H0")
""",
        "The test concerns all factor slopes jointly, unlike individual t-tests.",
    )
    add_topic(
        cells,
        "7.4 Risk-Adjusted Performance Measures",
        """
Sharpe uses total risk; Treynor uses beta; Sortino uses downside risk. Jensen
alpha is realized excess return minus CAPM-predicted excess return.
""",
        """
'''
本单元计算四种常用绩效指标。
所有收益率和无风险利率必须使用相同频率。
'''
import numpy as np

returns = np.array([0.04, -0.02, 0.03, 0.01, -0.01, 0.05, 0.02])
risk_free = 0.005
market_mean = 0.018
beta = 1.20

mean_return = returns.mean()
total_risk = returns.std(ddof=1)

# Sharpe = 平均超额收益 / 总标准差
sharpe = (mean_return - risk_free) / total_risk

# Treynor = 平均超额收益 / beta
treynor = (mean_return - risk_free) / beta

# 下行收益只保留低于基准 risk_free 的观测
downside = returns[returns < risk_free]
downside_deviation = np.sqrt(np.mean((downside - risk_free) ** 2))
sortino = (mean_return - risk_free) / downside_deviation

# Jensen alpha = 实际超额收益 - beta × 市场超额收益
jensen_alpha = (mean_return - risk_free) - beta * (market_mean - risk_free)

print("Sharpe =", round(float(sharpe), 4))
print("Treynor =", round(float(treynor), 4))
print("Sortino =", round(float(sortino), 4))
print("Jensen alpha =", round(float(jensen_alpha), 4))
""",
        "Different measures answer different risk questions, so their denominators should not be interchanged.",
    )
    add_topic(
        cells,
        "7.5 Preparing Fama-French Dates and Percentages",
        "Academic factor files often encode dates as integers and returns as percentages. Before merging, convert both date and units consistently.",
        """
'''
本单元把 YYYYMMDD 整数日期转换为 datetime，并把百分数转换为小数。
这是合并 Fama-French 数据前最容易出现填空错误的步骤。
'''
from datetime import datetime

raw_rows = [
    (20260102, 0.35, -0.12, 0.08, 0.01),
    (20260105, -0.20, 0.05, -0.03, 0.01),
]

processed = []
for raw_date, market_rf, smb, hml, rf in raw_rows:
    # strptime 的格式 %Y%m%d 对应 8 位整数日期
    date = datetime.strptime(str(raw_date), "%Y%m%d").date()

    # 因子文件通常以百分数表示，除以 100 转换为小数收益率
    factors = tuple(value / 100 for value in (market_rf, smb, hml, rf))
    processed.append((date, *factors))

print("Processed factor rows =")
for row in processed:
    print(row)
""",
        "The processed rows are ready for date-indexed merging with asset returns.",
    )
    add_topic(
        cells,
        "7.6 Lower Partial Standard Deviation",
        """
LPSD measures only returns below a benchmark. It is the downside-risk
denominator used by the Sortino ratio and appears explicitly in the classroom
source code.
""",
        """
'''
本单元封装下行标准差 LPSD。
先筛选低于基准的收益率，再计算相对基准的平方偏差。
'''
import numpy as np

def lower_partial_standard_deviation(returns, benchmark):
    returns = np.asarray(returns, dtype=float)

    # 布尔筛选只保留低于 benchmark 的下行观测
    downside_returns = returns[returns < benchmark]
    if len(downside_returns) < 2:
        return 0.0

    # LPSD 使用下行偏差的样本均方根
    variance = np.sum((downside_returns - benchmark) ** 2) / (len(downside_returns) - 1)
    return np.sqrt(variance)

returns = np.array([0.04, -0.02, 0.03, -0.01, 0.01, -0.04, 0.05])
benchmark = 0.005
lpsd = lower_partial_standard_deviation(returns, benchmark)
sortino = (returns.mean() - benchmark) / lpsd

print("LPSD =", round(float(lpsd), 5))
print("Sortino ratio =", round(float(sortino), 5))
""",
        "Only observations below the benchmark enter LPSD, unlike standard deviation, which treats upside and downside variation symmetrically.",
    )
    add_topic(
        cells,
        "7.7 Classroom Extension: Maximizing a Portfolio Sharpe Ratio",
        """
The source script extends performance measurement to multiple assets and uses
optimization. Because portfolio weights sum to one, only `n-1` weights are
independent; the final weight can be inferred.
""",
        """
'''
本单元补充源代码中的多资产 Sharpe Ratio 优化。
优化器执行最小化，因此目标函数返回负的 Sharpe Ratio。
'''
import numpy as np
from scipy.optimize import minimize

expected_returns = np.array([0.08, 0.11, 0.06])
covariance = np.array([
    [0.040, 0.012, 0.008],
    [0.012, 0.062, 0.010],
    [0.008, 0.010, 0.025],
])
risk_free = 0.02

def portfolio_sharpe(weights):
    portfolio_return = weights @ expected_returns
    # 组合方差的矩阵公式为 w'Σw
    portfolio_variance = weights @ covariance @ weights
    return (portfolio_return - risk_free) / np.sqrt(portfolio_variance)

def negative_sharpe(weights):
    # minimize 负 Sharpe 等价于 maximize Sharpe
    return -portfolio_sharpe(weights)

constraints = {"type": "eq", "fun": lambda weights: weights.sum() - 1}
bounds = [(0, 1)] * len(expected_returns)
initial_weights = np.ones(len(expected_returns)) / len(expected_returns)

result = minimize(
    negative_sharpe,
    initial_weights,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints,
)

print("Optimal weights =", np.round(result.x, 4))
print("Weight sum =", round(float(result.x.sum()), 6))
print("Optimal Sharpe =", round(float(portfolio_sharpe(result.x)), 4))
""",
        "The constraints enforce full investment and no short selling. Returning negative Sharpe corrects the direction problem that can occur when using a minimizer.",
    )
    return notebook(cells)


def chapter_8():
    cells = [
        chapter_header(
            8,
            "Time-Series Analysis and Hypothesis Testing",
            [
                "Normal, Student-t, F, and chi-square distributions",
                "Confidence intervals and mean tests",
                "Equal-variance and equal-mean tests",
                "Durbin-Watson autocorrelation",
                "Granger causality",
                "Interpolation and calendar effects",
            ],
        )
    ]
    add_topic(
        cells,
        "8.1 Distribution Functions: PDF, CDF, and PPF",
        "PDF measures density, CDF gives cumulative probability, and PPF is the inverse CDF used to obtain critical values.",
        """
'''
本单元比较正态、t、F 和卡方分布的关键函数。
ppf 输入概率并返回临界值，是考试常见填空。
'''
from scipy import stats

alpha = 0.05

# 双侧 95% 正态置信区间使用 alpha/2 和 1-alpha/2
z_left = stats.norm.ppf(alpha / 2)
z_right = stats.norm.ppf(1 - alpha / 2)

# t 临界值还需要自由度参数
t_right = stats.t.ppf(1 - alpha / 2, df=29)

# F 检验通常使用右尾临界值
f_right = stats.f.ppf(1 - alpha, dfn=10, dfd=12)

# chi2 是卡方分布；不要误用 chi 分布
chi_right = stats.chi2.ppf(1 - alpha, df=4)

print("Normal critical values =", round(z_left, 4), round(z_right, 4))
print("Student-t critical value =", round(t_right, 4))
print("F critical value =", round(f_right, 4))
print("Chi-square critical value =", round(chi_right, 4))
""",
        "The t critical value is wider than the normal value because finite-sample uncertainty produces heavier tails.",
    )
    add_topic(
        cells,
        "8.2 Confidence Interval for a Mean",
        "When population volatility is unknown, use the sample standard deviation and a Student-t critical value.",
        """
'''
本单元构造平均收益率的双侧 t 置信区间。
标准误等于样本标准差除以样本量平方根。
'''
import numpy as np
from scipy import stats

rng = np.random.default_rng(802)
returns = rng.normal(0.0005, 0.012, 60)
alpha = 0.05
n = len(returns)
sample_mean = returns.mean()
sample_std = returns.std(ddof=1)

# 标准误衡量样本均值的抽样波动
standard_error = sample_std / np.sqrt(n)

# 双侧区间使用 1-alpha/2 分位数
t_critical = stats.t.ppf(1 - alpha / 2, df=n - 1)
margin = t_critical * standard_error
lower, upper = sample_mean - margin, sample_mean + margin

print("Sample mean =", round(float(sample_mean), 6))
print("95% CI =", (round(float(lower), 6), round(float(upper), 6)))
print("Is zero inside? =", lower <= 0 <= upper)
""",
        "If zero lies inside the interval, the data do not provide enough evidence that mean return differs from zero at the 5% level.",
    )
    add_topic(
        cells,
        "8.3 Equal Variances and Equal Means",
        "Levene's test evaluates equal variances. The variance result helps choose between the pooled and Welch two-sample t-tests.",
        """
'''
本单元先检验方差，再检验均值。
Levene p 值较小时拒绝等方差假设，并优先使用 Welch t 检验。
'''
import numpy as np
from scipy import stats

rng = np.random.default_rng(803)
asset_a = rng.normal(0.0010, 0.010, 120)
asset_b = rng.normal(0.0015, 0.016, 120)
alpha = 0.05

# Levene 检验 H0：两个总体方差相等
levene_result = stats.levene(asset_a, asset_b)
equal_variance = levene_result.pvalue >= alpha

# equal_var=False 对应 Welch t 检验
t_result = stats.ttest_ind(asset_a, asset_b, equal_var=equal_variance)

print("Levene p-value =", round(float(levene_result.pvalue), 6))
print("Assume equal variance? =", equal_variance)
print("Mean-test p-value =", round(float(t_result.pvalue), 6))
""",
        "Testing variance first prevents mechanically applying the pooled t-test when dispersion differs substantially.",
    )
    add_topic(
        cells,
        "8.4 Durbin-Watson Autocorrelation Test",
        "Durbin-Watson is approximately 2 without first-order autocorrelation, below 2 for positive autocorrelation, and above 2 for negative autocorrelation.",
        """
'''
本单元直接实现 Durbin-Watson 统计量。
分子是相邻残差差值平方和，分母是残差平方和。
'''
import numpy as np

rng = np.random.default_rng(804)
errors = np.zeros(200)
for t in range(1, len(errors)):
    # 构造正自相关误差：当前误差依赖上一期误差
    errors[t] = 0.65 * errors[t - 1] + rng.normal(0, 1)

# np.diff 计算 e_t - e_(t-1)
durbin_watson = np.sum(np.diff(errors) ** 2) / np.sum(errors ** 2)

interpretation = (
    "positive autocorrelation" if durbin_watson < 1.5
    else "negative autocorrelation" if durbin_watson > 2.5
    else "weak or no autocorrelation"
)

print("Durbin-Watson =", round(float(durbin_watson), 4))
print("Interpretation =", interpretation)
""",
        "The simulated autoregressive errors should produce a statistic clearly below two.",
    )
    add_topic(
        cells,
        "8.5 Granger Causality by Restricted and Unrestricted Models",
        "X Granger-causes Y when lagged X values improve prediction of Y beyond lagged Y values. This is predictive precedence, not philosophical causation.",
        """
'''
本单元比较受限模型与非受限模型的残差平方和，并计算 Granger F 统计量。
受限模型只含 y 的滞后项，非受限模型再加入 x 的滞后项。
'''
import numpy as np
from scipy import stats

rng = np.random.default_rng(805)
n = 250
x = rng.normal(0, 1, n)
y = np.zeros(n)
for t in range(2, n):
    # y 同时受自身一期滞后和 x 一期滞后影响
    y[t] = 0.4 * y[t - 1] + 0.7 * x[t - 1] + rng.normal(0, 0.8)

target = y[2:]
y_lags = np.column_stack([y[1:-1], y[:-2]])
x_lags = np.column_stack([x[1:-1], x[:-2]])

# 受限模型：常数项 + y 的两个滞后
X_restricted = np.column_stack([np.ones(len(target)), y_lags])

# 非受限模型：再加入 x 的两个滞后
X_unrestricted = np.column_stack([X_restricted, x_lags])

resid_r = target - X_restricted @ np.linalg.lstsq(X_restricted, target, rcond=None)[0]
resid_u = target - X_unrestricted @ np.linalg.lstsq(X_unrestricted, target, rcond=None)[0]
rss_r = np.sum(resid_r**2)
rss_u = np.sum(resid_u**2)

# q 是新增的 x 滞后项数量
q = x_lags.shape[1]
df_denominator = len(target) - X_unrestricted.shape[1]
f_value = ((rss_r - rss_u) / q) / (rss_u / df_denominator)
p_value = 1 - stats.f.cdf(f_value, q, df_denominator)

print("Granger F-value =", round(float(f_value), 4))
print("p-value =", round(float(p_value), 8))
print("Conclusion =", "X Granger-causes Y" if p_value < 0.05 else "No evidence of Granger causality")
""",
        "The unrestricted model should fit materially better because the data-generating process includes lagged X.",
    )
    add_topic(
        cells,
        "8.6 Linear Interpolation and the January Effect",
        "Interpolation estimates internal missing values. A calendar-effect test compares January returns with non-January returns.",
        """
'''
本单元先对缺失序列做线性插值，再检验一月收益率是否不同。
插值只适用于内部缺口，不能替代对数据生成过程的判断。
'''
import numpy as np
from scipy import stats

series = np.array([1.0, 2.0, np.nan, np.nan, 6.0])
missing = np.isnan(series)

# np.interp 根据左右有效点对缺失位置进行线性插值
series[missing] = np.interp(
    np.flatnonzero(missing),
    np.flatnonzero(~missing),
    series[~missing],
)

rng = np.random.default_rng(806)
months = np.tile(np.arange(1, 13), 15)
monthly_returns = rng.normal(0.008, 0.04, len(months))
monthly_returns[months == 1] += 0.02

# 按月份标签拆分 January 与 non-January 样本
january = monthly_returns[months == 1]
non_january = monthly_returns[months != 1]
test = stats.ttest_ind(january, non_january, equal_var=False)

print("Interpolated series =", series)
print("January mean =", round(float(january.mean()), 4))
print("Non-January mean =", round(float(non_january.mean()), 4))
print("January-effect p-value =", round(float(test.pvalue), 6))
""",
        "The statistical result depends on sampling variation even though the simulation adds a positive January premium.",
    )
    add_topic(
        cells,
        "8.7 Manual F-Test for Equal Variances",
        """
The instructor demonstrates the classical F statistic as the larger sample
variance divided by the smaller sample variance, followed by comparison with a
right-tail critical value.
""",
        """
'''
本单元补充手工 F 方差检验，并与 Levene 检验区分。
将大方差放在分子可保证 F 值不小于 1。
'''
import numpy as np
from scipy import stats

rng = np.random.default_rng(807)
group_1 = rng.normal(0, 1.0, 40)
group_2 = rng.normal(0, 1.5, 35)
alpha = 0.05

variance_1 = group_1.var(ddof=1)
variance_2 = group_2.var(ddof=1)

if variance_1 >= variance_2:
    f_value = variance_1 / variance_2
    df_numerator, df_denominator = len(group_1) - 1, len(group_2) - 1
else:
    f_value = variance_2 / variance_1
    df_numerator, df_denominator = len(group_2) - 1, len(group_1) - 1

# 右尾临界值使用 1-alpha
f_critical = stats.f.ppf(1 - alpha, df_numerator, df_denominator)

print("F-value =", round(float(f_value), 4))
print("Critical F =", round(float(f_critical), 4))
print("Decision =", "Reject equal variances" if f_value > f_critical else "Do not reject equal variances")
""",
        "The manual F-test is sensitive to non-normality; Levene's test is often preferred for robustness.",
    )
    add_topic(
        cells,
        "8.8 Normality Tests",
        """
The source code includes Shapiro-Wilk and Anderson-Darling tests. Both assess
normality, which matters because many classical finance models assume normally
distributed errors or returns.
""",
        """
'''
本单元补充 Shapiro-Wilk 与 Anderson-Darling 正态性检验。
Shapiro 使用 p 值；Anderson 将统计量与指定显著性水平的临界值比较。
'''
import numpy as np
from scipy import stats

rng = np.random.default_rng(808)
normal_returns = rng.normal(0, 0.01, 200)
heavy_tailed_returns = rng.standard_t(df=3, size=200) * 0.01

# Shapiro H0：样本来自正态分布
shapiro_normal = stats.shapiro(normal_returns)
shapiro_heavy = stats.shapiro(heavy_tailed_returns)

# Anderson 返回多个显著性水平对应的临界值
anderson_heavy = stats.anderson(heavy_tailed_returns, dist="norm")
five_percent_index = list(anderson_heavy.significance_level).index(5.0)
critical_5 = anderson_heavy.critical_values[five_percent_index]

print("Normal sample Shapiro p =", round(float(shapiro_normal.pvalue), 6))
print("Heavy-tail Shapiro p =", round(float(shapiro_heavy.pvalue), 6))
print("Heavy-tail Anderson statistic =", round(float(anderson_heavy.statistic), 4))
print("Anderson 5% critical value =", round(float(critical_5), 4))
""",
        "The heavy-tailed sample should be more likely to reject normality than the Gaussian sample.",
    )
    add_topic(
        cells,
        "8.9 Bidirectional Granger Testing",
        """
The classroom script emphasizes testing both directions. Evidence that X
predicts Y does not automatically imply that Y predicts X.
""",
        """
'''
本单元封装 Granger F 检验，并分别检验 x→y 与 y→x。
每个方向都需要单独建立受限和非受限模型。
'''
import numpy as np
from scipy import stats

def granger_test(cause, effect, lags=2):
    target = effect[lags:]
    effect_lags = np.column_stack([
        effect[lags - lag - 1 : -lag - 1] for lag in range(lags)
    ])
    cause_lags = np.column_stack([
        cause[lags - lag - 1 : -lag - 1] for lag in range(lags)
    ])

    restricted = np.column_stack([np.ones(len(target)), effect_lags])
    unrestricted = np.column_stack([restricted, cause_lags])

    residual_r = target - restricted @ np.linalg.lstsq(restricted, target, rcond=None)[0]
    residual_u = target - unrestricted @ np.linalg.lstsq(unrestricted, target, rcond=None)[0]
    rss_r, rss_u = np.sum(residual_r**2), np.sum(residual_u**2)

    # 新增限制数量等于 cause 的滞后项数量
    q = lags
    df_denominator = len(target) - unrestricted.shape[1]
    f_value = ((rss_r - rss_u) / q) / (rss_u / df_denominator)
    p_value = 1 - stats.f.cdf(f_value, q, df_denominator)
    return f_value, p_value

rng = np.random.default_rng(809)
n = 250
x = rng.normal(0, 1, n)
y = np.zeros(n)
for t in range(2, n):
    y[t] = 0.4 * y[t - 1] + 0.7 * x[t - 1] + rng.normal(0, 0.8)

x_to_y = granger_test(x, y)
y_to_x = granger_test(y, x)

print("X -> Y p-value =", round(float(x_to_y[1]), 8))
print("Y -> X p-value =", round(float(y_to_x[1]), 8))
""",
        "The simulated structure should support X-to-Y predictability more strongly than the reverse direction.",
    )
    return notebook(cells)


def assignment_header(number, title, questions):
    items = "\n".join(f"{i}. {question}" for i, question in enumerate(questions, 1))
    return markdown(
        f"""
# Assignment {number}: {title}

This notebook preserves the completed solution logic and reorganizes it for
exam revision. Each question contains an English problem summary, an
independently runnable solution, Chinese line-level hints, and result guidance.

## Questions

{items}

## Recommended Answer Structure

1. State the financial or statistical objective.
2. Identify inputs, assumptions, and units.
3. Write the main formula or algorithm before coding.
4. Complete the code in execution order.
5. Report and interpret the result.
6. Add a short validation or reasonableness check.

## Assignment Review Checklist

- Each question can run independently.
- Imports are included in the question's own code cell.
- Random simulations use a fixed seed.
- The final answer includes interpretation, not only printed output.
- Any chart is discussed in the result Markdown.
"""
    )


def assignment_1():
    cells = [
        assignment_header(
            1,
            "Environment, Return Engineering, and Portfolio Display",
            ["Environment inspection", "Multi-stock cleaning and quarterly returns", "Mean tests, Sharpe ratios, and wealth growth"],
        )
    ]
    add_topic(
        cells,
        "Question 1: Environment Inspection",
        "Inspect Python and the core numerical finance packages. Working-directory changes are intentionally excluded as a finance knowledge module.",
        """
'''
本题检查 Python、NumPy、SciPy 和 numpy_financial 环境。
dir() 可用于探索包中公开的函数名称。
'''
import sys
import numpy as np
import scipy
import numpy_financial as npf

# 过滤下划线开头的内部名称，只保留公开对象
financial_functions = [name for name in dir(npf) if not name.startswith("_")]

print("Python =", sys.version.split()[0])
print("NumPy =", np.__version__)
print("SciPy =", scipy.__version__)
print("numpy-financial functions =", financial_functions)
""",
        "The environment exposes functions such as `pv`, `fv`, `npv`, `irr`, and `rate`.",
    )
    add_topic(
        cells,
        "Question 2: Multi-Stock Cleaning and Quarterly Returns",
        "Create three financially plausible price paths, repair an isolated price gap, and compound daily returns by quarter.",
        """
'''
本题生成三只股票的价格路径，前向填充缺失价格，并计算季度复合收益率。
所有中间数据都在本单元创建，因此可独立运行。
'''
import numpy as np

rng = np.random.default_rng(2026)
tickers = ["AAPL", "MSFT", "GOOGL"]
n_days = 504
daily_log_returns = rng.normal([0.0005, 0.0004, 0.00045], [0.015, 0.013, 0.016], (n_days, 3))
prices = 100 * np.exp(np.cumsum(daily_log_returns, axis=0))
prices[5, 0] = np.nan

# 对每一只股票分别进行前向填充
for column in range(prices.shape[1]):
    for row in range(1, prices.shape[0]):
        if np.isnan(prices[row, column]):
            prices[row, column] = prices[row - 1, column]

# 由相邻价格计算日收益率
returns = prices[1:] / prices[:-1] - 1
quarter_labels = np.repeat(np.arange(1, 9), 63)[: len(returns)]

quarterly = {}
for quarter in np.unique(quarter_labels):
    selected = returns[quarter_labels == quarter]
    # axis=0 表示分别对三只股票的日增长因子连乘
    quarterly[int(quarter)] = np.prod(1 + selected, axis=0) - 1

print("Tickers =", tickers)
for quarter, values in list(quarterly.items())[:4]:
    print("Quarter", quarter, np.round(values, 4))
""",
        "The result is a three-element return vector for each quarter, with compounding performed independently by asset.",
    )
    add_topic(
        cells,
        "Question 3: Mean Tests, Sharpe Ratios, and Growth of One Dollar",
        "Compare two mean returns, calculate annualized Sharpe ratios, and produce the final value of a one-dollar investment.",
        """
'''
本题计算 Welch t 检验、年化 Sharpe Ratio 和累计财富。
年化时日均超额收益与日波动率都基于 252 个交易日。
'''
import numpy as np
from scipy import stats

rng = np.random.default_rng(2027)
returns = rng.normal([0.0006, 0.0005, 0.0007], [0.015, 0.013, 0.016], (503, 3))
tickers = ["AAPL", "MSFT", "GOOGL"]

# Welch 检验不要求两组收益率方差相等
test = stats.ttest_ind(returns[:, 0], returns[:, 1], equal_var=False)

annual_rf = 0.01
daily_rf = (1 + annual_rf) ** (1 / 252) - 1

# Sharpe 年化：日超额收益均值/日标准差 × sqrt(252)
sharpe = (returns.mean(axis=0) - daily_rf) / returns.std(axis=0, ddof=1) * np.sqrt(252)

# cumprod 对增长因子连乘，最后一行是 1 元投资的期末价值
final_wealth = np.cumprod(1 + returns, axis=0)[-1]

print("Mean-test p-value =", round(float(test.pvalue), 6))
print("Sharpe ratios =", dict(zip(tickers, np.round(sharpe, 3))))
print("Final value of $1 =", dict(zip(tickers, np.round(final_wealth, 3))))
""",
        "The p-value addresses statistical mean differences; Sharpe and terminal wealth address risk-adjusted and cumulative performance.",
    )
    return notebook(cells)


def assignment_2():
    cells = [
        assignment_header(2, "Bond Sensitivity and CAPM Beta", ["Bond valuation and duration", "Technology-stock CAPM beta estimation"])
    ]
    add_topic(
        cells,
        "Question 1: Bond Valuation and Duration",
        "Calculate price and Macaulay duration at two YTM levels, preserving the completed assignment logic.",
        """
'''
本题计算附息债价格和 Macaulay 久期，并比较不同 YTM。
最后一期现金流需要加回面值，这是常见代码填空点。
'''
def bond_price(face_value, coupon_rate, ytm, years, frequency):
    coupon = face_value * coupon_rate / frequency
    periods = years * frequency
    return sum(
        (coupon + (face_value if period == periods else 0))
        / (1 + ytm / frequency) ** period
        for period in range(1, periods + 1)
    )

def calculate_duration(face_value, coupon_rate, ytm, years, frequency):
    periods = years * frequency
    coupon = face_value * coupon_rate / frequency
    price = bond_price(face_value, coupon_rate, ytm, years, frequency)
    duration = 0.0

    for period in range(1, periods + 1):
        time = period / frequency
        # 到期现金流 = 票息 + 面值
        cash_flow = coupon + (face_value if period == periods else 0)
        present_value = cash_flow / (1 + ytm / frequency) ** period
        # 现值占债券价格的比例是久期权重
        duration += (present_value / price) * time
    return price, duration

for ytm in (0.05, 0.08):
    price, duration = calculate_duration(1000, 0.07, ytm, 10, 2)
    print(f"YTM={ytm:.0%}: price={price:.2f}, duration={duration:.4f}")
""",
        "Higher YTM lowers both price and duration in this example.",
    )
    add_topic(
        cells,
        "Question 2: Technology-Stock CAPM Beta",
        "Estimate AAPL beta against a simulated S&P 500 factor and test whether the slope is significant.",
        """
'''
本题估计 CAPM 回归 AAPLret = alpha + beta*MktRet + error。
使用矩阵 OLS，并从残差计算 beta 的 p 值。
'''
import numpy as np
from scipy import stats

rng = np.random.default_rng(17)
n = 252
market_returns = rng.normal(0.0004, 0.011, n)
aapl_returns = 0.0002 + 1.25 * market_returns + rng.normal(0, 0.012, n)

# 常数列用于估计 alpha
X = np.column_stack([np.ones(n), market_returns])
coefficients = np.linalg.lstsq(X, aapl_returns, rcond=None)[0]
residuals = aapl_returns - X @ coefficients

df = n - X.shape[1]
residual_variance = np.sum(residuals**2) / df
covariance = residual_variance * np.linalg.inv(X.T @ X)
beta_standard_error = np.sqrt(covariance[1, 1])

# beta 的 t 检验原假设为 beta=0
t_value = coefficients[1] / beta_standard_error
p_value = 2 * (1 - stats.t.cdf(abs(t_value), df))

fitted = X @ coefficients
r_squared = 1 - np.sum(residuals**2) / np.sum((aapl_returns - aapl_returns.mean())**2)

print("Alpha =", round(float(coefficients[0]), 6))
print("Beta =", round(float(coefficients[1]), 4))
print("R-squared =", round(float(r_squared), 4))
print("Beta p-value =", round(float(p_value), 8))
""",
        "The estimated beta should be near the simulated value of 1.25 and statistically significant.",
    )
    return notebook(cells)


def assignment_3():
    cells = [
        assignment_header(3, "Gamma, SQL Left Join, and Implied Volatility", ["Gamma from Delta", "SQL LEFT JOIN", "Put implied volatility across strikes"])
    ]
    add_topic(
        cells,
        "Question 1: Gamma from Delta",
        "Compare the Black-Scholes closed-form gamma with a central finite-difference approximation.",
        """
'''
本题计算 Delta、解析 Gamma 和数值 Gamma。
中心差分公式 C(S+h)-2C(S)+C(S-h) 除以 h²。
'''
from math import exp, log, pi, sqrt
from scipy import stats

def black_scholes_call(S, K, T, r, sigma):
    d1 = (log(S / K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * stats.norm.cdf(d1) - K * exp(-r * T) * stats.norm.cdf(d2)

def delta_closed_form(S, K, T, r, sigma):
    # 看涨期权 Delta = N(d1)
    d1 = (log(S / K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
    return stats.norm.cdf(d1)

def gamma_closed_form(S, K, T, r, sigma):
    # Gamma = 标准正态密度 n(d1) / (S*sigma*sqrt(T))
    d1 = (log(S / K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
    return stats.norm.pdf(d1) / (S * sigma * sqrt(T))

def gamma_numerical(S, K, T, r, sigma, bump=1e-3):
    c_down = black_scholes_call(S - bump, K, T, r, sigma)
    c_mid = black_scholes_call(S, K, T, r, sigma)
    c_up = black_scholes_call(S + bump, K, T, r, sigma)
    # 二阶中心差分近似期权价格对 S 的二阶导数
    return (c_up - 2 * c_mid + c_down) / bump**2

S, K, T, r, sigma = 40, 40, 0.5, 0.01, 0.2
print("Delta =", round(float(delta_closed_form(S, K, T, r, sigma)), 6))
print("Closed-form Gamma =", round(float(gamma_closed_form(S, K, T, r, sigma)), 6))
print("Numerical Gamma =", round(float(gamma_numerical(S, K, T, r, sigma)), 6))
""",
        "The numerical and analytical gamma values should be very close when the bump is small but not dominated by floating-point error.",
    )
    add_topic(
        cells,
        "Question 2: SQL LEFT JOIN",
        "Retain every employee from the left table, including an employee without a matching department.",
        """
'''
本题在内存数据库中创建两张表，并执行 LEFT JOIN。
LEFT JOIN 保留左表全部记录，未匹配字段返回 NULL。
'''
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT)")
cursor.execute("CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER)")
cursor.executemany("INSERT INTO departments VALUES (?, ?)", [(10, "Engineering"), (20, "Sales"), (30, "Marketing")])
cursor.executemany("INSERT INTO employees VALUES (?, ?, ?)", [(1, "Alice", 10), (2, "Bob", 20), (3, "Charlie", None)])

query = '''
SELECT employees.name, departments.dept_name
FROM employees
LEFT JOIN departments
    ON employees.dept_id = departments.dept_id
ORDER BY employees.id
'''

# execute 后 fetchall 读取查询结果
cursor.execute(query)
rows = cursor.fetchall()
connection.close()

print("name | department")
for name, department in rows:
    print(name, "|", department)
""",
        "Charlie remains in the result with a null department, demonstrating the key difference from an inner join.",
    )
    add_topic(
        cells,
        "Question 3: Put Implied Volatility",
        "Use a grid search to find the volatility that makes the Black-Scholes put price closest to each market midpoint.",
        """
'''
本题对多个行权价逐一反求 put 隐含波动率。
核心是最小化模型价格与市场中间价的绝对误差。
'''
from math import exp, log, sqrt
from scipy import stats

def black_scholes_put(S, K, T, r, sigma):
    d1 = (log(S / K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    # put = K*e^(-rT)*N(-d2) - S*N(-d1)
    return K * exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)

def implied_volatility_put(S, K, T, r, market_price):
    best_sigma = None
    minimum_error = float("inf")

    for step in range(1, 5001):
        # 搜索区间为 0.01% 至 50%
        sigma = 0.0001 * step
        model_price = black_scholes_put(S, K, T, r, sigma)
        error = abs(model_price - market_price)

        # 只有误差更小时才更新当前最优波动率
        if error < minimum_error:
            minimum_error = error
            best_sigma = sigma
    return best_sigma, minimum_error

option_rows = [
    {"Bid": 1.05, "Ask": 1.15, "Strike": 36},
    {"Bid": 2.10, "Ask": 2.30, "Strike": 40},
    {"Bid": 4.75, "Ask": 5.05, "Strike": 44},
]

S, T, r = 40, 0.5, 0.01
for row in option_rows:
    # 市场中间价 = (Bid+Ask)/2
    midpoint = (row["Bid"] + row["Ask"]) / 2
    implied_vol, error = implied_volatility_put(S, row["Strike"], T, r, midpoint)
    print(
        f"K={row['Strike']}, midpoint={midpoint:.2f}, "
        f"implied vol={implied_vol:.2%}, error={error:.6f}"
    )
""",
        "The strike-by-strike estimates form the raw data for a volatility smile.",
    )
    return notebook(cells)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    notebooks = {
        "chapter_4.ipynb": chapter_4(),
        "chapter_5.ipynb": chapter_5(),
        "chapter_6.ipynb": chapter_6(),
        "chapter_7.ipynb": chapter_7(),
        "chapter_8.ipynb": chapter_8(),
        "assignment_1.ipynb": assignment_1(),
        "assignment_2.ipynb": assignment_2(),
        "assignment_3.ipynb": assignment_3(),
    }
    for filename, content in notebooks.items():
        path = OUTPUT_DIR / filename
        path.write_text(json.dumps(content, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
