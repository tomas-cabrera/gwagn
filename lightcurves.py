"""Module with some useful lightcurve utilities"""
import numpy as np


def gaussrise_expdecay(t, y_baseline, y_peak, t_peak, t_rise, t_decay):
    """Gaussian rise - exponential decay model.

    Parameters
    ----------
    t : _type_
        _description_
    r0 : _type_
        _description_
    A : _type_
        _description_
    t0 : _type_
        _description_
    tg : _type_
        _description_
    te : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    # Gaussian rise
    if t <= t_peak:
        return y_baseline + y_peak * np.exp(-((t - t_peak) ** 2) / (2 * t_rise**2))
    # Exponential decay
    return y_baseline + y_peak * np.exp(-(t - t_peak) / t_decay)
