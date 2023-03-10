'''
Aim: To visualize SWMF 3d data with pyvista volume rendering.
Modified for OH Data
Revised 23/03/10
'''

import numpy as np
import matplotlib.pyplot as plt
import imageio
import pyvista
from spacepy.pybats import IdlFile

# from plot_SWMF_Bxyz import Trace_in_box
k_b = 1.38e-23


def Trace_in_box(data_box, src_radius=400, n_src_points=100):
    # r,lon,lat = np.array(data_shl['r']),np.deg2rad(np.array(data_shl['lon'])),np.deg2rad(np.array(data_shl['lat']))
    x, y, z = np.array(data_box['x']), np.array(data_box['y']), np.array(data_box['z'])
    Bx, By, Bz = np.array(data_box['Bx']), np.array(data_box['By']), np.array(data_box['Bz'])

    xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')

    mesh = pyvista.StructuredGrid(xv, yv, zv)

    vectors = np.empty((mesh.n_points, 3))
    vectors[:, 0] = Bx.ravel(order='F')
    vectors[:, 1] = By.ravel(order='F')
    vectors[:, 2] = Bz.ravel(order='F')
    mesh['vectors'] = vectors
    streams = []

    stream, src = mesh.streamlines('vectors', return_source=True, source_radius=src_radius, n_points=n_src_points,
                                   progress_bar=True,
                                   integration_direction='both', max_time=1000.)
    streams.append(stream)

    # p = pyvista.Plotter()
    # p.add_mesh(stream.tube(radius=1),color='white')
    # p.show_grid()
    # p.show()

    return stream


if __name__ == '__main__':
    # %%
    data_path = '/Users/ephe/THL8/OH_THC/'
    file_type = 'box_mhd_5_'
    n_iter = 20000
    n_time = None

    filename = file_type + 'n' + str(int(n_iter)).zfill(8)

    data_box = IdlFile(data_path + filename + '.out')
    x = data_box['x']
    y = data_box['y']
    z = data_box['z']
    dimensions = data_box['grid']
    spacing = (abs(x[1] - x[0]), abs(y[1] - y[0]), abs(z[1] - z[0]))
    origin = (x[0], y[0], z[0])
    print(origin)
    print(spacing)
    # %%

    data_rho = data_box['Rho']
    data_p = data_box['P']
    data_T = (data_p / 10) / k_b / (2 * data_rho * 1e6)

    # var_str = 'Rho [amu/cc]'
    # plot_data = np.array(data_box['Rho'])
    # plot_data[x<0.0]=0.0
    # plot_data = np.log10(plot_data)

    var_str = 'T [K]'
    plot_data = data_T

    box_grid = pyvista.UniformGrid(dimensions=(dimensions[0], dimensions[1], dimensions[2]), spacing=spacing,
                                   origin=origin)
    box_grid.point_data[var_str] = plot_data.ravel('F')
    # %%
    stream = Trace_in_box(data_box)
    # %%
    p = pyvista.Plotter()

    vol = p.add_volume(box_grid, cmap='magma',
                       clim=[1e2, 2e6],  # Change Colorbar
                       opacity=(0.1, 1., 0.5),  # Change Opacity Mask
                       opacity_unit_distance=500)  # 调整透明的程度
    # vol.prop.interpolation_type='linear'

    p.add_mesh(stream.tube(radius=1.), color='white')

    p.set_background("black")
    p.add_title('Heliosphere')
    p.show_grid()

    p.show()
