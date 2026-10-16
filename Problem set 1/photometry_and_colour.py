from astropy.io import fits
from alopphot import findstars, aperphot
import numpy as np
from matplotlib import pyplot as plt
import math

gain = 5
RON = 250

def magnitude_adu(flux, gain):
    photonCount = flux*gain
    return -2.5*math.log(photonCount,10)

def SN(N_source, Nsky, k):
    return (gain * N_source)/math.sqrt((gain * N_source) + (gain * k * Nsky) + (k*RON*RON))

def uncertainties(flux_bv, pixel_radius):
    k = math.pi * pixel_radius * pixel_radius
    us = list()
    for bv in flux_bv:
        N_source_B = bv[0]
        N_sky_B = bv[1] #is per pixel
        SN_B = SN(N_source_B, N_sky_B, k)
        N_source_V = bv[2] 
        N_sky_V = bv[3] #is per pixel
        SN_V = SN(N_source_V, N_sky_V, k)
        us.append([SN_B, SN_V])
    return us


ccd_v = fits.getdata("exposure_V_alop_2026_2027.fits")
ccd_b = fits.getdata("exposure_B_alop_2026_2027.fits")
sources_v = findstars(ccd_v, 1100, 5)
print(sources_v)
sources_b = findstars(ccd_b, 1100, 5)
print(sources_b)

result_v = aperphot(ccd_v, sources_v["x"], sources_v["y"], 5, [6,8])
result_b = aperphot(ccd_b, sources_b["x"], sources_b["y"], 5, [6,8])
print(result_v)
print(result_b)

flux_bv = np.stack((result_b[0], result_b[1], result_v[0], result_v[1]), axis=1)

for bv in flux_bv:
    mb = magnitude_adu((bv[0])/30, gain)+16.43
    mv = magnitude_adu((bv[2])/10, gain)+17.4 
    bminusv = mb - mv   
    txt = "{b_tot:.0f} & {b_noise:.0f} & {v_tot:.0f} & {v_noise:.0f} & {mb:.3f} & {mv:.3f} & {bv:.3f} \\\\"
    print(txt.format(b_tot = bv[0], b_noise = bv[1], v_tot = bv[2], v_noise = bv[3], mb = mb, mv = mv, bv = bminusv))
    #print(bminusv)

u = uncertainties(flux_bv, 5)
print(u)

#print(adu)

# Optional: Downsample or slice large arrays (e.g., take a sub-region)
# data = data[250:270, 400:420]

# 2. Create coordinate grids (X and Y)
y, x = np.indices(ccd_v.shape)

# 3. Plot the 3D surface
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(projection='3d')

# surface plot
surf = ax.plot_surface(
    x,
    y,
    ccd_v,
    cmap='viridis',
    edgecolor='none',
    linewidth=0,
    antialiased=True,
)

ax.set_title('3D Surface Plot of FITS Data')
ax.set_xlabel('X Pixel')
ax.set_ylabel('Y Pixel')
ax.set_zlabel('Intensity / Value')
fig.colorbar(surf, shrink=0.5, aspect=10)

#flux, sky = aperphot(data, [119.99630765519932], [69.99063811643735], 10.0, [12.0,16.0])

#print(flux)
#print(sky)

plt.show()
plt.close()

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(ccd_v, cmap='gray', origin='lower')
ax2.imshow(ccd_b, cmap='gray', origin='lower')
plt.show()



