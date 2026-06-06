# Financial Big Data

[中文说明](README.md)

Financial Big Data is a Python learning toolkit for financial instrument pricing, risk measurement, and portfolio performance analysis. It organizes commonly used financial formulas into reusable functions grouped by asset class.

> This project is intended for education, formula validation, and demonstrations. It is not investment advice and should not be used directly in production trading or risk systems.

## Overview

The project is useful for:

- studying and validating financial engineering models;
- performing basic valuation of bonds, equities, and derivatives;
- calculating duration, convexity, option Greeks, and implied volatility;
- analyzing portfolio performance and market risk;
- visualizing model sensitivity through the scripts in `examples/`.

## Project Structure

```text
financial_big_data/
├── bond/             # Bond pricing, yield, duration, convexity, and default risk
├── stock/            # Dividend discount models and performance ratios
├── futures/          # Futures pricing, hedging, rolling, and bond futures
├── options/          # Option pricing, Greeks, implied volatility, and applications
├── rate/             # Interest rates, FX, FRAs, forwards, and arbitrage
├── swap/             # Interest rate, currency, and credit default swaps
├── VaR/              # Value at Risk calculations
├── examples/         # Runnable examples and visualizations
├── __init__.py       # Package entry point, version, and plotting style
├── function_list.txt # Function and parameter index
└── requirements.txt  # Python dependencies
```

## Modules

| Module | Main functionality |
| --- | --- |
| `bond` | Bond pricing with single or multiple discount rates, yield to maturity, Macaulay/modified/dollar duration, convexity, and default probability |
| `stock` | Zero-, constant-, two-, and three-stage dividend discount models; Sharpe, Sortino, Treynor, Calmar, information ratio, and maximum drawdown |
| `futures` | Cost-of-carry pricing, hedge contract counts, stack-and-roll results, accrued interest, cheapest-to-deliver analysis, and Treasury bond futures hedging |
| `options` | Put-call parity, Black-Scholes, binomial trees, American options, futures options, Greeks, implied volatility, interest-rate options, swaptions, convertible bonds, and the Merton model |
| `rate` | FRA cash flows and valuation, forward rates, spot FX, triangular arbitrage, FX forwards, covered arbitrage, and FX forward valuation |
| `swap` | Interest rate swap cash flows and valuation, fixed/floating currency swap cash flows, currency swap valuation, and CDS cash flows |
| `VaR` | Variance-covariance Value at Risk |
| `examples` | Basic calculations and Matplotlib visualizations for each major module |

Each feature is implemented in a focused function file. Package-level modules and `__init__.py` files provide convenient imports:

```python
from financial_big_data.bond import bond_price_single_discount
from financial_big_data.options import black_scholes_option_price
```

## Setup

Python 3.11 or later is recommended. Create a virtual environment from the directory that contains this repository:

```powershell
cd path\to\my_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\financial_big_data\requirements.txt
```

The project is currently used directly as a source package and does not include a `setup.py` or `pyproject.toml`. Make sure the parent directory of `financial_big_data` is on the Python module search path when running your own scripts.

## Quick Start

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

Option pricing example:

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

## Running the Examples

From the project root:

```powershell
python .\examples\bond_example.py
python .\examples\stock_example.py
python .\examples\futures_example.py
python .\examples\options_example.py
python .\examples\rate_example.py
python .\examples\swap_example.py
python .\examples\VaR_example.py
```

The examples print calculated values and display Matplotlib charts. Use the top-level helper below to configure common Chinese fonts and display minus signs correctly:

```python
from financial_big_data import set_plot_style

set_plot_style()
```

## Dependencies

The main dependencies are NumPy, SciPy, pandas, Matplotlib, yfinance, numpy-financial, and statsmodels. See `requirements.txt` for the complete list and pinned versions.

## Notes

- Rates, returns, and volatility are generally expressed as decimals: `0.05` means 5%.
- Time inputs are generally expressed in years: `0.5` means six months.
- Compounding, position direction, and option-type conventions may vary by function. Check the relevant function signature and source before use.
- `function_list.txt` provides a quick index of functions and parameters.
- Independently validate results before using them in any important financial decision or system.

## License

No license file is currently included. All rights remain with the project author unless a license is added.
