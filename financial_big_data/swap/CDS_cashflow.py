"""Function module for cds_cashflow."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def cds_cashflow(spot_price, coupon_frequency, start_time, end_time, notional_amount, recovery_rate, trader, event):
    """Compute cds_cashflow."""
    # 步骤1：合约到期未发生信用事件时计算现金流
    if event == 'N':
        n = int(start_time * coupon_frequency)  # 计算期间现金流支付的次数
        cashflow = spot_price * start_time * np.ones(n) / coupon_frequency  # 合约期间支付的信用保护费用金额的现金流
        if trader == 'buyer':
            CF = -cashflow  # 针对信用保护买方的期间现金流
        else:
            CF = cashflow  # 针对信用保护卖方的期间现金流
    # 步骤2：合约存续期内发生信用事件且每年支付1次
    else:
        default_pay = (1 - recovery_rate) * notional_amount  # 信用事件发生时买方支付的赔偿性支付
        if coupon_frequency == 1:
            n = int(end_time * coupon_frequency)  # 计算期间现金流支付的次数
            cashflow = (spot_price * end_time * np.ones(n)) / coupon_frequency  # 计算期间的现金流（最后一个元素后面要调整）
            spread_end = (end_time - int(end_time)) * spot_price * notional_amount  # 合约最后一期（信用事件发生日）支付的信用保护费用
            cashflow[-1] = spread_end - default_pay  # 合约最后一期的现金流
            if trader == 'buyer':
                CF = cashflow
            else:
                CF = cashflow
    # 步骤3：合约存续期内发生信用事件且每年支付2次
        else:
            if end_time - int(end_time) < 0.5:  # 信用事件发生在前半年
                n = int(end_time * coupon_frequency)
                cashflow = (spot_price * end_time * np.ones(n)) / coupon_frequency
                spread_end = (end_time - int(end_time)) * spot_price * notional_amount
                cashflow[-1] = spread_end - default_pay
            else:  # 信用事件发生在后半年
                n = (int(end_time) + 1) * coupon_frequency
                cashflow = (spot_price * end_time * np.ones(n)) / coupon_frequency + 0.5 * spot_price * notional_amount
                spread_end = (end_time - int(end_time) - 0.5) * spot_price * notional_amount
                cashflow[-1] = spread_end - default_pay
            if trader == 'buyer':
                CF = -cashflow
            else:
                CF = cashflow
        return CF
