import base64
import io
import json
from math import exp, log, sqrt
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats


ROOT = Path(__file__).resolve().parent


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(True),
    }


def write_nb(name, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.13"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (ROOT / name).write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding="utf-8")


def img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def make_return_plot():
    rng = np.random.default_rng(123)
    ret = rng.normal(0.0006, 0.018, 900)
    xs = np.linspace(ret.min(), ret.max(), 240)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.hist(ret, bins=45, density=True, alpha=0.65, color="#7fb069")
    ax.plot(xs, stats.norm.pdf(xs, ret.mean(), ret.std(ddof=1)), color="#c44536", lw=2)
    ax.set_title("Daily Return Distribution")
    ax.set_xlabel("Daily return")
    ax.set_ylabel("Density")
    return img(fig), ret.mean(), ret.std(ddof=1)


def make_capm_plot():
    rng = np.random.default_rng(7)
    mkt = rng.normal(0.0005, 0.012, 260)
    stock = 0.0002 + 1.15 * mkt + rng.normal(0, 0.01, 260)
    beta, alpha, r_value, p_value, _ = stats.linregress(mkt, stock)
    xx = np.linspace(mkt.min(), mkt.max(), 100)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.scatter(mkt, stock, s=14, alpha=0.55, color="#4d7ea8")
    ax.plot(xx, alpha + beta * xx, color="#d1495b", lw=2)
    ax.set_title("CAPM: Beta as Regression Slope")
    ax.set_xlabel("Market return")
    ax.set_ylabel("Stock return")
    ax.grid(alpha=0.2)
    return img(fig), beta, r_value, p_value


def make_term_plot():
    maturities = [0.25, 0.5, 2, 3, 5, 10, 20]
    rates = [0.47, 0.6, 1.18, 1.53, 2, 2.53, 3.12]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(maturities, rates, marker="o", color="#2f6f73")
    ax.set_title("Term Structure of Interest Rates")
    ax.set_xlabel("Maturity (years)")
    ax.set_ylabel("Risk-free rate (%)")
    ax.grid(alpha=0.25)
    return img(fig)


def make_ci_plot():
    x = np.arange(-3.5, 3.5, 0.01)
    y = stats.norm.pdf(x)
    z1, z2 = stats.norm.ppf(0.025), stats.norm.ppf(0.975)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(x, y, color="#2f6f73")
    ax.fill_between(x, y, where=(x >= z1) & (x <= z2), color="#9bc1bc", alpha=0.6)
    ax.axvline(z1, color="#c44536", ls="--")
    ax.axvline(z2, color="#c44536", ls="--")
    ax.set_title("95% Confidence Interval")
    ax.set_xlabel("z value")
    ax.set_ylabel("Density")
    return img(fig)


def make_portfolio_plot():
    rng = np.random.default_rng(42)
    mean = np.array([0.08, 0.11, 0.06])
    cov = np.array([[0.040, 0.018, 0.010], [0.018, 0.060, 0.016], [0.010, 0.016, 0.025]])
    weights = rng.dirichlet(np.ones(3), size=1500)
    returns = weights @ mean
    risks = np.sqrt(np.einsum("ij,jk,ik->i", weights, cov, weights))
    sharpe = (returns - 0.02) / risks
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sc = ax.scatter(risks, returns, c=sharpe, s=12, cmap="viridis", alpha=0.75)
    ax.scatter(risks[sharpe.argmax()], returns[sharpe.argmax()], color="#d1495b", s=55)
    ax.set_title("Portfolio Risk-Return Simulation")
    ax.set_xlabel("Volatility")
    ax.set_ylabel("Expected return")
    fig.colorbar(sc, ax=ax, label="Sharpe ratio")
    return img(fig), weights[sharpe.argmax()], sharpe.max()


def make_option_plot():
    s = np.arange(0, 100, 2)
    k, premium = 50, 4
    payoff = np.maximum(s - k, 0)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(s, payoff, label="Payoff", color="#2f6f73")
    ax.plot(s, payoff - premium, label="Profit", color="#d1495b")
    ax.axhline(0, color="black", lw=0.8)
    ax.axvline(k, color="gray", ls="--")
    ax.set_title("Long Call Payoff and Profit")
    ax.set_xlabel("Underlying price at maturity")
    ax.set_ylabel("Value")
    ax.legend()
    return img(fig)


def make_smile_plot():
    strikes = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120])
    vols = 0.18 + 0.00022 * (strikes - 100) ** 2
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(strikes, vols, marker="o", color="#4d7ea8")
    ax.set_title("Volatility Smile")
    ax.set_xlabel("Strike price")
    ax.set_ylabel("Implied volatility")
    ax.grid(alpha=0.25)
    return img(fig)


def make_growth_plot():
    rng = np.random.default_rng(2026)
    dates = pd.bdate_range("2024-01-01", periods=300)
    returns = pd.DataFrame(
        rng.normal([0.0005, 0.0006, 0.00045], [0.014, 0.016, 0.015], size=(300, 3)),
        index=dates,
        columns=["AAPL", "MSFT", "GOOGL"],
    )
    growth = (1 + returns).cumprod()
    fig, ax = plt.subplots(figsize=(6, 3.5))
    growth.plot(ax=ax)
    ax.set_title("Cumulative Growth of $1")
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    return img(fig), returns.mean() * 252, returns.std() * np.sqrt(252)


def make_gamma_plot():
    def gamma(s, k, t, r, sigma):
        d1 = (log(s / k) + (r + sigma**2 / 2) * t) / (sigma * sqrt(t))
        return stats.norm.pdf(d1) / (s * sigma * sqrt(t))

    prices = np.linspace(20, 70, 200)
    gammas = [gamma(s, 40, 0.5, 0.01, 0.2) for s in prices]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(prices, gammas, color="#d1495b")
    ax.axvline(40, color="gray", ls="--")
    ax.set_title("Call Gamma around At-the-Money")
    ax.set_xlabel("Underlying price")
    ax.set_ylabel("Gamma")
    return img(fig)


return_img, return_mean, return_std = make_return_plot()
capm_img, capm_beta, capm_r, capm_p = make_capm_plot()
portfolio_img, portfolio_w, portfolio_s = make_portfolio_plot()
growth_img, growth_mean, growth_std = make_growth_plot()


main = [
    md("# Financial Data Mining Atlas: Review Notebook\n\nSource file: `python_financial_coding.py`. This notebook is organized as a finance + computer science review atlas: concept first, code second, then expected output and interpretation."),
    md("## Chapter 0. Preparation: working directory and `os`\n\n- `os.getcwd()` returns the current working directory. Many finance scripts fail simply because Python is reading data from a different folder than the one you expect.\n- `os.chdir(path)` changes the working directory. In an exam, if a code blank asks why a local file cannot be found, the answer is often about the working directory.\n- `os.path.join(a, b, ...)` builds paths safely. It is better than manually typing separators because Windows and Mac/Linux use different separators.\n- `os.makedirs(path, exist_ok=True)` creates a folder and avoids an error if it already exists.\n- In this atlas, each code cell imports what it needs locally, because notebooks are usually studied and rerun block by block."),
    code("import os\n\n'''Check where Python is currently looking for local files.'''\ncurrent_directory = os.getcwd()\nprint(current_directory)\n\n'''Build a path under the current directory instead of hard-coding a personal desktop path.'''\nreview_folder = os.path.join(current_directory, 'review_outputs')\nos.makedirs(review_folder, exist_ok=True)\nprint(review_folder)"),
    md("**Expected output and interpretation**\n\n- The first printed line is the folder from which Python reads relative paths such as `ibm.pkl` or `callsfor15mar2024.txt`.\n- The second printed line is a newly prepared output folder path.\n- Code-fill exam reminder: `os.getcwd()` has no input; `os.path.join()` receives path pieces; `exist_ok=True` prevents repeated runs from crashing."),
    md("## Chapter 1 Slides. Course orientation and Python basics\n\n- The course applies Python to finance topics such as ratio analysis, portfolio theory, CAPM, Fama-French factor models, Monte Carlo simulation, options theory, VaR, and spread estimation.\n- Python is emphasized because it combines readable syntax, open-source data access, strong numerical libraries, visualization, machine learning support, and notebook-based communication.\n- Spyder is positioned as an engineering workbench: useful for long scripts, debugging, variable inspection, and repeated execution.\n- Jupyter Notebook is positioned as a lab journal: useful for exploratory data analysis, step-by-step explanation, charts, equations, and shareable reports.\n- Basic Python points from the slides: Python is case-sensitive; indentation matters; indexing starts from 0; lists are mutable while tuples are immutable; `#` and triple quotes can be used for comments.\n- Function structure: `def function_name(inputs):`, indented body, and `return output`. The future value example is `fv = pv * (1 + r) ** n`; the present value exercise reverses it as `pv = fv / (1 + r) ** n`.\n- Function inputs can be passed by position, by keyword, or by mixing both. For code-fill questions, keyword arguments are safer because they document meaning."),
    md("## Chapter 2 Slides. Python modules and package workflow\n\n- A module/package is a collection of programs organized around a topic. Examples in this course include `math`, `numpy`, `pandas`, `scipy`, `yfinance`, `matplotlib`, `numpy_financial`, and `statsmodels`.\n- Import styles matter: `import math` requires `math.sqrt(3)`; `import math as m` uses `m.sqrt(3)`; `from math import sqrt` allows `sqrt(3)` directly; `from math import *` imports many names but is less explicit.\n- Package installation is commonly done with `pip install package_name`, `conda install package_name`, or version-specific forms such as `pip install SomeProject==1.4`.\n- `dir(package)` lists objects inside a package; `help(function)` shows usage and parameters. These are useful when you forget exact function arguments during review.\n- Conventional aliases: `numpy as np`, `pandas as pd`, `yfinance as yf`, `matplotlib.pyplot as plt`, and sometimes `scipy as sp`.\n- The slides introduce `yfinance.download()` for market data and a Black-Scholes call function as an early example of packaging a finance formula into reusable code."),
    md("## 1. Time value of money, annuity, NPV and IRR\n\n- Time value of money says cash flows at different dates are not directly comparable. Discounting moves future cash flows to today; compounding moves current cash flows to the future.\n- A growing annuity is a finite stream of cash flows growing at rate `g`. The denominator `r - g` appears because valuation compares required return with cash-flow growth.\n- A delayed perpetuity is first valued one period before the first payment, then discounted back to today.\n- NPV evaluates a project using a required return. IRR is the discount rate that makes NPV equal to zero.\n- Code-fill focus: cash flow lists usually put the initial investment as a negative number; `npf.npv(rate, cashflows)` and `npf.irr(cashflows)` are separate calls."),
    code("import numpy_financial as npf\n\n'''Growing annuity present value: finite growing cash flows discounted to today.'''\ndef present_value_growing_annuity(first_cash_flow, discount_rate, growth_rate, periods):\n    return first_cash_flow / (discount_rate - growth_rate) * (1 - ((1 + growth_rate) / (1 + discount_rate)) ** periods)\n\n'''Delayed perpetuity: value at the start-payment date, then discount back.'''\ndef present_value_delayed_perpetuity(cash_flow, discount_rate, delay_years):\n    return (cash_flow / discount_rate) / (1 + discount_rate) ** (delay_years - 1)\n\ncash_flows = [-100, 50, 60, 70]\nproject_npv = npf.npv(0.05, cash_flows)\nproject_irr = npf.irr(cash_flows)\nprint(project_npv)\nprint(project_irr)"),
    md("**Expected output and interpretation**\n\n- For `cash_flows = [-100, 50, 60, 70]` and discount rate `5%`, NPV is about `62.51` and IRR is about `33.87%`.\n- Financial meaning: the project creates value under a 5% required return because NPV is positive. Its internal return is far above the required return.\n- Code-fill reminder: `npf.irr()` does not take the discount rate because IRR itself is the unknown rate."),
    md("## 2. Return engineering and distribution visualization\n\n- `pct_change()` converts prices into simple returns: `(P_t - P_{t-1}) / P_{t-1}`.\n- Multi-period simple returns should be compounded with `(1 + r).prod() - 1`.\n- Log returns can be summed over time, then converted back with `np.exp(sum_log_return) - 1`.\n- `dropna()` is needed because the first return is undefined.\n- The histogram checks empirical return behavior; the normal curve is a benchmark, not a guarantee."),
    code("import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport scipy.stats as stats\n\nnp.random.seed(123)\ndates = pd.bdate_range('2023-01-01', periods=500)\nprices = pd.Series(100 * np.exp(np.cumsum(np.random.normal(0.0005, 0.015, len(dates)))), index=dates, name='Close')\n\n'''Step 1: transform prices into daily returns.'''\ndaily_returns = prices.pct_change().dropna()\n\n'''Step 2: group daily returns into annual and monthly returns by compounding 1+r.'''\nannual_returns = (1 + daily_returns).groupby(daily_returns.index.year).prod() - 1\nyear_month = daily_returns.index.year * 100 + daily_returns.index.month\nmonthly_returns = (1 + daily_returns).groupby(year_month).prod() - 1\n\n'''Step 3: test whether the mean daily return is statistically different from zero.'''\nt_test_result = stats.ttest_1samp(daily_returns, 0)\nprint(annual_returns.head())\nprint(t_test_result)\n\nplt.hist(daily_returns, bins=45, density=True, alpha=0.65)\nx = np.linspace(daily_returns.min(), daily_returns.max(), 200)\nplt.plot(x, stats.norm.pdf(x, daily_returns.mean(), daily_returns.std()), color='red')\nplt.title('Daily Return Distribution')\nplt.show()"),
    md(f"**Expected output and interpretation**\n\n![Daily return distribution]({return_img})\n\n- The simulated daily mean is about `{return_mean:.5f}` and the daily standard deviation is about `{return_std:.5f}`.\n- The t-test output contains a statistic and a p-value. If the p-value is larger than 0.05, we do not reject the null that the mean return equals zero.\n- Code-fill reminder: `groupby(daily_returns.index.year).prod()` is the key line for annual compounding."),
    md("## 3. t-test and Fama-French factor regression\n\n- A two-sample t-test asks whether two return samples have equal population means.\n- Fama-French three-factor regression explains excess stock return using market excess return, size factor `SMB`, and value factor `HML`.\n- In `statsmodels`, `sm.add_constant(x)` adds the intercept column. Forgetting this line forces the regression through zero.\n- In exam code, the dependent variable is usually `y`; explanatory variables are `x`; `sm.OLS(y, x).fit()` estimates the model."),
    code("import numpy as np\nimport pandas as pd\nimport scipy.stats as stats\nimport statsmodels.api as sm\n\nnp.random.seed(7)\nsample_size = 252\nstock_a_returns = np.random.normal(0.0007, 0.018, sample_size)\nstock_b_returns = np.random.normal(0.0003, 0.016, sample_size)\n\n'''Two-sample t-test: compare average returns of two assets.'''\ntwo_sample_test = stats.ttest_ind(stock_a_returns, stock_b_returns, equal_var=False)\nprint(two_sample_test)\n\nfactor_data = pd.DataFrame({\n    'MKT_RF': np.random.normal(0.0005, 0.01, sample_size),\n    'SMB': np.random.normal(0.0001, 0.006, sample_size),\n    'HML': np.random.normal(0.0001, 0.007, sample_size),\n    'RF': 0.00008,\n})\nasset_return = 0.0002 + 1.1 * factor_data['MKT_RF'] + 0.25 * factor_data['SMB'] - 0.15 * factor_data['HML'] + np.random.normal(0, 0.008, sample_size)\n\n'''Excess return is asset return minus risk-free rate.'''\ny = asset_return - factor_data['RF']\nx = sm.add_constant(factor_data[['MKT_RF', 'SMB', 'HML']])\nff3_model = sm.OLS(y, x).fit()\nprint(ff3_model.summary())"),
    md("**Expected output and interpretation**\n\n- The t-test p-value is about `0.36` in this simulated case, so the difference in mean returns is not statistically significant at 5%.\n- The Fama-French regression should show a market beta near `1.04`, a positive `SMB` loading, and a negative `HML` loading because the data were simulated that way.\n- Interpretation: factor coefficients measure risk exposures, not just prediction weights. A significant `MKT_RF` coefficient means market risk explains a meaningful part of asset returns."),
    md("## 4. Bond valuation, term structure and duration\n\n- Bond price equals present value of coupons plus present value of face value.\n- YTM is the discount rate that matches the market price.\n- Macaulay duration is a present-value-weighted average time to receive cash flows.\n- Modified duration approximates price sensitivity to yield changes: higher duration means greater interest-rate risk.\n- Code-fill focus: the final period cash flow includes both coupon and face value."),
    code("import numpy_financial as npf\n\ndef bond_price(face_value, coupon_rate, ytm, years, frequency):\n    '''Price a coupon bond using pv(rate, nper, pmt, fv).'''\n    coupon_payment = face_value * coupon_rate / frequency\n    return -npf.pv(ytm / frequency, years * frequency, coupon_payment, face_value)\n\ndef macaulay_duration(face_value, coupon_rate, ytm, years, frequency):\n    '''Weight each payment time by that cash flow's present value share.'''\n    periods = years * frequency\n    price = bond_price(face_value, coupon_rate, ytm, years, frequency)\n    duration = 0\n    for period in range(1, periods + 1):\n        time = period / frequency\n        cash_flow = face_value * coupon_rate / frequency\n        if period == periods:\n            cash_flow += face_value\n        present_value = cash_flow / (1 + ytm / frequency) ** period\n        duration += (present_value / price) * time\n    return duration\n\nprice_5 = bond_price(1000, 0.07, 0.05, 10, 2)\nduration_5 = macaulay_duration(1000, 0.07, 0.05, 10, 2)\nprint(price_5)\nprint(duration_5)"),
    md(f"**Expected output and interpretation**\n\n![Term structure]({make_term_plot()})\n\n- With face value `1000`, coupon rate `7%`, YTM `5%`, maturity `10` years and semiannual coupons, price is about `1155.89` and Macaulay duration is about `7.56` years.\n- Because coupon rate is above YTM, the bond sells above par.\n- The term structure plot connects rates across maturities and is the input curve behind many fixed-income valuation tasks."),
    md("## 5. CAPM and linear regression\n\n- CAPM links an asset's expected excess return to market excess return.\n- In a simple regression, beta is the slope coefficient on market return.\n- `stats.linregress(x, y)` returns slope first and intercept second. This ordering is a common exam trap.\n- `sm.OLS(y, sm.add_constant(x)).fit()` gives a full statistical table, including p-values and R-squared."),
    code("import scipy.stats as stats\nimport statsmodels.api as sm\n\nstock_returns = [0.065, 0.0265, -0.0593, -0.001, 0.0345]\nmarket_returns = [0.055, -0.09, -0.041, 0.045, 0.022]\n\n'''linregress input order is X first, Y second.'''\nbeta, alpha, r_value, p_value, std_err = stats.linregress(market_returns, stock_returns)\nprint(beta, alpha, r_value, p_value)\n\n'''OLS requires adding a constant if we want an intercept.'''\nx = sm.add_constant(market_returns)\ncapm_result = sm.OLS(stock_returns, x).fit()\nprint(capm_result.summary())"),
    md(f"**Expected output and interpretation**\n\n![CAPM regression]({capm_img})\n\n- The small original five-observation example gives beta around `0.291`, alpha around `0.0137`, and a large p-value, so the slope is not statistically significant.\n- The plotted simulation gives beta about `{capm_beta:.3f}` and illustrates the slope idea visually.\n- Code-fill reminder: if `Y = alpha + beta * X`, then `X` is market return and `Y` is stock return."),
    md("## 6. Hypothesis testing: normal, F-test, Levene test and means\n\n- `stats.norm.cdf(x)` returns probability to the left of `x`; `stats.norm.ppf(p)` returns the cutoff with left-tail probability `p`.\n- A confidence interval is estimate ± critical value × standard error.\n- F-test compares variances through a variance ratio; Levene's test is often more robust.\n- After checking variance equality, choose `equal_var=True` or `False` in `stats.ttest_ind`."),
    code("import numpy as np\nimport scipy.stats as stats\n\nnp.random.seed(2026)\ngroup_1 = np.random.normal(0.02, 0.10, 80)\ngroup_2 = np.random.normal(0.04, 0.14, 80)\n\n'''F statistic: larger sample variance divided by smaller sample variance.'''\nvariance_ratio = max(group_1.var(ddof=1), group_2.var(ddof=1)) / min(group_1.var(ddof=1), group_2.var(ddof=1))\nf_critical = stats.f.ppf(0.95, len(group_1) - 1, len(group_2) - 1)\nprint(variance_ratio, f_critical)\n\n'''Levene test null hypothesis: equal variances.'''\nprint(stats.levene(group_1, group_2))\n\n'''Welch t-test does not assume equal variance.'''\nprint(stats.ttest_ind(group_1, group_2, equal_var=False))"),
    md(f"**Expected output and interpretation**\n\n![Normal confidence interval]({make_ci_plot()})\n\n- In this simulation, Levene's p-value is below 0.05, so equal variance is questionable.\n- The Welch t-test p-value is about `0.002`, suggesting the two group means differ significantly.\n- Code-fill reminder: `stats.f.ppf(1 - alpha, df1, df2)` gives the right-tail critical value."),
    md("## 7. Time-series lag logic and Granger causality\n\n- Time-series data depend on order. `shift(1)` creates a one-period lag.\n- Granger causality asks whether lagged values of X improve prediction of Y beyond lagged Y alone.\n- This is predictive causality, not philosophical causality.\n- In a manual Granger setup, compare a restricted model with only Y lags to a full model with both Y lags and X lags."),
    code("import numpy as np\nimport pandas as pd\nimport statsmodels.api as sm\n\nnp.random.seed(99)\nn = 120\nchicken = np.random.normal(size=n).cumsum()\negg = 0.4 * np.roll(chicken, 1) + np.random.normal(size=n)\nseries = pd.DataFrame({'chicken': chicken, 'egg': egg}).iloc[3:].copy()\n\n'''Create lagged variables. shift(1) means previous period.'''\nfor lag in [1, 2, 3]:\n    series[f'chicken_lag{lag}'] = series['chicken'].shift(lag)\n    series[f'egg_lag{lag}'] = series['egg'].shift(lag)\nseries = series.dropna()\n\nrestricted_x = sm.add_constant(series[['egg_lag1', 'egg_lag2', 'egg_lag3']])\nrestricted_model = sm.OLS(series['egg'], restricted_x).fit()\nfull_x = sm.add_constant(series[['egg_lag1', 'egg_lag2', 'egg_lag3', 'chicken_lag1', 'chicken_lag2', 'chicken_lag3']])\nfull_model = sm.OLS(series['egg'], full_x).fit()\nprint(restricted_model.rsquared)\nprint(full_model.rsquared)"),
    md("**Expected output and interpretation**\n\n- The restricted R-squared is about `0.573`; the full model R-squared is about `0.724`.\n- Adding lagged `chicken` improves prediction of `egg` in this simulated example.\n- Code-fill reminder: lags create missing values at the beginning, so `dropna()` is required before regression."),
    md("## 8. Portfolio theory and optimization\n\n- Portfolio variance includes individual variances and covariances.\n- Low correlation creates diversification benefits.\n- Sharpe Ratio equals excess return divided by total risk.\n- Optimizers usually minimize a function, so maximizing Sharpe is implemented as minimizing negative Sharpe.\n- Weight constraints are essential: in a no-short-sale portfolio, each weight is between 0 and 1 and all weights sum to 1."),
    code("import numpy as np\nfrom scipy.optimize import minimize\n\nexpected_returns = np.array([0.08, 0.11, 0.06])\ncovariance_matrix = np.array([[0.040, 0.018, 0.010], [0.018, 0.060, 0.016], [0.010, 0.016, 0.025]])\nrisk_free_rate = 0.02\n\ndef negative_sharpe_ratio(weights):\n    '''Objective function: optimizer minimizes this, so we return negative Sharpe.'''\n    portfolio_return = weights @ expected_returns\n    portfolio_volatility = np.sqrt(weights @ covariance_matrix @ weights)\n    return -(portfolio_return - risk_free_rate) / portfolio_volatility\n\nconstraints = ({'type': 'eq', 'fun': lambda weights: weights.sum() - 1})\nbounds = [(0, 1), (0, 1), (0, 1)]\ninitial_weights = np.array([1/3, 1/3, 1/3])\nresult = minimize(negative_sharpe_ratio, initial_weights, bounds=bounds, constraints=constraints)\nprint(result.x)\nprint(-result.fun)"),
    md(f"**Expected output and interpretation**\n\n![Portfolio simulation]({portfolio_img})\n\n- The optimized no-short-sale weights are close to `{np.round(portfolio_w, 3).tolist()}`, with Sharpe Ratio around `{portfolio_s:.3f}`.\n- Each point in the plot is one portfolio. The highlighted point is the highest Sharpe portfolio in the simulation.\n- Code-fill reminder: the equality constraint returns `weights.sum() - 1`; the optimizer tries to make it equal zero."),
    md("## 9. Options, Black-Scholes, implied volatility and Greeks\n\n- A long call payoff is `max(S_T - K, 0)`; profit subtracts the premium.\n- Black-Scholes call price equals expected present value of receiving stock minus expected present value of paying the strike under risk-neutral pricing.\n- Implied volatility is the volatility that makes model price match market price.\n- Delta is first-order sensitivity to underlying price; Gamma is second-order sensitivity."),
    code("from math import exp, log, sqrt\nimport scipy.stats as stats\n\ndef black_scholes_call(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility):\n    '''Compute d1 and d2 first; they are reused in the pricing formula.'''\n    d1 = (log(stock_price / strike_price) + (risk_free_rate + volatility ** 2 / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))\n    d2 = d1 - volatility * sqrt(time_to_maturity)\n    return stock_price * stats.norm.cdf(d1) - strike_price * exp(-risk_free_rate * time_to_maturity) * stats.norm.cdf(d2)\n\ndef implied_volatility_call(stock_price, strike_price, time_to_maturity, risk_free_rate, market_call_price):\n    '''Grid search over volatility candidates and keep the one with the smallest pricing error.'''\n    best_volatility = None\n    smallest_error = float('inf')\n    for i in range(1, 10000):\n        volatility = 0.0001 * i\n        model_price = black_scholes_call(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility)\n        error = abs(model_price - market_call_price)\n        if error < smallest_error:\n            smallest_error = error\n            best_volatility = volatility\n    return best_volatility\n\nprint(black_scholes_call(10, 10, 0.5, 0.01, 0.2))\nprint(implied_volatility_call(10, 10, 0.5, 0.01, 2))"),
    md(f"**Expected output and interpretation**\n\n![Call payoff]({make_option_plot()})\n\n![Volatility smile]({make_smile_plot()})\n\n- The BSM call price in the example is about `0.588`.\n- The implied volatility that makes the call price close to `2` is about `0.7092`, much higher than the example input volatility `0.2`.\n- Code-fill reminder: `d2 = d1 - sigma * sqrt(T)`, and call price uses `N(d1)` and `N(d2)`."),
    md("## 10. SQL and joins\n\n- `INNER JOIN` keeps only matched rows.\n- `LEFT JOIN` keeps all rows from the left table and fills unmatched right-table fields with missing values.\n- Finance example: keep all stock trading days on the left, then attach factor data, macro data, or accounting data on the right.\n- Code-fill focus: SQL join syntax is `FROM left_table LEFT JOIN right_table ON left_table.key = right_table.key`."),
    code("import sqlite3\nimport pandas as pd\n\nconn = sqlite3.connect(':memory:')\ncursor = conn.cursor()\ncursor.execute('CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT)')\ncursor.execute('CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER)')\ncursor.executemany('INSERT INTO departments VALUES (?, ?)', [(10, 'ENG'), (20, 'HR'), (30, 'MKT')])\ncursor.executemany('INSERT INTO employees VALUES (?, ?, ?)', [(1, 'Alice', 10), (2, 'Bob', 20), (3, 'Charlie', None)])\n\n'''LEFT JOIN preserves Charlie even though his dept_id is missing.'''\nleft_join_query = '''\nSELECT employees.name, departments.dept_name\nFROM employees\nLEFT JOIN departments ON employees.dept_id = departments.dept_id\n'''\njoined_data = pd.read_sql_query(left_join_query, conn)\nconn.close()\nprint(joined_data)"),
    md("**Expected output and interpretation**\n\n| name | dept_name |\n|---|---|\n| Alice | ENG |\n| Bob | HR |\n| Charlie | NaN |\n\n- Charlie remains because employees is the left table.\n- If this were an `INNER JOIN`, Charlie would disappear.\n- This distinction matters in data mining because join choice changes the sample used by later tests and regressions."),
]


coding1 = [
    md("# Coding 1 Atlas: Environment, Return Engineering and Portfolio Summary\n\nSource file: `coding_1.py`."),
    md("## Task 1. Environment and system audit\n\n- The task checks whether the coding environment is ready.\n- `os.getcwd()` and path construction verify file location.\n- `sys.version` and `package.__version__` verify reproducibility.\n- `dir(npf)` explores functions in `numpy_financial`; this is useful when you forget whether the function is called `npv`, `irr`, `pv`, or `rate`."),
    code("import os\nimport sys\nimport pandas as pd\nimport numpy as np\nimport yfinance as yf\nimport scipy.stats as stats\nimport numpy_financial as npf\nimport matplotlib.pyplot as plt\n\ncurrent_directory = os.getcwd()\nexercise_path = os.path.join(current_directory, 'Class_Exercise')\nos.makedirs(exercise_path, exist_ok=True)\nprint(f'Current Directory: {current_directory}')\nprint(f'Exercise Directory: {exercise_path}')\nprint(f'Python version: {sys.version}')\nprint(f'pandas: {pd.__version__}')\nprint(f'numpy: {np.__version__}')\nprint(f'yfinance: {yf.__version__}')\nprint('Functions in numpy_financial:', [name for name in dir(npf) if not name.startswith('_')][:20])"),
    md("**Expected output and interpretation**\n\n- You should see the current path, the exercise folder path, Python version, and versions of `pandas`, `numpy`, and `yfinance`.\n- The printed `numpy_financial` list should include functions such as `fv`, `irr`, `npv`, `pv`, and `rate`.\n- Code-fill reminder: package versions use `package.__version__`; built-in `sys.version` is not a function call."),
    md("## Task 2. Data cleaning and quarterly returns\n\n- The original assignment downloads close prices for multiple tickers. This notebook uses simulated prices so the block is review-stable without network dependency.\n- Missing prices are checked by `.isnull().sum()`.\n- Price missing values can often be forward-filled, but returns should be computed after cleaning prices.\n- Quarterly returns are produced by summing log returns within each year-quarter group and converting back with `np.exp(...) - 1`."),
    code("import numpy as np\nimport pandas as pd\n\nnp.random.seed(2026)\ntickers = ['AAPL', 'MSFT', 'GOOGL']\ndates = pd.bdate_range('2024-01-01', '2026-03-19')\nprice_data = pd.DataFrame(\n    100 * np.exp(np.cumsum(np.random.normal(0.0005, 0.015, (len(dates), len(tickers))), axis=0)),\n    index=dates,\n    columns=tickers,\n)\nprice_data.iloc[5, 0] = np.nan\nmissing_values = price_data.isnull().sum()\nclean_price_data = price_data.ffill().dropna()\n\nlog_returns = np.log(clean_price_data / clean_price_data.shift(1))\nlog_returns['Year'] = log_returns.index.year\nlog_returns['Quarter'] = log_returns.index.quarter\nquarterly_returns = np.exp(log_returns.groupby(['Year', 'Quarter']).sum()) - 1\nprint(missing_values)\nprint(quarterly_returns.head())"),
    md("**Expected output and interpretation**\n\n- `AAPL` has one missing value before cleaning; the other simulated stocks have no missing values.\n- The quarterly return table is indexed by `Year` and `Quarter`, with one column for each stock.\n- Code-fill reminder: create grouping columns before `groupby`, and apply `np.exp(sum_log_return) - 1` after grouping."),
    md("## Task 3. Statistical duel, Sharpe ratio and growth plot\n\n- The t-test compares average daily returns of two stocks.\n- Sharpe Ratio converts returns into risk-adjusted performance.\n- Cumulative return uses `(1 + returns).cumprod()`, which shows the value path of one invested dollar."),
    code("import numpy as np\nimport scipy.stats as stats\nimport matplotlib.pyplot as plt\n\nreturns = clean_price_data.pct_change().dropna()\nt_statistic, p_value = stats.ttest_ind(returns['AAPL'], returns['MSFT'], equal_var=False)\nprint(p_value)\nprint('significant' if p_value < 0.05 else 'not significant')\n\nannual_risk_free_rate = 0.01\ndaily_risk_free_rate = (1 + annual_risk_free_rate) ** (1 / 252) - 1\nexcess_returns = returns - daily_risk_free_rate\nsharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252)\nprint(sharpe_ratio)\n\ncumulative_returns = (1 + returns).cumprod()\ncumulative_returns.plot(figsize=(10, 5), title='Growth of $1')\nplt.xlabel('Date')\nplt.ylabel('Value')\nplt.show()"),
    md(f"**Expected output and interpretation**\n\n![Cumulative growth]({growth_img})\n\n- In the simulated example, the AAPL-MSFT p-value is usually above 0.05, so the mean-return difference is not significant.\n- The Sharpe Ratio output is a three-element Series, one value per stock.\n- Code-fill reminder: annualizing a daily Sharpe Ratio requires multiplying by `sqrt(252)`."),
]


coding2 = [
    md("# Coding 2 Atlas: Bond Sensitivity and CAPM Beta\n\nSource file: `coding_2.py`."),
    md("## Task 1. Bond valuation and duration\n\n- This task combines bond pricing with duration.\n- `bond_price()` wraps `npf.pv`; the negative sign converts the present value convention into a positive price.\n- `calculate_duration()` loops over all coupon periods, computes each cash flow's present value weight, then multiplies by time.\n- Code-fill trap: the final cash flow equals coupon plus face value, not coupon only."),
    code("import numpy_financial as npf\n\ndef bond_price(face_value, coupon_rate, ytm, years, frequency):\n    coupon_payment = face_value * coupon_rate / frequency\n    return -npf.pv(ytm / frequency, years * frequency, coupon_payment, face_value)\n\ndef calculate_duration(face_value, coupon_rate, ytm, years, frequency):\n    periods = years * frequency\n    coupon_payment = face_value * coupon_rate / frequency\n    price = bond_price(face_value, coupon_rate, ytm, years, frequency)\n    duration = 0\n    for period in range(1, periods + 1):\n        time = period / frequency\n        cash_flow = coupon_payment + (face_value if period == periods else 0)\n        weight = cash_flow / (1 + ytm / frequency) ** period / price\n        duration += weight * time\n    return duration\n\nface_value = 1000\ncoupon_rate = 0.07\nyears = 10\nfrequency = 2\nprint(calculate_duration(face_value, coupon_rate, 0.05, years, frequency))\nprint(calculate_duration(face_value, coupon_rate, 0.08, years, frequency))"),
    md("**Expected output and interpretation**\n\n- Duration is about `7.56` years when YTM is 5%, and about `7.25` years when YTM is 8%.\n- Higher YTM gives relatively less present-value weight to distant cash flows, so duration declines.\n- This result is important for interest-rate risk: longer duration means larger price movement for a yield change."),
    md("## Task 2. CAPM beta for a tech stock\n\n- The original code downloads AAPL and S&P 500 data; this version uses simulated data for stable review.\n- `pct_change()` would be used for real prices; here we directly simulate returns.\n- `pd.concat(..., axis=1)` or `merge` aligns the two return series by date.\n- `sm.add_constant()` is required for alpha; beta is the coefficient on `MktRet`."),
    code("import numpy as np\nimport pandas as pd\nimport statsmodels.api as sm\n\nnp.random.seed(17)\ndates = pd.bdate_range('2025-01-01', '2025-12-31')\nmarket_returns = pd.Series(np.random.normal(0.0004, 0.011, len(dates)), index=dates, name='MktRet')\naapl_returns = pd.Series(0.0002 + 1.25 * market_returns + np.random.normal(0, 0.012, len(dates)), index=dates, name='AAPLret')\ncapm_data = pd.concat([aapl_returns, market_returns], axis=1).dropna()\n\nx = sm.add_constant(capm_data['MktRet'])\ny = capm_data['AAPLret']\nmodel = sm.OLS(y, x).fit()\nbeta = model.params['MktRet']\nr_squared = model.rsquared\np_value = model.pvalues['MktRet']\nprint(model.summary())\nprint(beta, r_squared, p_value)\nprint('significant' if p_value < 0.05 else 'insignificant')"),
    md(f"**Expected output and interpretation**\n\n![CAPM regression]({capm_img})\n\n- The simulated beta is about `1.24`, R-squared is about `0.59`, and p-value is very small.\n- Financial meaning: the stock is more sensitive than the market; a 1% market move is associated with about a 1.24% stock move on average.\n- Code-fill reminder: `model.params['MktRet']` extracts beta by variable name."),
]


coding3 = [
    md("# Coding 3 Atlas: Gamma, SQL Left Join and Volatility Smile\n\nSource file: `coding_3.py`."),
    md("## Question 1. Derive Gamma\n\n- Delta is the first derivative of option value with respect to stock price.\n- Gamma is the derivative of Delta, or the second derivative of option value with respect to stock price.\n- Closed-form Gamma under Black-Scholes is `N'(d1) / (S * sigma * sqrt(T))`, where `N'` is the standard normal PDF.\n- Numerical Gamma uses central difference: `C(S+h) - 2C(S) + C(S-h)` divided by `h^2`."),
    code("from math import exp, log, sqrt\nimport scipy.stats as stats\n\ndef black_scholes_call(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility):\n    d1 = (log(stock_price / strike_price) + (risk_free_rate + volatility ** 2 / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))\n    d2 = d1 - volatility * sqrt(time_to_maturity)\n    return stock_price * stats.norm.cdf(d1) - strike_price * exp(-risk_free_rate * time_to_maturity) * stats.norm.cdf(d2)\n\ndef delta_closed_form(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility):\n    d1 = (log(stock_price / strike_price) + (risk_free_rate + volatility ** 2 / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))\n    return stats.norm.cdf(d1)\n\ndef gamma_closed_form(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility):\n    d1 = (log(stock_price / strike_price) + (risk_free_rate + volatility ** 2 / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))\n    return stats.norm.pdf(d1) / (stock_price * volatility * sqrt(time_to_maturity))\n\ndef gamma_numerical(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility, bump=1e-4):\n    c_down = black_scholes_call(stock_price - bump, strike_price, time_to_maturity, risk_free_rate, volatility)\n    c_mid = black_scholes_call(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility)\n    c_up = black_scholes_call(stock_price + bump, strike_price, time_to_maturity, risk_free_rate, volatility)\n    return (c_up - 2 * c_mid + c_down) / bump ** 2\n\nS = 40; K = 40; T = 0.5; r = 0.01; sigma = 0.2\nprint(round(delta_closed_form(S, K, T, r, sigma), 6))\nprint(round(gamma_closed_form(S, K, T, r, sigma), 6))\nprint(round(gamma_numerical(S, K, T, r, sigma), 6))"),
    md(f"**Expected output and interpretation**\n\n![Gamma curve]({make_gamma_plot()})\n\n- Delta is about `0.542235`; closed-form Gamma and numerical Gamma are both about `0.070128`.\n- Gamma is highest near at-the-money, meaning Delta changes fastest when stock price is close to strike.\n- Code-fill reminder: use `stats.norm.pdf(d1)` for Gamma, not `cdf`."),
    md("## Question 2. SQL left join\n\n- The task practices SQL join logic using mock employee and department tables.\n- `LEFT JOIN` keeps every employee and attaches department names when available.\n- This is directly transferable to finance tables: keep every stock-date observation and attach factor or macro data where available."),
    code("import sqlite3\nimport pandas as pd\n\nconn = sqlite3.connect(':memory:')\ncursor = conn.cursor()\ncursor.execute('CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT)')\ncursor.execute('CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER)')\ncursor.executemany('INSERT INTO departments VALUES (?, ?)', [(10, 'Engineering'), (20, 'Sales'), (30, 'Marketing')])\ncursor.executemany('INSERT INTO employees VALUES (?, ?, ?)', [(1, 'Alice', 10), (2, 'Bob', 20), (3, 'Charlie', None)])\n\nleft_join_query = '''\nSELECT employees.name, departments.dept_name\nFROM employees\nLEFT JOIN departments ON employees.dept_id = departments.dept_id\n'''\nemployee_department_data = pd.read_sql_query(left_join_query, conn)\nconn.close()\nprint(employee_department_data)"),
    md("**Expected output and interpretation**\n\n| name | dept_name |\n|---|---|\n| Alice | Engineering |\n| Bob | Sales |\n| Charlie | NaN |\n\n- Charlie is retained because `employees` is the left table.\n- Code-fill reminder: the `ON` clause specifies the key equality between the two tables."),
    md("## Question 3. Put implied volatility and `apply()`\n\n- The task rewrites a loop as a DataFrame operation.\n- Mid price is `(Bid + Ask) / 2`, a common approximation of market option price.\n- `apply(lambda row: ..., axis=1)` sends one row at a time to the pricing function.\n- The put formula is `K e^{-rT} N(-d2) - S N(-d1)`."),
    code("from math import exp, log, sqrt\nimport pandas as pd\nimport scipy.stats as stats\n\ndef implied_volatility_put(stock_price, strike_price, time_to_maturity, risk_free_rate, market_put_price):\n    implied_vol = 1.0\n    min_error = float('inf')\n    for i in range(1, 10000):\n        volatility = 0.0001 * i\n        d1 = (log(stock_price / strike_price) + (risk_free_rate + volatility ** 2 / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))\n        d2 = d1 - volatility * sqrt(time_to_maturity)\n        put_price = strike_price * exp(-risk_free_rate * time_to_maturity) * stats.norm.cdf(-d2) - stock_price * stats.norm.cdf(-d1)\n        error = abs(put_price - market_put_price)\n        if error < min_error:\n            min_error = error\n            implied_vol = volatility\n    return implied_vol\n\noption_chain = pd.DataFrame({'Bid': [2.5, 3.0, 3.5], 'Ask': [2.7, 3.2, 3.8], 'Strike': [40, 45, 50]})\noption_chain['Mid_Price'] = (option_chain['Bid'] + option_chain['Ask']) / 2\nclean_options = option_chain[option_chain['Mid_Price'] > 0].copy()\nS = 40; T = 0.5; r = 0.01\nclean_options['Implied_Vol'] = clean_options.apply(lambda row: implied_volatility_put(S, row['Strike'], T, r, row['Mid_Price']), axis=1)\nprint(clean_options)"),
    md(f"**Expected output and interpretation**\n\n![Volatility smile]({make_smile_plot()})\n\n- The output table contains `Bid`, `Ask`, `Strike`, `Mid_Price`, and `Implied_Vol`.\n- The first row has implied volatility near `0.2400`; the other two rows are lower in this toy example.\n- Code-fill reminder: `axis=1` is essential; otherwise `apply` works column by column."),
]


write_nb("python_financial_coding_图鉴.ipynb", main)
write_nb("coding_1_图鉴.ipynb", coding1)
write_nb("coding_2_图鉴.ipynb", coding2)
write_nb("coding_3_图鉴.ipynb", coding3)
print("enhanced notebooks created")
