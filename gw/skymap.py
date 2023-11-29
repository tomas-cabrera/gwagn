"""Module handling GW skymaps"""
import astropy_healpix as ah
import ligo.skymap.moc as lsm_moc
import numpy as np


def lonlat_to_uniq(lon, lat, sm_uniqs, warn=True, level_min=0, level_max=12):
    """Finds the HEALPix that contains (lon, lat) from the list of UNIQ indices.
    Does this by iterating over nside until a matching UNIQ is found.

    Parameters
    ----------
    lon : _type_
        _description_
    lat : _type_
        _description_
    sm_uniqs : _type_
        _description_
    warn : bool, optional
        _description_, by default True
    level_min : int, optional
        _description_, by default 0
    level_max : int, optional
        _description_, by default 12

    Returns
    -------
    _type_
        _description_
    """

    # Check if there's full-sky coverage (in steradians)
    accuracy = 6
    if warn:
        area = 0.0
        for uniq in sm_uniqs:
            area += lsm_moc.uniq2pixarea(uniq)
        if round(area, accuracy) != round(4 * np.pi, accuracy):
            print(
                f"WARNING: uniqs do not have full-sky coverage! (area = {area} != 4pi str)"
            )

    # Make array of matching uniqs from level_min to level_max;
    # transpose so masked indexing returns things in the right order
    lonlat_uniqs = np.array(
        [
            ah.level_ipix_to_uniq(
                l, ah.lonlat_to_healpix(lon, lat, ah.level_to_nside(l), order="nested")
            )
            for l in np.arange(level_min, level_max)
        ]
    ).transpose()
    # Masked index by lonlat_uniqs found in sm_uniqs, and return
    mask = np.isin(lonlat_uniqs, sm_uniqs)
    return_uniqs = lonlat_uniqs[mask]
    return return_uniqs

def get_hpxs_from_coords(lon, lat, skymap):
    """Crossmatches lon+lat with a multi-order skymap
    to find the matching HEALPixs.

    Parameters
    ----------
    lon : _type_
        _description_
    lat : _type_
        _description_
    skymap : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    # Get uniq indices from skymap
    uniqs = lonlat_to_uniq(lon, lat, skymap["UNIQ"])
    # Get HEALPixs, by finding indices of uniqs
    sorter = np.argsort(skymap["UNIQ"])
    uniq_inds = sorter[np.searchsorted(skymap["UNIQ"], uniqs, sorter=sorter)]
    hpxs = skymap[uniq_inds]
    return hpxs
