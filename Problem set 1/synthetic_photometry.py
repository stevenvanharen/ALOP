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
#print(C_B)
#print(C_V)

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
plt.ylim(3, -1.5)
#plt.yticks(range(3, -2, 1)) 
for star, colours in datalist.items():
    mask = (spectra_list['filename'] == star)
    type = spectra_list[mask]['type'][0][0:2]
    #V = main sequence, I = giant    
    MKL_class = spectra_list[mask]['type'][0][2]
    zorder = 2
    if type in markers:
        zorder = 3
    ax.plot(colours[0],colours[1], marker='.' if MKL_class=='V' else 'x', color=markers.get(type,'k'), zorder=zorder)    

  

"""
Add a line for blackbody colours
"""

bb_datalist = dict()
from black_body import spectrum
for T in range(2000,31000,1000):
    bb_spectrum = spectrum(T, range(3000,6000, 10))
    m_u = magnitude_weighted(bb_spectrum, band_u) + C_U 
    m_b = magnitude_weighted(bb_spectrum, band_b) + C_B
    m_v = magnitude_weighted(bb_spectrum, band_v) + C_V    
    bb_datalist[T] = [m_b - m_v, m_u - m_b]

line_bb = bb_datalist.values()
bv, ub = zip(*list(line_bb))
ax.plot(bv,ub, '-', color='black')
# fig2, ax2 = plt.subplots()
# ax2.plot(bb['wavelength'],bb['flux'])
# plt.savefig('plots\\bb.png', format='png')  
# 

from matplotlib.lines import Line2D
# 2. Define custom proxy lines for the legend
legend_elements = [Line2D([0], [0], color='black', lw=2, marker='', label='Blackbody')]
for type, colour in markers.items():
    legend_elements.append(Line2D([0], [0], color=colour, lw=0, marker='.', label=type))

plt.legend(handles=legend_elements)

 

def plot(star, bb, type, star_name, styles):    
    fig, ax = plt.subplots()    
    plt.xlabel("Wavelength (Å)")
    #plt.ylabel("Flux (erg $\mathregular{cm^{-2}}$ $\mathregular{s^{-1}}$ $\mathregular{\AA^{-1}}$)") # erg/cm2/s/A?, change compared to: https://brightspace.universiteitleiden.nl/d2l/le/lessons/494809/topics/4063078
    plt.xlim(3000, 9000)
    
    #find row for 3000
    #find row for 9000    
    div = star['flux']/bb['flux']
    table = Table([star['wavelength'], div],names=('wavelength','flux'))
    mask = (table['wavelength'] >= 3000) & (table['wavelength'] <= 9000)    
    ax.plot(table[mask]['wavelength'],table[mask]['flux'], styles[0] , label=star_name + ", type: " + type, linewidth=2.0)
    #ax.plot(bb['wavelength'],bb['flux'], styles[0] , label=stars[0] + ", type: " + type, linewidth=2.0)
    ax.legend()    
    #plt.savefig('plots\\plots.eps', format='eps')
    plt.savefig('plots\\plots_bb'+star_name+'div.png', format='png')
    plt.close()

    fig, ax = plt.subplots()    
    plt.xlabel("Wavelength (Å)")
    #plt.ylabel("Flux (erg $\mathregular{cm^{-2}}$ $\mathregular{s^{-1}}$ $\mathregular{\AA^{-1}}$)") # erg/cm2/s/A?, change compared to: https://brightspace.universiteitleiden.nl/d2l/le/lessons/494809/topics/4063078
    plt.xlim(3000, 9000)
    mask = (star['wavelength'] >= 3000) & (star['wavelength'] <= 9000)
    ax.plot(star[mask]['wavelength'],star[mask]['flux'], styles[0] , label=star_name + ", type: " + type, linewidth=2.0)
    ax.plot(bb['wavelength'],bb['flux'], styles[0] , label=star_name + ", type: " + type, linewidth=2.0)
    ax.legend()    
    #plt.savefig('plots\\plots.eps', format='eps')
    plt.savefig('plots\\plots_bb'+star_name+'.png', format='png')
    plt.close()

def plot_combined(divs, styles):    
    fig, ax = plt.subplots()    
    plt.xlabel("Wavelength (Å)")
    plt.ylabel("Flux ratio") # erg/cm2/s/A?, change compared to: https://brightspace.universiteitleiden.nl/d2l/le/lessons/494809/topics/4063078
    plt.xlim(3000, 9000)
    
    #find row for 3000
    #find row for 9000
    for type, spectra in divs.items():
        star = spectra[0]
        bb = spectra[1]    
        div = star['flux']/bb['flux']
        table = Table([star['wavelength'], div],names=('wavelength','flux'))
        mask = (table['wavelength'] >= 3000) & (table['wavelength'] <= 9000)    
        ax.plot(table[mask]['wavelength'],table[mask]['flux'], styles[0] , label=type, linewidth=1.0)        
    ax.axvspan(band_u[0], band_u[1], color='violet', alpha=0.3, label='U band')
    ax.axvspan(band_b[0], band_b[1], color='blue', alpha=0.3, label='B band')
    ax.axvspan(band_v[0], band_v[1], color='yellow', alpha=0.3, label='V band')
    ax.legend()    
    plt.savefig('plots\\plots_bb_divs.eps', format='eps')
    plt.savefig('plots\\plots_bb_divs.png', format='png')
    plt.close()    

#problem 4: B0, A0, F0 and G0
bv_x = list(bv)
bv_x.reverse()
T_y = list(bb_datalist.keys())
T_y.reverse()
folder = 'spectra\\'
import numpy as np
selected_stars = {"Ab71f.csv":"F0I", "Ab24f.csv": "G0V", "Bb14.csv": "A0V", "Ab66f.csv": "B0I"}
divs = dict()
styles = ['-']
for selected_star, type in selected_stars.items():
    BminusV = datalist[selected_star][0]
    T_bb = np.interp(BminusV, bv_x ,T_y)
    print(BminusV)
    print(T_bb)
    star_spectrum = Table.read ( folder+selected_star , format = "ascii.csv")
    bb_spectrum = spectrum(T_bb, star_spectrum['wavelength'])
    scaling =  star_spectrum[(star_spectrum['wavelength'] == 6000)]['flux']/bb_spectrum[(bb_spectrum['wavelength'] == 6000)]['flux']
    bb_spectrum['flux'] *= scaling
    plot(star_spectrum,bb_spectrum,selected_star, type,styles)
    divs[type] = [star_spectrum,bb_spectrum]

plot_combined(divs, styles)
#TODO: add vertical lines
vertical_lines = [0.341,0.542,-0.030,0.425,-0.013]
for vertrical_line in vertical_lines:
    ax.vlines(vertrical_line,-1.5,3, linestyles='--')
plt.savefig('plots\\colours.png', format='png')
plt.savefig('plots\\colours.eps', format='eps')   
  
    
