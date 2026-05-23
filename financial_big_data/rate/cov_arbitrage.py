"""Function module for cov_arbitrage."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def cov_arbitrage(exchange_rate_a, exchange_rate_b, forward_rate_a, forward_rate_b, notional_a, notional_b, rate_a, rate_b, time_to_maturity, amount):
    """Compute cov_arbitrage."""
    if forward_rate_b * (1 + rate_b * time_to_maturity) / (exchange_rate_a * (1 + rate_a * time_to_maturity)) > 1:
        # 期初借入A货币、期末偿还A货币的套利路径成功
        profit = (forward_rate_b * (1 + rate_b * time_to_maturity) / exchange_rate_a - (1 + rate_a * time_to_maturity)) * notional_a
        sequence = [
            '套利路径如下',
            '第1步，初始借入的货币：', amount,
            '第2步，按即期汇率兑换后并投资的货币：', amount,
            '第3步，在投资结束时按远期汇率兑换后的货币：', amount,
            '第4步，偿还初始借入的本金和利息'
        ]
    elif exchange_rate_b * (1 + rate_a * time_to_maturity) / (forward_rate_a * (1 + rate_b * time_to_maturity)) > 1:
        # 期初借入B货币、期末偿还B货币的套利路径成功
        profit = (exchange_rate_b * (1 + rate_a * time_to_maturity) / forward_rate_a - (1 + rate_b * time_to_maturity)) * notional_b
        sequence = [
            '套利路径如下',
            '第1步，初始借入的货币：', amount,
            '第2步，按即期汇率兑换后并投资的货币：', amount,
            '第3步，在投资结束时按远期汇率兑换后的货币：', amount,
            '第4步，偿还初始借入的本金和利息'
        ]
    else:
        # 不存在套利机会
        profit = 'Na'
        sequence = '套利机会不存在'
    return [profit, sequence]
