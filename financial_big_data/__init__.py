"""Python financial toolkit for bonds, stocks, derivatives, rates, swaps and VaR."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

__version__ = "0.1.0"
__author__ = "Kevin Chen"


def set_plot_style():
    """Set matplotlib defaults for Chinese labels and normal minus signs."""
    plt.rcParams["font.sans-serif"] = ["SimSun", "FangSong", "Microsoft YaHei", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False


from . import bond, futures, options, rate, stock, swap, VaR

__all__ = [
    "np",
    "pd",
    "plt",
    "set_plot_style",
    "bond",
    "futures",
    "options",
    "rate",
    "stock",
    "swap",
    "VaR",
]

_seen_exports = set(__all__)
_duplicate_exports = set()
for _module in (bond, futures, options, rate, stock, swap, VaR):
    for _name in getattr(_module, "__all__", []):
        if _name in _seen_exports:
            _duplicate_exports.add(_name)
            globals().pop(_name, None)
            if _name in __all__:
                __all__.remove(_name)
            continue
        globals()[_name] = getattr(_module, _name)
        __all__.append(_name)
        _seen_exports.add(_name)

del _module, _name, _seen_exports, _duplicate_exports
