"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm
import scipy.optimize as so
import scipy.stats as st


def Rc(Rm, m):
    """复利利率转连续复利利率"""
    r = m * np.log(1+Rm/m)
    return r
