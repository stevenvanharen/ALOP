import math
from astropy.table import Table

k = 1.3806504e-23
h = 6.62606896e-34
c = 2.99792458e8

def planck(T, wavelength):
    return (2*h*math.pow(c,2)/math.pow(wavelength,5))/(math.exp((h*c)/(wavelength * k * T)) - 1)

def spectrum(T):
    table = Table(names=('wavelength','flux'),dtype=('f8','f8'))
    #we need the spectrum between 3000 and 6000 angstrom
    for wavelength in range(3000,6000, 10):
        b_lambda = planck(T, wavelength/1e10)/1e9 # unit W m-2 nm -1 sr -1 # TODO: convert to erg m-2 nm -1 A
        table.add_row((wavelength, b_lambda))

    return table