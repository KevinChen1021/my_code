"""Function module for forward_rate."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def forward_rate(R1, R2, end_time, T2):
    """
    计算远期利率
    R1: 对应期限T1的零息利率
    R2: 对应期限T2的零息利率
    T1: R1的期限（年）
    T2: R2的期限（年）
    """
    forward_rate = R2 + (R2 - R1) * end_time / (T2 - end_time)
    return forward_rate
