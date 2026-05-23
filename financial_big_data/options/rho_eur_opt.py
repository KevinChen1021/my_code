"""Function module for rho_eur_opt."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def rho_eur_opt(spot_price, strike_price, volatility, interest_rate, time_to_maturity, option_type):
    '''计算欧式期权Rho的函数'''
    d2 = (log(spot_price / strike_price) + (interest_rate + power(volatility, 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
    if option_type == 'call':
        rho = strike_price * time_to_maturity * exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
    else:
        rho = -strike_price * time_to_maturity * exp(-interest_rate * time_to_maturity) * norm.cdf(-d2)
    return rho
