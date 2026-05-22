"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def CTD_cost(price1, price2, CF, name):
    cost = price1 - price2 * CF
    cost = pd.DataFrame(cost, index=name, columns=["交割成本"])
    CTD_bond = cost.idxmin()
    CTD_bond = CTD_bond.rename(index={'交割成本': '最廉价交割债券'})
    return cost, CTD_bond
