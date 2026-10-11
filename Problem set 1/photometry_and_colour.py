from astropy.io import fits
from alopphot import findstars, aperphot
import numpy as np
from matplotlib import pyplot as plt

data = fits.getdata("exposure_V_alop_2026_2027.fits")
sources = findstars(data, 1100, 1)
print(sources)

# Optional: Downsample or slice large arrays (e.g., take a sub-region)
# data = data[250:270, 400:420]

# 2. Create coordinate grids (X and Y)
y, x = np.indices(data.shape)

# 3. Plot the 3D surface
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(projection='3d')

# surface plot
surf = ax.plot_surface(
    x,
    y,
    data,
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



