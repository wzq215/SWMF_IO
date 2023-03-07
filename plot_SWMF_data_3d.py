'''
Aim: To visualize SWMF 3d data with pyvista volume rendering.
'''

import numpy as np
import matplotlib.pyplot as plt
import imageio
import pyvista
from spacepy.pybats import IdlFile

data_path = '/Users/ephe/THL8/output_0207/SC/'
file_type = 'box_mhd_4_'
n_iter = 3000
n_time = None

filename = file_type + 'n' +str(int(n_iter)).zfill(8)

data_box = IdlFile(data_path+filename+'.out')
x = data_box['x']
y = data_box['y']
z = data_box['z']
dimensions = data_box['grid']
spacing =(abs(x[1]-x[0]),abs(y[1]-y[0]),abs(z[1]-z[0]))
origin = (0.0,0.0,0.0)

var_str = 'Rho'
plot_data = np.array(data_box[var_str])

plot_data[x<0.0]=0.0
plot_data = np.log10(plot_data)

box_grid = pyvista.UniformGrid(dimensions=(dimensions[0],dimensions[1],dimensions[2]),spacing=spacing,origin=origin)
box_grid.point_data['values'] = plot_data.ravel('F')
box_grid.plot(volume=True,cmap='viridis',clim=[-25,-17],opacity=(0.0,0.0,0.2,0.8),
              show_scalar_bar=True,shade=False,show_grid=True,show_axes=True)



