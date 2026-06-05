import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "Notebooks"


def markdown(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip() + "\n"}


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.strip() + "\n",
    }


def notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.13",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def review_scaffold(title):
    normalized = title.lower()

    if any(word in normalized for word in ("future value", "present value", "annuit", "perpetuit", "npv", "irr", "payback")):
        return """
### Structured Review

- **Inputs:** Identify the cash-flow amount, timing, period rate, and number of periods.
- **Timeline first:** Mark time 0 separately and determine whether payments occur at the beginning or end of each period.
- **Frequency check:** Convert the rate or period count whenever their frequencies do not match.
- **Decision link:** Separate a valuation result from a project decision rule.

### Exam Focus

- Be able to reconstruct the formula from the cash-flow timeline.
- Check the exponent, discounting direction, and cash-flow sign.
- Verify a library result with a short manual calculation whenever possible.

### Common Mistakes

- Mixing annual rates with monthly periods.
- Discounting the time-zero cash flow.
- Confusing an annuity due with an ordinary annuity.
"""
    if any(word in normalized for word in ("module", "import", "package", "numpy", "help", "array")):
        return """
### Structured Review

- **Namespace:** Determine whether the function is called through a module name, an alias, or a direct import.
- **Dependency:** Import only the package required by the current code block.
- **Inspection:** Use version metadata, `dir()`, and documentation to understand an unfamiliar package.
- **Numerical object:** Distinguish ordinary Python containers from vectorized NumPy arrays.

### Exam Focus

- Complete the correct import statement before using a function.
- Recognize standard aliases such as `np`, `pd`, `yf`, and `plt`.
- Explain why wildcard imports make code harder to audit.

### Common Mistakes

- Installing a package into a different Python environment.
- Calling a module function without its namespace.
- Assuming a list automatically supports NumPy-style vectorized arithmetic.
"""
    if any(word in normalized for word in ("variable", "list", "tuple", "string", "function", "lambda", "index")):
        return """
### Structured Review

- **Object:** Identify the value and data type stored by each variable.
- **Access:** Remember that Python sequence indexing begins at zero.
- **Mutability:** Decide whether the object may be changed after creation.
- **Function contract:** Separate parameters, calculation steps, and the returned value.

### Exam Focus

- Preserve indentation inside functions and conditional blocks.
- Distinguish positional arguments from keyword arguments.
- Trace the value returned by a function for a small input.

### Common Mistakes

- Using the wrong capitalization in a variable name.
- Attempting to modify a tuple.
- Printing a result inside a function when the question requires `return`.
"""
    if any(word in normalized for word in ("black-scholes", "option", "gamma", "volatility")):
        return """
### Structured Review

- **Market inputs:** Identify spot price, strike, maturity, risk-free rate, volatility, and option premium.
- **Intermediate variables:** Compute `d1` before `d2`; both depend on consistent annualized inputs.
- **Distribution functions:** Distinguish the normal PDF from the normal CDF.
- **Sensitivity:** Interpret the result as a price or derivative with respect to an input.

### Exam Focus

- Reproduce the `d1` and `d2` sequence.
- Select `cdf` for option probabilities and `pdf` for Gamma.
- Check whether the formula is for a call, put, Delta, or Gamma.

### Common Mistakes

- Reversing spot and strike in the logarithm.
- Omitting the square root of maturity.
- Using percentage volatility such as `20` instead of decimal volatility `0.20`.
"""
    if any(word in normalized for word in ("csv", "return", "missing", "saving", "data", "aggregation")):
        return """
### Structured Review

- **Data source:** Record where the observations come from and whether the example is online, local, or simulated.
- **Cleaning:** Inspect missing values, data types, date order, and duplicated observations before calculating returns.
- **Transformation:** Use adjacent prices for one-period returns and compounding for multi-period returns.
- **Storage:** Choose CSV for portability and pickle only for trusted Python workflows that need preserved data types.

### Formula and Workflow

1. Sort observations by date.
2. Clean the price series without inventing unsupported returns.
3. Calculate simple or log returns.
4. Aggregate with products of growth factors or sums of log returns.
5. Validate one observation manually.

### Exam Focus

- Complete `P_t / P_(t-1) - 1`, `log(P_t/P_(t-1))`, and `prod(1+R)-1`.
- Distinguish price filling from return filling.
- Explain why averaging daily returns is not the exact monthly return.

### Common Mistakes

- Calculating returns on unsorted dates.
- Keeping the first missing return in a statistical test.
- Treating a percentage value as if it were already a decimal.
"""
    if any(word in normalized for word in ("bond", "ytm", "duration", "apr", "effective rate", "continuous", "credit spread", "dividend")):
        return """
### Structured Review

- **Cash flows:** Separate coupon payments, face value, dividends, and terminal value.
- **Rate convention:** Identify APR, effective period rate, effective annual rate, or continuous rate before substitution.
- **Discounting:** Match the payment frequency with the discount-rate frequency.
- **Risk interpretation:** Connect YTM and duration to bond-price sensitivity.

### Key Relationships

- Higher YTM generally implies a lower bond price.
- A coupon rate above YTM generally produces a premium bond.
- Earlier or larger cash flows generally reduce duration.
- One basis point equals `0.0001`.

### Exam Focus

- Calculate coupon per period and total number of periods.
- Add face value only to the final coupon cash flow.
- Distinguish Macaulay duration from modified duration.

### Common Mistakes

- Multiplying or dividing YTM by frequency in the wrong direction.
- Forgetting the negative cash-flow convention in financial-library functions.
- Using current dividend instead of next-period dividend in terminal value.
"""
    if any(word in normalized for word in ("capm", "regression", "beta", "rolling")):
        return """
### Structured Review

- **Dependent variable:** Asset return or asset excess return belongs on the left-hand side.
- **Independent variable:** Market return or market excess return explains the asset.
- **Intercept:** A constant column is required when alpha is estimated.
- **Alignment:** Join datasets by matching dates before running the regression.

### Interpretation

- `alpha` measures the intercept or abnormal return.
- `beta` measures sensitivity to the market factor.
- `R-squared` measures the proportion of sample variation explained by the model.
- A p-value evaluates statistical significance, not economic size.

### Exam Focus

- Preserve the order `x = market`, `y = stock`.
- Add a constant before OLS.
- Read the beta from the market coefficient, not the intercept.

### Common Mistakes

- Reversing stock and market inputs in `linregress`.
- Merging unmatched dates without checking missing values.
- Treating a high beta as proof of a high realized return.
"""
    if any(word in normalized for word in ("fama", "factor", "sharpe", "treynor", "sortino", "jensen", "lpsd", "performance", "portfolio")):
        return """
### Structured Review

- **Return basis:** Use excess return when the model or performance measure requires subtraction of the risk-free rate.
- **Risk denominator:** Match total risk, beta, or downside deviation to the correct measure.
- **Factor exposure:** Interpret each slope as sensitivity to a named systematic factor.
- **Model comparison:** Prefer adjusted R-squared when models contain different numbers of factors.

### Measure Map

| Measure | Numerator | Denominator |
|---|---|---|
| Sharpe | Mean excess return | Total standard deviation |
| Treynor | Mean excess return | Beta |
| Sortino | Mean excess return | Downside deviation |
| Jensen alpha | Realized minus CAPM-predicted return | None |

### Exam Focus

- Identify the correct denominator from the measure name.
- Keep factor returns and asset returns in the same units and frequency.
- State the null hypothesis for an individual t-test and the overall F-test.

### Common Mistakes

- Using total return instead of excess return in a factor regression.
- Comparing raw R-squared across models with different factor counts.
- Minimizing the positive Sharpe ratio instead of minimizing its negative.
"""
    if any(word in normalized for word in ("distribution", "confidence", "variance", "mean", "durbin", "granger", "normality", "january", "interpolation", "f-test")):
        return """
### Structured Review

- **Hypotheses:** Write the null and alternative before selecting a test.
- **Tail choice:** Determine whether the test is one-sided or two-sided.
- **Reference distribution:** Match the statistic with the normal, Student-t, F, or chi-square distribution.
- **Decision:** Compare either the p-value with alpha or the statistic with its critical value.

### Test Selection

| Question | Typical method |
|---|---|
| One mean versus a target | One-sample t-test |
| Two independent means | Pooled or Welch t-test |
| Equality of variances | F-test or Levene test |
| First-order residual autocorrelation | Durbin-Watson |
| Predictive content of lagged variables | Granger F-test |
| Normality | Shapiro-Wilk or Anderson-Darling |

### Exam Focus

- Use `alpha/2` in each tail of a two-sided test.
- Track degrees of freedom when calling `ppf`.
- State conclusions as evidence to reject or not reject the null hypothesis.

### Common Mistakes

- Saying that a large p-value proves the null hypothesis.
- Using a one-sided critical value for a two-sided interval.
- Interpreting Granger causality as structural or philosophical causation.
"""
    if "sql" in normalized or "join" in normalized:
        return """
### Structured Review

- **Left table:** Decide which records must always remain in the result.
- **Join key:** Confirm that both tables use compatible identifiers.
- **Join type:** Use inner for matched records, left/right for preserving one table, and outer for the union.
- **Missing match:** Expect null values when a preserved record has no counterpart.

### Exam Focus

- Complete the `ON left.key = right.key` condition.
- Predict which rows survive each join type.
- Close the database connection after reading results.

### Common Mistakes

- Joining on the wrong column.
- Expecting a left join to discard unmatched left-side rows.
- Confusing SQL `NULL` with the text string `"None"`.
"""
    return """
### Structured Review

- **Purpose:** State what the code calculates and why the quantity matters in finance.
- **Inputs:** Identify the required data, parameter units, and expected data type.
- **Process:** Follow the transformation in execution order rather than reading only the final line.
- **Output:** Connect the printed value to an economic or statistical interpretation.

### Exam Focus

- Identify the lines most likely to be removed in a code-completion question.
- Trace dimensions, indices, and units through each intermediate variable.
- Use a small numerical example to check the direction and scale of the answer.

### Common Mistakes

- Reusing a variable with a different meaning.
- Depending on a previous notebook cell for an import or intermediate object.
- Reporting a number without explaining its financial meaning.
"""


def add_topic(cells, title, explanation, source, result):
    cells.append(markdown(f"## {title}\n\n{explanation}\n\n{review_scaffold(title)}"))
    cells.append(code(source))
    cells.append(
        markdown(
            f"""**Result interpretation.** {result}

### Result Checklist

- Confirm that the sign and magnitude are economically reasonable.
- Match the output to the formula, decision rule, or statistical hypothesis described above.
- If the result differs from expectation, inspect input frequency, indexing, and parameter order first.
"""
        )
    )


def chapter_1():
    cells = [
        markdown(
            """
# Chapter 1: Python Basics for Financial Data Mining

This chapter introduces the working environment and the Python concepts needed
throughout the course. The examples use small finance-oriented calculations so
that syntax is learned together with interpretation.

## Learning map

1. Python environments and the Jupyter workflow
2. Variables, indexing, and case sensitivity
3. Lists, tuples, and mutability
4. Strings, comments, and mathematical modules
5. Functions and parameter passing
6. Future value and present value functions

**Code availability:** Yes. Every code cell is self-contained and can be run
independently.

## How to Study This Chapter

- Read the syntax rule and immediately trace the corresponding finance example.
- Re-type short functions instead of memorizing only their output.
- Pay special attention to indentation, indexing, mutability, and `return`.
- Before execution, predict the data type and printed value.

## Exam Checklist

- Can I distinguish a list, tuple, string, and numerical scalar?
- Can I define and call a function with positional and keyword arguments?
- Can I explain every symbol in the future-value and present-value formulas?
"""
        ),
        markdown(
            """
## 1.1 Python Tools Used in the Course

- **Spyder** is suitable for long scripts, debugging, and reusable programs.
- **Jupyter Notebook** is suitable for exploratory analysis, formulas, charts,
  explanations, and reproducible reports.
- **JupyterLab** provides notebooks, terminals, and file management in one
  browser-based workspace.

In Jupyter, press `Shift+Enter` to execute the current cell and move to the next
cell. Python is case-sensitive, uses indentation to define code blocks, and
starts sequence indexing at zero.
"""
        ),
    ]
    add_topic(
        cells,
        "1.2 Variables, Case Sensitivity, and Zero-Based Indexing",
        """
A variable stores an object. `price` and `Price` are different names. A list
index identifies the position of an observation, beginning with index `0`.
This matters when selecting the first price, return, or cash flow.
""",
        """
'''
本单元演示变量赋值、大小写敏感和从零开始的索引。
价格序列代表连续三个交易日的收盘价。
'''
price = 100
Price = 105
closing_prices = [100.0, 101.5, 99.8]

# Python 序列从 0 开始计数，索引 0 表示第一项
print("price =", price)
print("Price =", Price)
print("First closing price =", closing_prices[0])
print("Third closing price =", closing_prices[2])
""",
        "The two differently capitalized variables coexist, and index `0` returns the first market observation.",
    )
    add_topic(
        cells,
        "1.3 Lists and Tuples",
        """
Lists are mutable: their elements can be updated after creation. Tuples are
immutable and are useful for values that should stay fixed, such as a contract
description or a pair of model parameters.
""",
        """
'''
本单元比较列表与元组。
列表中的投资组合权重可以调整；元组中的合约信息保持不变。
'''
portfolio_weights = [0.60, 0.40]

# 列表可变：通过索引直接修改指定位置的元素
portfolio_weights[0] = 0.55
portfolio_weights[1] = 0.45

# 元组不可变，适合保存不应被修改的合约属性
bond_contract = ("US Treasury", 10)

print("Adjusted weights =", portfolio_weights)
print("Fixed contract description =", bond_contract)
print("Weight sum =", sum(portfolio_weights))
""",
        "The list accepts rebalancing and the weights still sum to one; the tuple represents fixed descriptive information.",
    )
    add_topic(
        cells,
        "1.4 Strings and Mathematical Constants",
        """
Strings store labels such as ticker symbols. Methods like `.upper()` and
`.lower()` standardize text. The standard-library `math` module provides
constants and mathematical functions without requiring an external package.
""",
        """
'''
本单元演示字符串标准化以及 math 模块中的常数和函数。
按需导入 math，避免依赖其他单元。
'''
import math

ticker = "ibm"

# math.exp(x) 计算 e 的 x 次方，常用于连续复利
continuous_growth = math.exp(0.05)

# upper() 将字符串统一转换为大写
print("Standardized ticker =", ticker.upper())
print("Euler's number =", round(math.e, 6))
print("Pi =", round(math.pi, 6))
print("One-year growth factor at 5% continuous growth =", round(continuous_growth, 6))
""",
        "The ticker is standardized for consistent labeling, and `exp(0.05)` gives the continuous-compounding growth factor.",
    )
    add_topic(
        cells,
        "1.5 Defining Reusable Functions",
        """
A function packages a calculation behind a clear name. Parameters are inputs,
and `return` sends the computed value back to the caller. Keyword arguments make
financial inputs easier to audit because their meanings are explicit.
""",
        """
'''
本单元定义一个简单的收益放大函数。
函数、参数、缩进和 return 是后续金融模型复用的基础。
'''
def scale_return(period_return, multiplier):
    # return 将计算结果返回给函数调用者
    return period_return * multiplier

base_return = 0.025

print("Positional arguments =", scale_return(base_return, 2))
print("Keyword arguments =", scale_return(period_return=base_return, multiplier=3))
""",
        "The same function works with positional or keyword arguments; keyword input is usually clearer in longer financial formulas.",
    )
    add_topic(
        cells,
        "1.6 Future Value",
        """
Future value compounds a present amount:

$$FV = PV(1+r)^n$$

The rate `r` and number of periods `n` must use the same frequency. For example,
an annual rate requires a number of years, while a monthly rate requires a
number of months.
""",
        """
'''
本单元封装复利终值函数。
pv 为现值，r 为每期利率，n 为期数；利率频率必须与期数一致。
'''
def future_value(pv, r, n):
    # 复利终值公式：现值乘以 (1 + 每期利率) 的 n 次方
    return pv * (1 + r) ** n

# 位置参数必须严格按照函数定义中的参数顺序传入
fv_positional = future_value(100, 0.10, 2)

# 关键字参数直接写明变量含义，顺序可以调整
fv_keyword = future_value(pv=100, r=0.0123, n=5)

print("FV of $100 at 10% for 2 years =", round(fv_positional, 2))
print("FV of $100 at 1.23% for 5 years =", round(fv_keyword, 2))
""",
        "Compounding produces $121.00 in the first example and approximately $106.30 in the lecture example.",
    )
    add_topic(
        cells,
        "1.7 Present Value",
        """
Present value reverses compounding:

$$PV = \\frac{FV}{(1+r)^n}$$

It answers how much a future cash flow is worth today at a required return or
discount rate.
""",
        """
'''
本单元封装现值函数，并用终值函数进行反向验证。
每个函数均在本单元内定义，因此可以独立运行。
'''
def future_value(pv, r, n):
    # 将现值向未来复利
    return pv * (1 + r) ** n

def present_value(fv, r, n):
    # 将未来值除以复利因子，折现回当前时点
    return fv / (1 + r) ** n

today = present_value(fv=110, r=0.10, n=1)

# 用终值函数反向验证现值计算是否正确
recovered_future = future_value(pv=today, r=0.10, n=1)

print("Present value =", round(today, 2))
print("Compounded back to the future =", round(recovered_future, 2))
""",
        "Discounting $110 for one year at 10% gives $100, and compounding it again recovers the original future value.",
    )
    add_topic(
        cells,
        "1.8 Lambda Functions from the Classroom Script",
        """
The instructor's source code also demonstrates `lambda`, a compact way to
define a short anonymous function. It is frequently used as an objective,
transformation, or row-level operation.
""",
        """
'''
本单元补充老师源代码中的 lambda 函数。
lambda 后写参数，冒号后写返回表达式，适合简短的一行函数。
'''
# 单变量 lambda：输入收益率并转换为增长因子
growth_factor = lambda return_rate: 1 + return_rate

# 多变量 lambda：x 是包含两个元素的向量
distance_objective = lambda x: (x[0] - 10) ** 2 + (x[1] - 25) ** 2

print("Growth factor =", growth_factor(0.08))
print("Objective at (11, 27) =", distance_objective((11, 27)))
""",
        "The first lambda returns 1.08. The second evaluates squared distance from the target point `(10, 25)`.",
    )
    cells.append(
        markdown(
            """
## Chapter Review

- Python names are case-sensitive and indentation defines program structure.
- Sequences start at index zero.
- Lists are mutable; tuples are immutable.
- Modules provide reusable functions and constants.
- Functions turn formulas into auditable, reusable tools.
- Financial rates and periods must always use matching frequencies.
"""
        )
    )
    return notebook(cells)


def chapter_2():
    cells = [
        markdown(
            """
# Chapter 2: Python Modules and Packages

A module is a collection of related Python objects, such as functions, classes,
and constants. Packages organize modules into larger toolboxes. This chapter
focuses on importing, inspecting, installing, and using packages responsibly.

## Learning map

1. Why modules are needed
2. Import styles and conventional aliases
3. Package metadata and object inspection
4. Help and documentation
5. Package installation commands
6. NumPy arrays
7. A modular Black-Scholes example

**Code availability:** Yes. Installation commands are shown as Markdown because
they should be run in a terminal, while Python demonstrations are independently
runnable.

## How to Study This Chapter

- Practice all import styles and identify the namespace created by each one.
- Inspect one package with version metadata, `dir()`, and its docstring.
- Separate terminal installation commands from Python code.
- Re-run every example in a fresh kernel to confirm that dependencies are local.

## Exam Checklist

- Can I write the correct import before calling a function?
- Can I explain why conventional aliases improve readability?
- Can I distinguish package installation from package import?
- Can I use a NumPy array for vectorized financial calculations?
"""
        )
    ]
    add_topic(
        cells,
        "2.1 Why Modules Are Needed",
        """
Python does not place every possible function in the default namespace.
Importing a module makes a focused set of tools available and keeps their origin
visible. For example, `sqrt` belongs to the standard-library `math` module.
""",
        """
'''
本单元演示通过模块命名空间调用函数。
使用 math.sqrt 可以清楚看到函数来源，并避免命名冲突。
'''
import math

# 模块名位于点号左侧，函数名位于点号右侧
value = math.sqrt(3)
print("Square root of 3 =", value)
""",
        "`math.sqrt(3)` works because the module has been imported and the function is accessed through its namespace.",
    )
    add_topic(
        cells,
        "2.2 Import Styles and Conventional Aliases",
        """
Common import styles include `import module`, `import module as alias`, and
`from module import object`. Explicit imports are preferred over wildcard
imports because they make dependencies and names easier to trace.
""",
        """
'''
本单元比较三种常见导入方式。
示例仅使用标准库，且所有依赖都在当前单元中导入。
'''
import math
import math as m
from math import sqrt

# 完整模块名调用：来源最清楚
print("Module namespace =", math.sqrt(9))

# 别名调用：适合名称较长且频繁使用的模块
print("Alias namespace =", m.sqrt(16))

# 直接导入函数后，不需要再写模块名前缀
print("Direct function import =", sqrt(25))
""",
        "All three approaches calculate square roots, but module namespaces provide the clearest provenance.",
    )
    cells.append(
        markdown(
            """
## 2.3 Conventional Aliases

Frequently used packages have community conventions:

```python
import numpy as np
import pandas as pd
import scipy as sp
import yfinance as yf
import matplotlib.pyplot as plt
```

Aliases are not mandatory, but following conventions makes code easier for
other analysts to read. Each notebook code unit should still import only the
packages it actually uses.
"""
        )
    )
    add_topic(
        cells,
        "2.4 Inspecting a Package",
        """
`dir()` lists names exposed by an object. Package metadata can report the
installed version. Inspection is useful when learning a new financial library,
but the official documentation remains the best source for detailed behavior.
""",
        """
'''
本单元检查 NumPy 的版本与可用对象数量。
按需导入 numpy 和标准库 metadata，不依赖前置单元。
'''
import numpy as np
from importlib.metadata import version

# dir() 返回模块中的名称；过滤下划线开头的内部对象
public_objects = [name for name in dir(np) if not name.startswith("_")]

print("NumPy version =", version("numpy"))
print("Number of public NumPy objects =", len(public_objects))
print("Sample objects =", public_objects[:10])
""",
        "The exact version and object count depend on the local environment, so they should be checked rather than memorized.",
    )
    add_topic(
        cells,
        "2.5 Reading Help Without Flooding the Notebook",
        """
`help(object)` prints the full documentation, which can be very long. In a
revision notebook, the first line of the docstring is often enough to identify
the purpose before opening the complete reference.
""",
        """
'''
本单元读取函数文档的第一行，避免输出过长。
np.std 用于计算标准差，是金融风险度量中的基础函数。
'''
import numpy as np

# __doc__ 保存函数文档；这里只提取第一行作为功能摘要
summary = np.std.__doc__.strip().splitlines()[0]

# np.std 默认计算总体标准差，衡量收益率的离散程度
example = np.std([0.01, -0.02, 0.03, 0.00])

print("np.std summary:", summary)
print("Example population standard deviation =", round(float(example), 6))
""",
        "The docstring identifies the function, and the example measures dispersion in a small return series.",
    )
    cells.append(
        markdown(
            """
## 2.6 Installing and Managing Packages

Run package-management commands in **Anaconda Prompt**, PowerShell, Terminal, or
a Jupyter cell prefixed with `!`. Typical commands are:

```text
python -m pip install numpy
python -m pip install yfinance
python -m pip install numpy-financial
python -m pip install --upgrade pip
python -m pip list
python -m pip show numpy
```

Version constraints can improve reproducibility:

```text
python -m pip install "SomeProject==1.4"
python -m pip install "SomeProject>=1,<2"
```

Use the active environment's Python executable. Installing into a different
environment is a common reason that an import still fails after installation.
"""
        )
    )
    add_topic(
        cells,
        "2.7 NumPy Arrays for Financial Data",
        """
A NumPy array stores homogeneous numerical data and supports vectorized
operations. It is more suitable than a plain list for repeated numerical
calculations such as return transformations and scenario analysis.
""",
        """
'''
本单元使用 NumPy 数组保存资产收益率并进行向量化计算。
所有收益率同时乘以投资金额，得到各情景下的盈亏。
'''
import numpy as np

returns = np.array([0.02, -0.01, 0.015, 0.005])
investment = 10_000

# 数组与标量相乘会逐元素运算，无需手写 for 循环
profit_and_loss = investment * returns

print("Returns =", returns)
print("Scenario P&L =", profit_and_loss)
print("Average return =", round(float(returns.mean()), 6))
""",
        "Vectorization converts all return scenarios into dollar profit and loss without writing an explicit loop.",
    )
    add_topic(
        cells,
        "2.8 Modular Black-Scholes Call Function",
        """
The lecture uses the Black-Scholes call formula to demonstrate that a function
can import only the objects it needs. The example also previews how NumPy and
SciPy support later finance topics.

$$C=S\\Phi(d_1)-Xe^{-rT}\\Phi(d_2)$$
""",
        """
'''
本单元实现欧式看涨期权的 Black-Scholes 定价函数。
函数内部按需导入 NumPy 数学函数与 SciPy 正态分布工具，
因此本单元可独立运行，并清楚展示模块化依赖。
'''
def black_scholes_call(S, X, T, r, sigma):
    # 函数内部按需导入：log、exp、sqrt 负责公式计算
    from numpy import exp, log, sqrt

    # norm.cdf() 计算标准正态分布的累积概率 Phi(d)
    from scipy.stats import norm

    # d1 同时包含价内程度、无风险利率、波动率和到期时间
    d1 = (log(S / X) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))

    # d2 等于 d1 减去一个波动率时间尺度
    d2 = d1 - sigma * sqrt(T)

    # 看涨期权价值 = 股票现值部分 - 行权价格现值部分
    return S * norm.cdf(d1) - X * exp(-r * T) * norm.cdf(d2)

call_value = black_scholes_call(S=100, X=100, T=1, r=0.05, sigma=0.20)
print("European call value =", round(float(call_value), 4))
""",
        "For the stated assumptions, the model produces a call value of approximately $10.45.",
    )
    cells.append(
        markdown(
            """
## Chapter Review

- Modules organize related programs and reduce duplication.
- Prefer explicit imports and standard aliases.
- Use `dir()`, metadata, docstrings, and official documentation to inspect tools.
- Install packages into the same environment that runs the notebook.
- NumPy enables vectorized numerical analysis.
- Functions should declare their own required dependencies when independence is important.
"""
        )
    )
    return notebook(cells)


def chapter_3():
    cells = [
        markdown(
            """
# Chapter 3: Time Value of Money and Investment Decisions

This chapter converts the lecture formulas into reusable Python modules. Every
code cell is self-contained and uses either a formula, `numpy-financial`, or
both to verify the result.

## Learning map

1. Cash-flow timelines and rate consistency
2. Future and present value
3. Perpetuities and delayed perpetuities
4. Ordinary annuities and annuities due
5. Growing annuities
6. Excel and `numpy-financial` sign conventions
7. NPV and IRR decision rules
8. Ordinary and discounted payback periods
9. NPV profiles and multiple IRRs

**Code availability:** Yes. Every code cell imports its own dependencies and
produces a numerical or visual result.

## How to Study This Chapter

- Draw a cash-flow timeline before selecting a formula.
- Label the rate frequency and payment timing explicitly.
- Compare manual formulas with `numpy-financial` outputs.
- Practice both valuation questions and accept/reject decision rules.

## Exam Checklist

- Can I distinguish ordinary, due, growing, and delayed cash-flow patterns?
- Can I apply the Excel sign convention correctly?
- Can I calculate and interpret NPV, IRR, and payback?
- Can I explain why non-conventional cash flows may generate multiple IRRs?
"""
        ),
        markdown(
            """
## 3.1 Cash-Flow Timelines and Rate Consistency

A timeline identifies **when** each cash flow occurs. Receiving money is
normally represented as positive, while investing or repaying money is
negative. The period rate and number of periods must have the same frequency.

Example loan timeline:

| Time | Borrower's cash flow |
|---:|---:|
| 0 | +100 |
| 1 | -10 |
| 2 | -110 |
"""
        ),
    ]
    add_topic(
        cells,
        "3.2 Future Value and Present Value",
        """
The core formulas are:

$$FV=PV(1+r)^n, \\qquad PV=\\frac{FV}{(1+r)^n}$$

These functions form the basis of bond, stock, project, and derivative
valuation.
""",
        """
'''
本单元同时定义终值和现值函数，并进行双向验证。
r 为每期利率，n 为期数，两者的频率必须一致。
'''
def future_value(pv, r, n):
    # 终值：把当前金额按每期利率复利 n 期
    return pv * (1 + r) ** n

def present_value(fv, r, n):
    # 现值：把未来金额除以复利因子
    return fv / (1 + r) ** n

fv = future_value(pv=100, r=0.0123, n=5)
pv = present_value(fv=100, r=0.05, n=5)

print("FV example =", round(fv, 2))
print("PV example =", round(pv, 2))
print("Reverse-check =", round(present_value(fv, 0.0123, 5), 2))
""",
        "The lecture future-value example is about $106.30, and discounting $100 for five years at 5% gives about $78.35.",
    )
    add_topic(
        cells,
        "3.3 Perpetuities and Delayed Perpetuities",
        """
An ordinary perpetuity pays the same cash flow forever, beginning one period
from today:

$$PV_0=\\frac{C}{r}$$

If the first payment arrives at time `k`, first value the perpetuity at time
`k-1`, then discount it back to time zero:

$$PV_0=\\frac{C/r}{(1+r)^{k-1}}$$
""",
        """
'''
本单元计算普通永续年金与延期永续年金。
k 表示第一笔现金流发生的期数，因此永续年金价值位于 k-1 期。
'''
def pv_perpetuity(cash_flow, rate):
    # 普通永续年金第一笔现金流发生在第 1 期末
    return cash_flow / rate

def pv_delayed_perpetuity(cash_flow, rate, first_payment_period):
    # 永续年金价值位于第一笔付款的前一期，即 k-1 期
    value_before_first_payment = cash_flow / rate

    # 再将 k-1 期的价值折现回 0 期
    return value_before_first_payment / (1 + rate) ** (first_payment_period - 1)

ordinary = pv_perpetuity(cash_flow=100, rate=0.10)
delayed = pv_delayed_perpetuity(cash_flow=100, rate=0.10, first_payment_period=4)

print("Ordinary perpetuity PV =", round(ordinary, 2))
print("Delayed perpetuity PV =", round(delayed, 2))
""",
        "The ordinary perpetuity is worth $1,000 today; delaying its first payment to year 4 lowers today's value.",
    )
    add_topic(
        cells,
        "3.4 Ordinary Annuities and Annuities Due",
        """
An ordinary annuity pays at each period end:

$$PV=C\\frac{1-(1+r)^{-n}}{r}, \\qquad
FV=C\\frac{(1+r)^n-1}{r}$$

An annuity due pays at each period beginning, so its value equals the ordinary
annuity value multiplied by `(1+r)`.
""",
        """
'''
本单元计算普通年金及先付年金的现值和终值。
先付年金比普通年金早一期收到每笔现金流，因此多乘一个增长因子。
'''
def pv_annuity(cash_flow, rate, periods, due=False):
    # 先计算期末支付的普通年金现值
    value = cash_flow * (1 - (1 + rate) ** (-periods)) / rate

    # 先付年金每笔现金流提前一期，因此普通年金价值乘以 (1+r)
    return value * (1 + rate) if due else value

def fv_annuity(cash_flow, rate, periods, due=False):
    # 普通年金终值公式
    value = cash_flow * ((1 + rate) ** periods - 1) / rate

    # due=True 时转换为先付年金终值
    return value * (1 + rate) if due else value

pv_ordinary = pv_annuity(100, 0.05, 10)
pv_due = pv_annuity(100, 0.05, 10, due=True)
fv_ordinary = fv_annuity(100, 0.05, 10)

print("Ordinary annuity PV =", round(pv_ordinary, 2))
print("Annuity-due PV =", round(pv_due, 2))
print("Ordinary annuity FV =", round(fv_ordinary, 2))
""",
        "Earlier payments make the annuity due more valuable than the otherwise identical ordinary annuity.",
    )
    add_topic(
        cells,
        "3.5 Growing Annuities",
        """
For a first payment `C` at time 1 growing at rate `g`, the present value is:

$$PV=C\\frac{1-\\left(\\frac{1+g}{1+r}\\right)^n}{r-g}, \\quad r\\ne g$$

The future value at time `n` is:

$$FV=C\\frac{(1+r)^n-(1+g)^n}{r-g}$$

**Correction to the raw course script:** the denominator must be `r-g`, not
`r`. The corrected formula below is also verified by discounting each cash flow.
""",
        """
'''
本单元实现增长年金的正确公式，并用逐期现金流求和进行验证。
原始课程总代码分母写成 r；标准公式分母应为 r-g。
当 r 与 g 相等时，改用逐期求和以避免除零。
'''
def pv_growing_annuity(cash_flow, rate, growth, periods):
    # r=g 时标准公式分母为零，必须改用逐期折现求和
    if abs(rate - growth) < 1e-12:
        return sum(
            cash_flow * (1 + growth) ** (t - 1) / (1 + rate) ** t
            for t in range(1, periods + 1)
        )

    # 重要填空：增长年金公式的分母是 rate-growth，不是 rate
    return cash_flow * (1 - ((1 + growth) / (1 + rate)) ** periods) / (rate - growth)

def fv_growing_annuity(cash_flow, rate, growth, periods):
    # r=g 时使用对应的极限形式
    if abs(rate - growth) < 1e-12:
        return cash_flow * periods * (1 + rate) ** (periods - 1)

    # 增长年金终值同样使用 rate-growth 作为分母
    return cash_flow * ((1 + rate) ** periods - (1 + growth) ** periods) / (rate - growth)

c, r, g, n = 100, 0.15, 0.02, 10
formula_pv = pv_growing_annuity(c, r, g, n)

# 逐期生成增长现金流并折现，用于检查封闭公式
direct_pv = sum(c * (1 + g) ** (t - 1) / (1 + r) ** t for t in range(1, n + 1))

print("Growing annuity PV =", round(formula_pv, 2))
print("Direct cash-flow check =", round(direct_pv, 2))
print("Growing annuity FV =", round(fv_growing_annuity(c, r, g, n), 2))
""",
        "The formula and direct cash-flow calculation match, confirming the corrected implementation.",
    )
    add_topic(
        cells,
        "3.6 Excel and numpy-financial Sign Conventions",
        """
Excel-style financial functions treat cash inflows and outflows as opposite
signs. A positive future receipt therefore corresponds to a negative present
investment. `numpy-financial` follows this convention and mirrors functions
such as `PV`, `FV`, `PMT`, `NPER`, and `RATE`.
""",
        """
'''
本单元展示 numpy_financial 的现金流符号约定。
今天支付 100 属于现金流出，因此输入 pv=-100，未来收到的金额为正。
'''
import numpy_financial as npf

# 现金流出使用负号：今天投入 100，未来收到正的终值
future_receipt = npf.fv(rate=0.10, nper=1, pmt=0, pv=-100)

# 未来收到 110 为正，因此对应的当前投入由函数返回负值
present_outflow = npf.pv(rate=0.10, nper=1, pmt=0, fv=110)

print("Future receipt =", round(float(future_receipt), 2))
print("Present outflow =", round(float(present_outflow), 2))
""",
        "The future receipt is positive and the corresponding present investment is negative, matching the Excel convention.",
    )
    add_topic(
        cells,
        "3.7 Net Present Value and the NPV Rule",
        """
NPV discounts all project cash flows to time zero:

$$NPV=\\sum_{t=0}^{n}\\frac{CF_t}{(1+r)^t}$$

Decision rule: accept an independent project when `NPV > 0` and reject it when
`NPV < 0`. In `numpy_financial.npv`, include the time-zero cash flow as the first
element if using the full cash-flow list.
""",
        """
'''
本单元用手工公式和 numpy_financial 两种方法计算 NPV。
现金流列表的第一个元素是 0 期初始投资，负号表示现金流出。
'''
import numpy_financial as npf

cash_flows = [-100, 50, 60, 70]
required_return = 0.12

# enumerate 同时提供时间 t 和现金流 cf；0 期现金流不折现
manual_npv = sum(cf / (1 + required_return) ** t for t, cf in enumerate(cash_flows))

# npf.npv 将列表第一项视为 0 期现金流
library_npv = npf.npv(required_return, cash_flows)

# NPV 决策规则：大于 0 接受，否则拒绝
decision = "Accept" if library_npv > 0 else "Reject"

print("Manual NPV =", round(manual_npv, 2))
print("numpy-financial NPV =", round(float(library_npv), 2))
print("Decision =", decision)
""",
        "Both methods agree. A positive NPV means the project adds value at the 12% required return.",
    )
    add_topic(
        cells,
        "3.8 Internal Rate of Return and the IRR Rule",
        """
IRR is the discount rate that makes NPV equal to zero. Decision rule: accept a
project when `IRR` exceeds the firm's required return. Non-conventional cash
flows can have multiple IRRs, so IRR should be interpreted together with NPV.
""",
        """
'''
本单元计算 IRR，并将其代回 NPV 公式验证 NPV 接近零。
随后比较 IRR 与资本成本，形成项目决策。
'''
import numpy_financial as npf

cash_flows = [-100, 50, 60, 70]
cost_of_capital = 0.12

# IRR 是使项目 NPV 等于 0 的折现率
irr = npf.irr(cash_flows)

# 将 IRR 代回 NPV，结果应非常接近 0
npv_at_irr = npf.npv(irr, cash_flows)

# IRR 决策规则：IRR 高于资本成本时接受项目
decision = "Accept" if irr > cost_of_capital else "Reject"

print("IRR =", f"{irr:.2%}")
print("NPV evaluated at IRR =", round(float(npv_at_irr), 10))
print("Decision =", decision)
""",
        "The calculated IRR is above the 12% cost of capital, and the NPV evaluated at that IRR is approximately zero.",
    )
    add_topic(
        cells,
        "3.9 Ordinary and Discounted Payback Periods",
        """
The ordinary payback period measures how quickly undiscounted inflows recover
the initial investment. Discounted payback applies the time value of money
first. A project passes the rule when its payback is shorter than the firm's
maximum allowed period, but payback ignores cash flows after recovery.
""",
        """
'''
本单元分别计算普通回收期和折现回收期。
函数逐期累计现金流，并对最后一个未完整年度按比例插值。
若项目在给定现金流内无法回收，则返回 None。
'''
def payback_period(initial_investment, inflows, discount_rate=0.0):
    # recovered 保存截至当前年度已收回的累计金额
    recovered = 0.0

    # start=1 使第一笔未来现金流对应第 1 年
    for year, inflow in enumerate(inflows, start=1):
        # discount_rate=0 时为普通回收期；大于 0 时为折现回收期
        adjusted_inflow = inflow / (1 + discount_rate) ** year
        remaining_before_year = initial_investment - recovered

        # 如果本年现金流足以覆盖剩余投资，则进行年度内线性插值
        if recovered + adjusted_inflow >= initial_investment:
            return (year - 1) + remaining_before_year / adjusted_inflow

        # 尚未收回投资时，将本年现金流加入累计值
        recovered += adjusted_inflow

    # 所有给定现金流结束后仍未回收投资
    return None

initial = 100
future_inflows = [50, 30, 30, 20, 25]

ordinary = payback_period(initial, future_inflows)
discounted = payback_period(initial, future_inflows, discount_rate=0.12)

print("Ordinary payback =", round(ordinary, 2), "years")
print("Discounted payback =", round(discounted, 2), "years")
""",
        "The ordinary payback is about 2.67 years. Discounting delays recovery because future inflows are worth less today.",
    )
    add_topic(
        cells,
        "3.10 NPV Profile and Multiple IRRs",
        """
An NPV profile plots project NPV against the discount rate. Each crossing of
the horizontal axis is a candidate IRR. Cash flows that change sign more than
once can generate multiple IRRs, making the NPV rule more reliable.
""",
        """
'''
本单元绘制非传统现金流的 NPV 曲线。
现金流多次改变符号，可能使 NPV 曲线多次穿过零轴并产生多个 IRR。
'''
import numpy as np

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

cash_flows = [504, -432, -432, -432, 832]
rates = np.linspace(-0.45, 1.50, 800)

def project_npv(rate, cash_flows):
    # 每笔现金流按其时间 t 折现，并对所有现值求和
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))

# 在一系列折现率上计算 NPV，形成 NPV profile
npv_values = np.array([project_npv(rate, cash_flows) for rate in rates])

# 相邻 NPV 符号发生变化，表示曲线在两点之间穿过零轴
crossing_indices = np.where(np.sign(npv_values[:-1]) != np.sign(npv_values[1:]))[0]
approximate_irrs = rates[crossing_indices]

if plt is not None:
    plt.figure(figsize=(8, 4.5))
    plt.plot(rates, npv_values, color="navy", label="NPV profile")
    plt.axhline(0, color="black", linewidth=1)
    plt.axvline(0, color="gray", linewidth=0.8, linestyle="--")
    plt.ylim(-800, 1200)
    plt.xlabel("Discount rate")
    plt.ylabel("Net present value")
    plt.title("NPV Profile for Non-Conventional Cash Flows")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.show()
else:
    print("ASCII NPV profile (o = NPV point, | = zero-NPV level)")
    sample_rates = np.linspace(-0.40, 1.40, 31)
    sample_npvs = np.array([project_npv(rate, cash_flows) for rate in sample_rates])
    lower, upper, width = -800, 1200, 60
    zero_col = int((0 - lower) / (upper - lower) * width)
    for rate, value in zip(sample_rates, sample_npvs):
        clipped = min(max(value, lower), upper)
        value_col = int((clipped - lower) / (upper - lower) * width)
        row = [" "] * (width + 1)
        row[zero_col] = "|"
        row[value_col] = "o"
        print(f"{rate:>6.1%} {''.join(row)} {value:>9.1f}")

print("Approximate zero crossings =", [round(float(x), 4) for x in approximate_irrs])
""",
        "The graph can cross zero more than once. Those crossings illustrate why a single IRR may be ambiguous for non-conventional projects.",
    )
    cells.append(
        markdown(
            """
## Chapter Review

- Place every cash flow on a timeline before applying a formula.
- Match the rate frequency with the number of periods.
- Payments at the beginning of a period are more valuable than end-of-period payments.
- Growing annuity formulas use the denominator `r-g`.
- Excel and `numpy-financial` use opposite signs for inflows and outflows.
- NPV directly measures value creation; IRR is a break-even rate.
- Discounted payback is more economically meaningful than ordinary payback, but both ignore later cash flows.
- Multiple sign changes can create multiple IRRs; inspect the NPV profile.
"""
        )
    )
    return notebook(cells)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    chapters = {
        "chapter_1.ipynb": chapter_1(),
        "chapter_2.ipynb": chapter_2(),
        "chapter_3.ipynb": chapter_3(),
    }
    for filename, content in chapters.items():
        path = OUTPUT_DIR / filename
        path.write_text(
            json.dumps(content, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
