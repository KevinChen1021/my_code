"""Function module for fx_forward."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def fx_forward(exchange_rate_a, exchange_rate_b, rate_a, rate_b, start_time, end_time, option_type):
    """Compute fx_forward."""
    T = (end_time - start_time).days / 365  # 计算定价日至到期日的期限（年）
    if option_type == '卖出价':
        # 针对远期汇率的卖出价
        forward = exchange_rate_a * (1 + rate_a * T) / (1 + rate_b * T)
    else:
        # 针对远期汇率的买入价
        forward = exchange_rate_b * (1 + rate_a * T) / (1 + rate_b * T)
    return forward
