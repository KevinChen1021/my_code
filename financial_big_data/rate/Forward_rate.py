"""Function module for forward_rate."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def forward_rate(R1, R2, end_time, T2):
    """Compute forward_rate."""
    forward = R2 + (R2 - R1) * end_time / (T2 - end_time)  # 计算远期利率的表达式
    return forward
