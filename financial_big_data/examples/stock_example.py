from pathlib import Path
import sys

PROJECT_PARENT = Path(__file__).resolve().parents[2]
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))

import numpy as np
import matplotlib.pyplot as plt

from financial_big_data import set_plot_style
from financial_big_data.stock import value_CGM, SR

set_plot_style()

growth = np.linspace(0.01, 0.08, 30)
values = [value_CGM(D=1.2, g=g, r=0.10) for g in growth]
print("Sharpe ratio:", round(SR(Rp=0.12, Rf=0.03, Vp=0.18), 4))

plt.plot(growth, values)
plt.xlabel("Dividend growth")
plt.ylabel("Intrinsic value")
plt.title("Constant growth stock valuation")
plt.grid(True)
plt.show()
