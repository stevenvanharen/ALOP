from astropy.table import Table
import astropy.units as u
import numpy as np
import math

# vega dataset
vega_spectrum = Table.read ( "vega_fnu.csv" , format = "ascii.csv")
# for this spectrum, the wavelength is in nm, we convert to angstrom
vega_spectrum['wavelength'].unit = 'nm'
vega_spectrum['wavelength'].convert_unit_to('angstrom')
# for this spectrum, the flux density is given in erg cm^-2 s^-1 Hz^-1, we convert to erg cm^-2 s^-2 angstrom^-1
vega_spectrum['flux'].unit = 'Jy'
vega_spectrum['flux'].convert_unit_to(
    u.erg / (u.s * u.cm**2 * u.AA), 
    equivalencies=u.spectral_density(vega_spectrum['wavelength'].quantity)
)

# or use weighted magnitude as in (1) of PS1 description
def magnitude(spectrum, band):    
    delta_lambda = (band[1] - band[0])/100
    discrete_lambdas = np.linspace(band[0]+delta_lambda/2, band[1]-delta_lambda/2, 100)    
    integral = 0       
    for wavelength in discrete_lambdas:        
        flux = np.interp(wavelength, spectrum['wavelength'], spectrum['flux'])
        integral+=flux * delta_lambda
    return -2.5 * math.log(integral, 10)


# or use weighted magnitude as in (1) of PS1 description
def magnitude_weighted(spectrum, band):    
    delta_lambda = (band[1] - band[0])/100
    discrete_lambdas = np.linspace(band[0]+delta_lambda/2, band[1]-delta_lambda/2, 100)    
    integral = 0  
    integral_denom = 0     
    for wavelength in discrete_lambdas:        
        flux = np.interp(wavelength, spectrum['wavelength'], spectrum['flux'])
        integral+=flux * delta_lambda * wavelength
        integral_denom = delta_lambda * wavelength
    return -2.5 * math.log(integral/integral_denom, 10)


#calculate m_u, m_b, m_v for vega
def determine_filter_constants(band_u, band_b, band_v):
    m_u = magnitude_weighted(vega_spectrum, band_u) # bands in angstrom
    m_b = magnitude_weighted(vega_spectrum, band_b)
    m_v = magnitude_weighted(vega_spectrum, band_v)

    C_U = 0 - m_u
    C_B = 0 - m_b
    C_V = 0 - m_v
    return C_U, C_B, C_V