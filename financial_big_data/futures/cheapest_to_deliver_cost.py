"""Function module for cheapest_to_deliver_cost."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def cheapest_to_deliver_cost(price1, price2, cash_flow, name):
    '''计算国债期货可交割债券的交割成本并找出最便宜可交割债券
    price1: 可交割债券净价（数组）
    price2: 期货价格（数组）
    CF: 转换因子（数组）
    name: 可交割债券名称（数组）'''
    cost = price1 - price2 * cash_flow  # 交割成本
    cost = pd.DataFrame(cost, index=name, columns=["交割成本"])
    CTD_bond = cost.idxmin()  # 最便宜可交割债券
    CTD_bond = CTD_bond.rename(index={'交割成本': '最廉价交割债券'})
    return cost, CTD_bond
