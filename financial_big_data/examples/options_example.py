from pathlib import Path
import sys

PROJECT_PARENT = Path(__file__).resolve().parents[2]
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))

import numpy as np
import matplotlib.pyplot as plt

from financial_big_data import set_plot_style
from financial_big_data.options import black_scholes_option_price

set_plot_style()

spots = np.linspace(80, 120, 41)
try:
    values = [black_scholes_option_price(S=s, K=100, sigma=0.2, r=0.03, T=1, opt="call") for s in spots]
except TypeError:
    values = [black_scholes_option_price(s, 100, 0.2, 0.03, 1, "call") for s in spots]

print("Sample option value:", round(values[20], 4))
plt.plot(spots, values)
plt.xlabel("Spot price")
plt.ylabel("Option value")
plt.title("BSM option value")
plt.grid(True)
plt.show()
