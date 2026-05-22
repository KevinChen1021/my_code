"""Function-level module generated from the original financial_big_data sources."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def Forward_rate(R1, R2, T1, T2):
    forward = R2 + (R2 - R1) * T1 / (T2 - T1)
    return forward
