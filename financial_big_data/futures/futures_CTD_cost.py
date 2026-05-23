"""Function module for cheapest_to_deliver_cost."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def cheapest_to_deliver_cost(price1, price2, cash_flow, name):
    """Compute cheapest_to_deliver_cost."""
    cost = price1 - price2 * cash_flow
    cost = pd.DataFrame(cost, index=name, columns=["交割成本"])
    CTD_bond = cost.idxmin()
    CTD_bond = CTD_bond.rename(index={'交割成本': '最廉价交割债券'})
    return cost, CTD_bond
