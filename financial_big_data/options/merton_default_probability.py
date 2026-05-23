"""Function module for merton_default_probability."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def merton_default_probability(exchange_rate, debt_value, asset_value, volatility, interest_rate, time_to_maturity):
    """运用默顿模型计算企业违约概率"""
    d1 = (np.log(asset_value/debt_value) + (interest_rate + np.power(volatility, 2)/2)*time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    PD = norm.cdf(-d2)
    return PD
