# Financial Big Data

[English README](README_EN.md)

一个使用 Python 实现金融产品定价、风险度量和投资绩效分析的学习型工具库。项目按照金融产品类别组织，覆盖债券、股票、期货、期权、利率与汇率、互换以及风险价值（VaR）等常见主题。

> 本项目主要用于金融工程学习、公式验证和案例演示，不构成投资建议，也不应直接用于生产交易或风险管理。

## 项目用途

本项目把常见的金融计算公式封装成独立的 Python 函数，方便用于：

- 学习和验证金融工程模型；
- 对债券、股票及衍生品进行基础定价；
- 计算久期、凸性、希腊字母和隐含波动率等指标；
- 分析投资组合绩效和市场风险；
- 通过 `examples/` 中的脚本观察参数变化对计算结果的影响。

## 项目结构

```text
financial_big_data/
├── bond/             # 债券定价、收益率、久期、凸性和违约概率
├── stock/            # 股利贴现估值和投资组合绩效指标
├── futures/          # 期货定价、套期保值、展期和国债期货相关计算
├── options/          # 期权定价、希腊字母、隐含波动率及扩展应用
├── rate/             # 利率、远期利率、FRA、汇率和套利计算
├── swap/             # 利率互换、货币互换和信用违约互换
├── VaR/              # 风险价值计算
├── examples/         # 各模块的可视化使用示例
├── __init__.py       # 顶层包入口、版本信息和绘图样式
├── function_list.txt # 项目函数及参数索引
└── requirements.txt  # Python 依赖
```

## 模块说明

| 模块 | 主要内容 |
| --- | --- |
| `bond` | 单一/不同贴现率债券定价、到期收益率、麦考利久期、修正久期、美元久期、凸性、违约概率 |
| `stock` | 零增长、固定增长、两阶段和三阶段股利贴现模型；Sharpe、Sortino、Treynor、Calmar、信息比率及最大回撤 |
| `futures` | 持有成本期货定价、套期保值合约数量、展期损益、应计利息、最便宜交割券和国债期货套保 |
| `options` | 看涨看跌平价、Black-Scholes、二叉树、美式期权、期货期权、希腊字母、隐含波动率、利率期权、互换期权、可转债和 Merton 模型 |
| `rate` | FRA 现金流和估值、远期利率、即期外汇兑换、三角套利、远期外汇、抛补套利及远期外汇估值 |
| `swap` | 利率互换现金流和估值、固定/浮动货币互换现金流、货币互换估值及 CDS 现金流 |
| `VaR` | 方差-协方差法（Variance-Covariance Method）风险价值 |
| `examples` | 每个主要模块的简单计算与 Matplotlib 可视化 |

各子目录中的单函数文件负责具体计算，目录内的汇总模块和 `__init__.py` 负责统一导出。例如：

```python
from financial_big_data.bond import bond_price_single_discount
from financial_big_data.options import black_scholes_option_price
```

## 环境与安装

建议使用 Python 3.11 或更高版本，并在项目父目录中创建虚拟环境：

```powershell
cd path\to\my_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\financial_big_data\requirements.txt
```

项目目前直接以源码包形式使用，没有提供 `setup.py` 或 `pyproject.toml`。运行自己的脚本时，请确保 `financial_big_data` 的父目录位于 Python 模块搜索路径中。

## 快速上手

下面的例子计算一只债券的价格和麦考利久期：

```python
import numpy as np

from financial_big_data.bond import (
    bond_price_single_discount,
    macaulay_duration,
)

cashflow_times = np.arange(0.5, 5.5, 0.5)

price = bond_price_single_discount(
    coupon_rate=0.035,
    par_value=100,
    coupon_frequency=2,
    discount_rate=0.04,
    cashflow_times=cashflow_times,
)

duration = macaulay_duration(
    coupon_rate=0.035,
    par_value=100,
    coupon_frequency=2,
    yield_rate=0.04,
    cashflow_times=cashflow_times,
)

print("Bond price:", price)
print("Macaulay duration:", duration)
```

期权定价示例：

```python
from financial_big_data.options import black_scholes_option_price

call_value = black_scholes_option_price(
    spot_price=100,
    strike_price=100,
    volatility=0.20,
    interest_rate=0.03,
    time_to_maturity=1,
    option_type="call",
)

print("European call value:", call_value)
```

## 运行示例

在项目根目录执行：

```powershell
python .\examples\bond_example.py
python .\examples\stock_example.py
python .\examples\futures_example.py
python .\examples\options_example.py
python .\examples\rate_example.py
python .\examples\swap_example.py
python .\examples\VaR_example.py
```

示例脚本会输出计算结果，并使用 Matplotlib 显示图表。顶层函数 `set_plot_style()` 可设置常用中文字体并修复坐标轴负号显示：

```python
from financial_big_data import set_plot_style

set_plot_style()
```

## 主要依赖

- `NumPy`：数组和数值计算；
- `SciPy`：统计分布、优化和数值求解；
- `pandas`：时间序列与表格数据处理；
- `Matplotlib`：结果可视化；
- `yfinance`：市场数据获取；
- `numpy-financial`：金融计算函数；
- `statsmodels`：统计分析和建模。

完整版本要求见 `requirements.txt`。

## 使用说明

- 利率、收益率和波动率通常以小数输入，例如 `0.05` 表示 5%；
- 时间通常以“年”为单位，例如 `0.5` 表示半年；
- 不同函数对复利方式、头寸方向和期权类型的约定可能不同，使用前请查看对应函数的参数和源码；
- `function_list.txt` 提供了函数与参数的快速索引；
- 这是一个持续整理中的学习项目，建议在重要场景中对结果进行独立复核。

## 许可证

项目目前没有包含许可证文件。在添加许可证之前，所有权利归项目作者所有。
