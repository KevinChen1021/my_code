"""Function module for exchange."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def exchange(par_value, steps, exchange_rate_a, exchange_rate_b, currency_a, currency_b, direction):
    """Compute exchange."""
    if direction == 'A to B':
        # 企业向银行用A货币兑换为B货币
        if steps == 'Na':
            # 计算汇兑后的金额
            value = par_value / exchange_rate_a
            currency = currency_b
        else:
            # 计算汇兑前的金额
            value = steps * exchange_rate_a
            currency = currency_a
    else:
        # 企业向银行用B货币兑换为A货币
        if steps == 'Na':
            # 计算汇兑后的金额
            value = par_value * exchange_rate_b
            currency = currency_a
        else:
            # 计算汇兑前的金额
            value = steps / exchange_rate_b
            currency = currency_b
    return [value, currency]
