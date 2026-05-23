"""Function module for american_futures_put_amer."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def american_futures_put_amer(forward_price, strike_price, volatility, interest_rate, time_to_maturity, steps):
    """
    N步二叉树计算美式看跌期货期权价格
    参数同FutOption_call_Amer
    """
    t = time_to_maturity / steps
    u = np.exp(volatility * np.sqrt(t))
    d = 1 / u
    p = (1 - d) / (u - d)
    put_matrix = np.zeros((steps+1, steps+1))

    # 到期节点价值
    N_list = np.arange(0, steps+1)
    F_end = forward_price * np.power(u, steps - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(strike_price - F_end, 0)

    # 倒推计算非到期节点价值
    i_list = list(range(0, steps))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i+1)
        for j in j_list:
            Fi = forward_price * np.power(u, i - j) * np.power(d, j)
            put_strike = np.maximum(strike_price - Fi, 0)
            put_nostrike = np.exp(-interest_rate*t) * (p*put_matrix[i+1, j+1] + (1-p)*put_matrix[i+1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)
    return put_matrix[0, 0]
