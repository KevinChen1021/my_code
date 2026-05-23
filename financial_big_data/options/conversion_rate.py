"""Function module for conversion_rate."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def conversion_rate(market_rate, coupon_frequency):
    """复利利率转连续复利利率"""
    r = coupon_frequency * np.log(1+market_rate/coupon_frequency)
    return r
