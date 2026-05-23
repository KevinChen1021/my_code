from pathlib import Path
import sys

PROJECT_PARENT = Path(__file__).resolve().parents[2]
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))

import numpy as np
import matplotlib.pyplot as plt

from financial_big_data import set_plot_style
from financial_big_data.bond import bond_price_single_discount, macaulay_duration

set_plot_style()

t = np.arange(0.5, 5.5, 0.5)
yields = np.linspace(0.02, 0.06, 30)
prices = [bond_price_single_discount(coupon_rate=0.035, par_value=100, coupon_frequency=2, discount_rate=y, cashflow_times=t) for y in yields]

print("Bond price:", round(bond_price_single_discount(0.035, 100, 2, 0.04, t), 4))
print("Macaulay duration:", round(macaulay_duration(0.035, 100, 2, 0.04, t), 4))

plt.plot(yields, prices)
plt.xlabel("Yield")
plt.ylabel("Bond price")
plt.title("Bond price sensitivity")
plt.grid(True)
plt.show()
