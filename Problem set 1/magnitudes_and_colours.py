from astropy.table import Table
from astropy import units as u
from astropy.visualization import quantity_support
from matplotlib import pyplot as plt
import numpy as np
import math

dataset = list()
types = ['']
stars = ['vega']
# vega dataset is in nm on x-axis
# for magnitude use Carrol and Ostlie 3.31 
dataset.append(Table.read ( "vega_fnu.csv" , format = "ascii.csv"))

def magnitude(spectrum, band):
    interpolated_spectrum = np.interp(np.linspace(band[0], band[1], 100), spectrum['wavelength'], spectrum['flux'])
    delta_lambda = (band[1] - band[0])/100
    return -2.5 * math.log(sum(interpolated_spectrum)*delta_lambda, 10)

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
m_u = magnitude_weighted(dataset[0], [333, 399])
m_b = magnitude_weighted(dataset[0], [411, 505])
m_v = magnitude_weighted(dataset[0], [500, 588])
print(m_u)
print(m_b)
print(m_v)

C_u = 0 - m_u
C_b = 0 - m_b
C_v = 0 - m_v