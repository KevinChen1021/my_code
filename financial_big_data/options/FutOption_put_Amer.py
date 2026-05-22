"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def FutOption_put_Amer(F, K, sigma, r, T, N):
    """
    N步二叉树计算美式看跌期货期权价格
    参数同FutOption_call_Amer
    """
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (1 - d) / (u - d)
    put_matrix = np.zeros((N+1, N+1))

    # 到期节点价值
    N_list = np.arange(0, N+1)
    F_end = F * np.power(u, N - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(K - F_end, 0)

    # 倒推计算非到期节点价值
    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i+1)
        for j in j_list:
            Fi = F * np.power(u, i - j) * np.power(d, j)
            put_strike = np.maximum(K - Fi, 0)
            put_nostrike = np.exp(-r*t) * (p*put_matrix[i+1, j+1] + (1-p)*put_matrix[i+1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)
    return put_matrix[0, 0]
