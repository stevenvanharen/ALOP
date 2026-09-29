"""
synthetic_photometry.py

Determine the colours of a set of stars. Use Vega as a reference to define a magnitude system.
"""


"""
Determine the filter constants using Vega as a reference to define a magnitude system.
"""
from determine_filter_constants import determine_filter_constants, magnitude_weighted
C_U, C_B, C_V = determine_filter_constants()

#print(C_U)

"""
Calculate the colours of all stars in scope
"""
from pathlib import Path
from astropy.table import Table
folder = Path('spectra/')
band_u = [3659-330, 3659+330] #bands in angstrom
band_b = [4582-470, 4582+470]
band_v = [5448-440, 5448+440]
datalist = dict()
for file in folder.iterdir():
    spectrum = Table.read ( file , format = "ascii.csv")   
    m_u = magnitude_weighted(spectrum, band_u) + C_U 
    m_b = magnitude_weighted(spectrum, band_b) + C_B
    m_v = magnitude_weighted(spectrum, band_v) + C_V    
    datalist[file.name] = [m_b - m_v, m_u - m_b]

"""
Plot colours and add markers for main-sequence stars and giants
"""

spectra_list = Table.read ( "spectra_list.csv" , format = "ascii.csv")

from matplotlib import pyplot as plt
fig, ax = plt.subplots()
plt.xlabel("B-V")
plt.ylabel("U-B")
plt.ylim(3, -2)
for star, colours in datalist.items():
    mask = (spectra_list['filename'] == star)
    MKL_class = spectra_list[mask]['type'][0]
    ax.plot(colours[0],colours[1], marker='o' if MKL_class[2]=='V' else 'x')    


plt.savefig('plots\\colours.png', format='png')      
    
