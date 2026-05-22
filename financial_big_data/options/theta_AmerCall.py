"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def theta_AmerCall(S, K, sigma, r, T, N):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    call_matrix = np.zeros((N + 1, N + 1))
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    call_matrix[:, -1] = np.maximum(S_end - K, 0)

    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)
            call_strike = np.maximum(Si - K, 0)
            call_nostrike = np.exp(-r * t) * (p * call_matrix[i + 1, j + 1] + (1 - p) * call_matrix[i + 1, j])
            call_matrix[i, j] = np.maximum(call_strike, call_nostrike)

    Theta = (call_matrix[1, 2] - call_matrix[0, 0]) / (2 * t)
    return Theta
