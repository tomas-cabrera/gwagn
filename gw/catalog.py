import glob2
import pandas as pd

# Dataframe containing information about the catalog skymap conventions
DF_GWTC = pd.DataFrame(
    data=[
        ["GWTC2", "", "_C01:"],
        ["GWTC2.1", "IGWN-GWTC2p1-v2-", "_PEDataRelease_cosmo_reweight_C01:"],
        ["GWTC3", "IGWN-GWTC3p0-v1-", "_PEDataRelease_cosmo_reweight_C01:"],
    ],
    columns=["id", "prefix", "midfix"],
).set_index("id")


def get_skymap_paths(
    gweventname,
    skymap_dir,
    df_gwtc=DF_GWTC,
    waveform="*",
):
    """Function to find skymap paths, given an event and waveform.

    Parameters
    ----------
    gweventname : str
        LIGO/VIRGO Alert ID of event, e.g. GW170817.
    waveform : str, optional
        Desired waveform.
        Default value of "*" returns all waveforms.
    df_gwtcs : _type_, optional
        pd.DataFrame of catalog information, by default DF_GWTCS

    Returns
    -------
    list of str
        Paths to matching skymaps, as a list of strings.
    """

    # Iterate over catalogs
    skymap_paths = []
    for gwtci, gwtc in df_gwtc.iterrows():
        # Assemble glob search string
        globstr = gwtc["dir"] + "/%s%s%s%s.fits" % (
            gwtc["prefix"],
            gweventname,
            gwtc["midfix"],
            waveform,
        )

        # Add paths to list
        skymap_paths += glob2.glob(globstr)
    return skymap_paths


def assign_waveform(
    gweventname,
    skymap_dir,
    cutoff_2to3=191001,
    reference_skymaps=None,
    df_gwtc=DF_GWTC,
    default_waveform="*",
):
    """Assigns GW waveform to eventname.

    Parameters
    ----------
    gweventname : _type_
        _description_
    cutoff_2to3 : int, optional
        _description_, by default 191001
    reference_skymaps : _type_, optional
        _description_, by default None
    skymap_dir : str, optional
        _description_, by default "/hildafs/projects/phy220048p/share/skymaps"
    df_gwtc : _type_, optional
        _description_, by default DF_GWTC
    default_waveform : str, optional
        _description_, by default "*"

    Returns
    -------
    _type_
        _description_
    """
    date = int(gweventname[2:8])
    if date < cutoff_2to3:
        if gweventname.endswith("*"):
            waveform = "SEOBNRv4PHM"
        else:
            waveform = "NRSur7dq4"
    else:
        waveform = "IMRPhenomXPHM"

    # If reference_skymaps defined, use to verify presence of waveform
    if reference_skymaps is None:
        return waveform
    else:
        skymap_paths = get_skymap_paths(
            gweventname, skymap_dir, df_gwtc=df_gwtc, waveform=waveform
        )
        if len(skymap_paths) == 0:
            if default_waveform == "":
                print(
                    "assign_waveform: WARNING: %s skymap not found for %s!  Returning empty string"
                    % (waveform, gweventname)
                )
            elif default_waveform == "*":
                print(gweventname)
                skymap_path = get_skymap_paths(
                    gweventname, skymap_dir, df_gwtc=df_gwtc, waveform=default_waveform
                )[0]
                new_waveform = skymap_path.split("_C01:")[-1].split(".")[0]
                print(
                    "assign_waveform: WARNING: %s skymap not found for %s!  Returning first available waveform from catalog (%s)"
                    % (waveform, gweventname, new_waveform)
                )
                waveform = new_waveform
            else:
                print(
                    "assign_waveform: WARNING: %s skymap not found for %s!  Returning default: %s"
                    % (waveform, gweventname, default_waveform)
                )
                waveform = default_waveform
        return waveform
