from astropy.table import Table
import numpy as np
import math

# vega dataset is in nm on x-axis
# for magnitude use Carrol and Ostlie 3.31 
vega_spectrum = Table.read ( "vega_fnu.csv" , format = "ascii.csv")

# or use weighted magnitude as in (1) of PS1 description
def magnitude_weighted(spectrum, band):
    interpolated_spectrum = np.interp(np.linspace(band[0], band[1], 100), spectrum['wavelength'], spectrum['flux'])
    delta_lambda = (band[1] - band[0])/100
    integral = 0
    integral_denominator = 0
    pos = band[0]
    for flux in interpolated_spectrum:
        integral+=flux * (pos + delta_lambda/2) * delta_lambda
        integral_denominator+=(pos + delta_lambda/2) * delta_lambda
        pos+=delta_lambda
    return -2.5 * math.log(integral/integral_denominator, 10)


#calculate m_u, m_b, m_v for vega
def determine_filter_constants():
    m_u = magnitude_weighted(vega_spectrum, [333, 399]) # bands in nm
    m_b = magnitude_weighted(vega_spectrum, [411, 505])
    m_v = magnitude_weighted(vega_spectrum, [500, 588])

    C_U = 0 - m_u
    C_B = 0 - m_b
    C_V = 0 - m_v
    return C_U, C_B, C_V