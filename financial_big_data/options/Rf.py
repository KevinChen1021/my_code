"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def Rf(R1, R2, T1, T2):
    """
    计算远期利率
    R1: 对应期限T1的零息利率
    R2: 对应期限T2的零息利率
    T1: R1的期限（年）
    T2: R2的期限（年）
    """
    forward_rate = R2 + (R2 - R1) * T1 / (T2 - T1)
    return forward_rate
