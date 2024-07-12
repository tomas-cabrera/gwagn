###############################################################################

# # Calculate limits of luminosity distance fraction, if specified
# if distance_frac is not None:
#     # Get the upper z-score limit to the fractional region
#     zscore_max = norm.ppf((1 - distance_frac) / 2)
#     # Calculate the luminosity distance limits
#     distance_min = healpix["DISTMU"] - zscore_max * healpix["DISTSIGMA"]
#     distance_max = healpix["DISTMU"] + zscore_max * healpix["DISTSIGMA"]
import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM, z_at_value

import agn.distribution as agn_dist
import agn.flare as agn_flare
import gw.catalog as gw_catalog
import gw.selection as gw_select


class Inference:
    def __init__(
        self,
        theta,
        df_gws,
        df_flares,
        df_assoc,
        cosmo_model=FlatLambdaCDM,
        z_grid=np.linspace(0, 1, 50),
        agn_distribution=agn_dist.QLFHopkins(),
        agn_flare_model=agn_flare.Kimura20(),
    ) -> None:
        # Extract initial params
        self._lamb, self._H0, self._Om0 = theta

        # Carry args forward
        self.df_gws = df_gws
        self.df_flares = df_flares
        self.df_assoc = df_assoc

        # Carry kwargs forward
        self.cosmo_model = cosmo_model
        self.z_grid = z_grid
        self.agn_distribution = agn_distribution
        self.agn_flare_model = agn_flare_model

        # Calculate initial cosmology
        self._cosmo = self.cosmo_model(H0=self._H0, Om0=self._Om0)

    def n_agn_in_gw_areas(self, cosmo, n_dz_grid=50, limiting_magnitude=np.inf):
        n_agn = [
            self.agn_distribution.n_agn_in_dOmega_dz_volume(
                dOmega=gw["area90"],
                dz_grid=np.linspace(
                    z_at_value(
                        cosmo.comoving_distance, gw["distance"] + gw["dist_err_lo"]
                    ),
                    z_at_value(
                        cosmo.comoving_distance, gw["distance"] + gw["dist_err_hi"]
                    ),
                    n_dz_grid,
                ),
                cosmo=cosmo,
                limiting_magnitude=limiting_magnitude,
            )
            for _, gw in self.df_gws
        ]

    def run_mcmc():
        pass


class Lamb(Inference):
    def __init__(self) -> None:
        super().__init__()

    def prepare_static_values(
        self,
        limiting_magnitude,
    ):
        statics = {}

        # Define cosmology
        statics["cosmo"] = self.cosmo_model(H0=self._H0, Om0=self._Om0)

        # Get selection effect beta
        statics["beta"] = gw_select.get_beta_for_H0(self._H0)

        # Calculate expected number of flares per gwevent
        statics["n_flares_detect_expect"] = []

    def ln_likelihood(lamb):
        pass
