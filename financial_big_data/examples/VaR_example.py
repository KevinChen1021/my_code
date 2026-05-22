from pathlib import Path
import sys

PROJECT_PARENT = Path(__file__).resolve().parents[2]
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))

import numpy as np
import matplotlib.pyplot as plt

from financial_big_data import set_plot_style
from financial_big_data.VaR import VaR_VCM

set_plot_style()

confidence = np.linspace(0.90, 0.99, 20)
var_values = [VaR_VCM(Value=1_000_000, Rp=0.0002, Vp=0.015, X=x, N=1) for x in confidence]
print("95% one-day VaR:", round(VaR_VCM(1_000_000, 0.0002, 0.015, 0.95, 1), 2))

plt.plot(confidence, var_values)
plt.xlabel("Confidence level")
plt.ylabel("VaR")
plt.title("Variance-covariance VaR")
plt.grid(True)
plt.show()
