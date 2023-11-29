"""Module handling GW selection effects"""
import numpy as np

SELECTION_FILE = "/hildafs/projects/phy220048p/share/selection_O3/selection_O3.npz"

def get_beta_for_H0(H0, selection_file=SELECTION_FILE):
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