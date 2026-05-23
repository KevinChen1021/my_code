"""Function module for price_futures."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def price_futures(spot_price, interest_rate, yield_rate, up_factor, carry_cost, time_to_maturity):
    '''计算期货理论价格的函数
    S: 现货价格
    r: 无风险利率（连续复利）
    y: 便利收益率（连续复利）
    u: 租借利率（期间收益率，连续复利）
    c: 仓储费用
    T: 剩余期限（年）'''
    from numpy import exp
    # 期货理论价格公式：S * exp((r - y + u) * T) + c
    price = spot_price * exp((interest_rate - yield_rate + up_factor) * time_to_maturity) + carry_cost
    return price
