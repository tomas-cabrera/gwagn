"""Module handling AGN flare modeling"""
import pandas as pd


class AGNFlareModel:
    """A class to handle AGN flare models

    Returns
    -------
    _type_
        _description_
    """
    def __init__(self) -> None:
        pass

class Kimura20FlareModel(AGNFlareModel):
    def __init__(self) -> None:
        super().__init__()
        # Structure function parameters from Kimura+20 S2.1,
        self.sf_params = pd.DataFrame(
            [
                {"band": "g", "SF0": 0.210, "SF0err": 0.003, "dt0": 100, "bt": 0.411, "bterr": 0.13},
                {"band": "r", "SF0": 0.160, "SF0err": 0.002, "dt0": 100, "bt": 0.440, "bterr": 0.12},
                {"band": "i", "SF0": 0.133, "SF0err": 0.001, "dt0": 100, "bt": 0.511, "bterr": 0.10},
                {"band": "z", "SF0": 0.097, "SF0err": 0.001, "dt0": 100, "bt": 0.492, "bterr": 0.13},
            ]
        ).set_index("band")
