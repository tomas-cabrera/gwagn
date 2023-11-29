###############################################################################

# # Calculate limits of luminosity distance fraction, if specified
# if distance_frac is not None:
#     # Get the upper z-score limit to the fractional region
#     zscore_max = norm.ppf((1 - distance_frac) / 2)
#     # Calculate the luminosity distance limits
#     distance_min = healpix["DISTMU"] - zscore_max * healpix["DISTSIGMA"]
#     distance_max = healpix["DISTMU"] + zscore_max * healpix["DISTSIGMA"]
