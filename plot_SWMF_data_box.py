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
import plotly.offline as py
import plotly.graph_objects as go

# from plot_SWMF_Bxyz import Trace_in_box
k_b = 1.38e-23


def Trace_in_box(data_box, src_radius=100, n_src_points=100):
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

    print('Reading file: '+data_path + filename + '.out')
    data_box = IdlFile(data_path + filename + '.out')
    var_list = list(data_box.keys())
    unit_list = data_box.meta['header'].split()[1:]
    print('Variables: ', var_list)
    print('Units: ', unit_list)
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
    var_str = 'T [K]'
    plot_data = data_T

    var_str = 'Rho [amu/cc]'
    plot_data = np.array(data_box['Rho'])
    # var_str = '|B| [nT]'
    # plot_data = np.sqrt(data_box['Bx']**2+data_box['By']**2+data_box['Bz']**2)*1e5
    cmin = plot_data.min()
    cmax = plot_data.max()
    print(cmin,cmax)

    # plot_data = np.log10(plot_data)



    box_grid = pyvista.UniformGrid(dimensions=(dimensions[0], dimensions[1], dimensions[2]), spacing=spacing,
                                   origin=origin)
    box_grid.point_data[var_str] = plot_data.ravel('F')
    # %%
    stream_outer = Trace_in_box(data_box,src_radius=300.,n_src_points=50)
    stream_inner = Trace_in_box(data_box,src_radius=10.,n_src_points=50)
    # %%
    p = pyvista.Plotter()

    # vol = p.add_volume(box_grid, cmap='plasma',
    #                    clim=[3.,15.],  # Change Colorbar
    #                    opacity=( 0.,1,1),  # Change Opacity Mask
    #                    opacity_unit_distance=500)  # 调整透明的程度
    vol = p.add_volume(box_grid, cmap='magma',
                       clim=[1e-4, 1e-2],  # Change Colorbar
                       opacity=(0., .5, 0.),  # Change Opacity Mask
                       opacity_unit_distance=150)  # 调整透明的程度

    p.add_mesh(stream_outer.tube(radius=1.), color='green')
    p.add_mesh(stream_inner.tube(radius=1.),color='silver')

    # slices = box_grid.slice_orthogonal(x=0, y=0, z=0)
    # p.add_mesh_slice_orthogonal(box_grid,cmap='jet',
    #                             # clim=[-1.3e-7,-1e-7]
    #                             clim=[-3e-11,3e-11]
    #                             # clim=[0.00125,0.00126]
    #                             # clim=[0.0,0.002]
    #                             # clim=[7.5,8.6]
    #                             # clim=[2.497,2.505]
    #                             # clim=[2.504-0.0005,2.504+0.001],
    #                             # clim=[0.00021,0.00028],
    #                             # clim=[0.003,0.007]
    #                             # clim=[-0.003,-0.001]
    #                             # clim = [6.03,6.06]
    #                             )
    p.set_background("black")
    # p.add_title('Comet')
    p.show_grid()
    p.show(auto_close=False)
    # path = p.generate_orbital_path(n_points=36, shift=box_grid.length)
    viewup = [0.5, 0.5, 1]
    path = p.generate_orbital_path(factor=2.0, shift=box_grid.length, viewup=viewup, n_points=36)

    p.open_movie("orbit.mov")
    p.orbit_on_path(path, write_frames=True)
    p.close()

# %%
    vertices = box_grid.points
    # triangles = box_grid.faces.reshape(-1, 4)
    plot = go.Figure()
    plot.add_trace(go.Volume(x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2],
                             opacity=0.05,
                             value=plot_data.ravel('F'),
                             isomin=1e-4,
                             isomax=1e-2,
                             surface_count=16,
                             showscale=True,
                             ))

    py.plot(plot)
    # p.export_html(data_path + 'sample.html')
    # p.show()
    # widget = p.to_pythreejs()

