from pathlib import Path
import sys

PROJECT_PARENT = Path(__file__).resolve().parents[2]
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))

import numpy as np
import matplotlib.pyplot as plt

from financial_big_data import set_plot_style
from financial_big_data.futures import price_futures

set_plot_style()

spot = 100
risk_free_rates = np.linspace(0.01, 0.06, 30)
try:
    prices = [price_futures(S=spot, r=r, T=1) for r in risk_free_rates]
except TypeError:
    prices = [spot * np.exp(r) for r in risk_free_rates]

print("Sample futures price:", round(prices[0], 4))
plt.plot(risk_free_rates, prices)
plt.xlabel("Risk-free rate")
plt.ylabel("Futures price")
plt.title("Futures price example")
plt.grid(True)
plt.show()
