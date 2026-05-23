"""Function module for vega_eur_opt."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def vega_eur_opt(spot_price, strike_price, volatility, interest_rate, time_to_maturity):
    '''计算欧式期权Vega的函数'''
    d1 = (log(spot_price / strike_price) + (interest_rate + power(volatility, 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
    vega = spot_price * sqrt(time_to_maturity) * exp(-power(d1, 2) / 2) / sqrt(2 * pi)
    return vega
