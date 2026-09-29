from astropy.table import Table
from astropy import units as u
from astropy.visualization import quantity_support
from matplotlib import pyplot as plt
quantity_support()

def plotCSV(dataset, types, stars, styles):    
    fig, ax = plt.subplots()
    #plt.title("Spectra")
    plt.xlabel("Wavelength (Å)")
    #plt.ylabel("Flux (W $\mathregular{m^-2}$ $\mathregular{nm^-1}$)") #TODO: check unit, per nm or angstrom?
    plt.ylabel("Flux (W $\mathregular{m^{-2}}$ $\mathregular{nm^{-1}}$)") # erg/cm2/s/A?, change compared to: https://brightspace.universiteitleiden.nl/d2l/le/lessons/494809/topics/4063078
    #find row for 3000
    #find row for 9000
    for i in range(0,len(dataset)):
        data = dataset[i]
        type = types[i]
        mask = (data['wavelength'] >= 3000) & (data['wavelength'] <= 9000)    
        ax.plot(data[mask]['wavelength'],data[mask]['flux'], styles[i] , label=stars[i] + ", type: " + type, linewidth=2.0)
    ax.legend()
    #fig.xlabel('test')
    fig.savefig("plots\\plots.jpg")
    plt.savefig('plots\\plots.eps', format='eps')
    plt.savefig('plots\\plots.png', format='png')
    

import os
p = r"spectra"

#pick the 3 stars of interest
#add 3 stars to a single plot
#add axis labels
#add legend
#read spectra list
spectra_list = Table.read ( "spectra_list.csv" , format = "ascii.csv")

stars = ['Ab11f', 'Bb18','Bb63']
styles = ['--','-','-.']
folder = 'spectra\\'

dataset = list()
types = list()
for star in stars:
    filename = star+'.csv'
    print(star)
    mask = (spectra_list['filename'] == filename)
    types.append(spectra_list[mask]['type'][0])
    dataset.append(Table.read ( folder+filename , format = "ascii.csv"))

plotCSV(dataset, types, stars, styles)