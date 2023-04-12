import os
import imageio
import matplotlib.pyplot as plt
import numpy as np
from spacepy.pybats import IdlFile

filename = '/Users/ephe/THL8/Test_SC230315_2304/fdips_bxyz_23031418.out'
Bxyz = IdlFile(filename)
header = Bxyz.meta['header'].split(';')
print('=======HEADER INFO=======')
for var in header:
    print(var)
print('=========================')
Bx = Bxyz['Bx']
By = Bxyz['By']
Bz = Bxyz['Bz']
Bt = np.sqrt(Bx**2+By**2+Bz**2)

lon = np.array(Bxyz['Longitude'])
lat = np.array(Bxyz['Latitude'])

X,Y = np.meshgrid(lon,lat)
plt.pcolormesh(X,Y,np.array(Bt[-1,:,:]).T)
plt.colorbar()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('B_tot')
