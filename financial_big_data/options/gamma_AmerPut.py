"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def gamma_AmerPut(S, K, sigma, r, T, N):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    put_matrix = np.zeros((N + 1, N + 1))
    N_list = np.arange(0, N + 1)
    S_end = S * np.power(u, N - N_list) * np.power(d, N_list)
    put_matrix[:, -1] = np.maximum(K - S_end, 0)

    i_list = list(range(0, N))
    i_list.reverse()
    for i in i_list:
        j_list = np.arange(i + 1)
        for j in j_list:
            Si = S * np.power(u, i - j) * np.power(d, j)
            put_strike = np.maximum(K - Si, 0)
            put_nostrike = np.exp(-r * t) * (p * put_matrix[i + 1, j + 1] + (1 - p) * put_matrix[i + 1, j])
            put_matrix[i, j] = np.maximum(put_strike, put_nostrike)

    Delta1 = (put_matrix[0, 2] - put_matrix[1, 2]) / (S * np.power(u, 2) - S)
    Delta2 = (put_matrix[1, 2] - put_matrix[2, 2]) / (S - S * np.power(d, 2))
    Gamma = (Delta1 - Delta2) / (S * np.power(u, 2) - S * np.power(d, 2))
    return Gamma
