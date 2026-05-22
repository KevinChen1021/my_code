from pathlib import Path
import sys

PROJECT_PARENT = Path(__file__).resolve().parents[2]
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))

import numpy as np
import matplotlib.pyplot as plt

from financial_big_data import set_plot_style
from financial_big_data.rate import Forward_rate

set_plot_style()

terms = np.array([1, 2, 3, 4, 5])
zero_rates = np.array([0.02, 0.024, 0.027, 0.03, 0.032])
try:
    forwards = Forward_rate(zero_rates[:-1], zero_rates[1:], terms[:-1], terms[1:])
except TypeError:
    forwards = np.diff(zero_rates * terms) / np.diff(terms)

print("Forward rates:", forwards)
plt.plot(terms[1:], forwards, marker="o")
plt.xlabel("Term")
plt.ylabel("Forward rate")
plt.title("Forward rate curve")
plt.grid(True)
plt.show()
