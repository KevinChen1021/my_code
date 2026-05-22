"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def BTM_Nstep(S, K, sigma, r, T, N, types):
    t = T / N
    u = np.exp(sigma * np.sqrt(t))
    d = 1 / u
    p = (np.exp(r * t) - d) / (u - d)
    N_list = range(0, N + 1)
    A = []
    for j in N_list:
        C_Nj = np.maximum(S * np.power(u, j) * np.power(d, N - j) - K, 0) if types == 'call' else np.maximum(
            K - S * np.power(u, j) * np.power(d, N - j), 0)
        Num = factorial(N) / (factorial(j) * factorial(N - j))
        A.append(Num * np.power(p, j) * np.power(1 - p, N - j) * C_Nj)
    option_val = np.exp(-r * T) * sum(A)
    return option_val
