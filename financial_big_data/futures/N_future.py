"""Function module for n_future."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.stats import norm


def n_future(holding_period, quantity_a, quantity_f):
    """Compute n_future."""
    N = holding_period * quantity_a / quantity_f
    return N
