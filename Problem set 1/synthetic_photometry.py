"""
synthetic_photometry.py

Determine the colours of a set of stars. Use Vega as a reference to define a magnitude system.
"""

# filter bands in angstrom
band_u = [3659-330, 3659+330] 
band_b = [4582-470, 4582+470]
band_v = [5448-440, 5448+440]


"""
Determine the filter constants using Vega as a reference to define a magnitude system.
"""
from determine_filter_constants import determine_filter_constants, magnitude_weighted
C_U, C_B, C_V = determine_filter_constants(band_u, band_b, band_v)

#print(C_U)

"""
Calculate the colours of all stars in scope
"""
from pathlib import Path
from astropy.table import Table
folder = Path('spectra/')
datalist = dict()
for file in folder.iterdir():
    spectrum = Table.read ( file , format = "ascii.csv")   
    m_u = magnitude_weighted(spectrum, band_u) + C_U 
    m_b = magnitude_weighted(spectrum, band_b) + C_B
    m_v = magnitude_weighted(spectrum, band_v) + C_V    
    datalist[file.name] = [m_b - m_v, m_u - m_b]

"""
Plot colours and add markers for main-sequence stars and giants
 O5, B0, A0, F0, G0, K0, and M0
"""
markers = {'O5':'r', 'B0':'b', 'A0':'g', 'F0':'y', 'G0':'olivedrab', 'K0':'c', 'M0':'m'}

spectra_list = Table.read ( "spectra_list.csv" , format = "ascii.csv")

from matplotlib import pyplot as plt
fig, ax = plt.subplots()
plt.xlabel("B-V")
plt.ylabel("U-B")
plt.ylim(3, -2)
for star, colours in datalist.items():
    mask = (spectra_list['filename'] == star)
    type = spectra_list[mask]['type'][0][0:2]    
    MKL_class = spectra_list[mask]['type'][0][2]
    ax.plot(colours[0],colours[1], marker='.' if MKL_class=='V' else 'x', color=markers.get(type,'k'))    

  

"""
Add a line for blackbody colours
"""

bb_datalist = dict()
from black_body import spectrum
for T in range(2000,31000,1000):
    bb_spectrum = spectrum(T)
    m_u = magnitude_weighted(bb_spectrum, band_u) + C_U 
    m_b = magnitude_weighted(bb_spectrum, band_b) + C_B
    m_v = magnitude_weighted(bb_spectrum, band_v) + C_V    
    bb_datalist[T] = [m_b - m_v, m_u - m_b]

line = bb_datalist.values()
bv, ub = zip(*list(line))
ax.plot(bv,ub, '-', color='black')
# fig2, ax2 = plt.subplots()
# ax2.plot(bb['wavelength'],bb['flux'])
# plt.savefig('plots\\bb.png', format='png')  
# 
plt.savefig('plots\\colours.png', format='png')    
  
    
