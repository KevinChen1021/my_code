"""Function module for accrued_interest."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def accrued_interest(par_value, cost, coupon_frequency, start_time, end_time, third_time, fourth_time, rule):
    """Compute accrued_interest."""
    d1 = (end_time - start_time).days  # 非参考期间天数
    if rule == "actual/actual":
        d2 = (fourth_time - third_time).days  # 参考期间天数
        interest = (d1 / d2) * par_value * cost / coupon_frequency
    elif rule == "actual/360":
        interest = (d1 / 360) * par_value * cost
    else:
        interest = (d1 / 365) * par_value * cost
    return interest
