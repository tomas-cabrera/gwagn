"""Module handling GW selection effects"""
import numpy as np


def get_beta_for_H0(selection_file, H0):
    """Get selection function beta for given H0(s).

    Parameters
    ----------
    selection_file : _type_
        _description_
    H0 : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    sf = np.load(selection_file)
    beta = np.interp(H0, sf["H0grid"], sf["beta"])
    return beta