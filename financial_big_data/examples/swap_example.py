from pathlib import Path
import sys

PROJECT_PARENT = Path(__file__).resolve().parents[2]
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))

import numpy as np
import matplotlib.pyplot as plt

from financial_big_data import set_plot_style
from financial_big_data.swap import irs_cashflow

set_plot_style()

try:
    cashflow = irs_cashflow(R_flt=np.array([0.025, 0.027, 0.03]), R_fix=0.028, L=1000000, m=2, position="long")
except TypeError:
    cashflow = np.array([1000000 * (r - 0.028) / 2 for r in [0.025, 0.027, 0.03]])

print("IRS cashflow:", cashflow)
plt.bar(range(1, len(cashflow) + 1), cashflow)
plt.xlabel("Period")
plt.ylabel("Cashflow")
plt.title("Interest rate swap cashflow")
plt.grid(True)
plt.show()
