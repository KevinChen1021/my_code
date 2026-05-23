"""Function module for floorlet."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def floorlet(notional_amount, rate, forward_price, strike_rate, volatility, start_time, end_time):
    """
    计算利率下限单元价值
    参数同caplet
    """
    d1 = (np.log(forward_price/strike_rate) + np.power(volatility, 2) * start_time/2) / (volatility * np.sqrt(start_time))
    d2 = d1 - volatility * np.sqrt(start_time)
    tau = end_time - start_time
    value = notional_amount * tau * np.exp(-rate * end_time) * (strike_rate * norm.cdf(-d2) - forward_price * norm.cdf(-d1))
    return value
