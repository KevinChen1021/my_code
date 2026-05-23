"""Function module for stack_roll."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def stack_roll(F_open, F_close, par_value, steps, position):
    """Compute stack_roll."""
    if position == 'long':
        # 多头套期保值，计算每次期货合约移仓的盈亏
        profit_list = (F_close - F_open) * par_value * steps
    else:
        # 空头套期保值，计算每次期货合约移仓的盈亏
        profit_list = (F_open - F_close) * par_value * steps
    # 计算套期保值期间期货合约的盈亏合计
    profit_sum = np.sum(profit_list)
    return profit_sum
