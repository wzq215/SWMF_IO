import imageio
import matplotlib.pyplot as plt
import numpy as np
import pyvista
from spacepy.pybats import IdlFile

def HCS_from_shl(data_shl):
    r,lon,lat = np.array(data_shl['r']),np.deg2rad(np.array(data_shl['lon'])),np.deg2rad(np.array(data_shl['lat']))
    Bx,By,Bz = np.array(data_shl['Bx']),np.array(data_shl['By']),np.array(data_shl['Bz'])

    rv,lonv,latv = np.meshgrid(r,lon,lat,indexing='ij')

    xv = rv*np.cos(lonv)*np.cos(latv)
    yv = rv*np.sin(lonv)*np.cos(latv)
    zv = rv*np.sin(latv)

    Br = (Bx*xv+By*yv+Bz*zv)/np.sqrt(xv**2+yv**2+zv**2)

    mesh = pyvista.StructuredGrid(xv, yv, zv)
    mesh.point_data['values'] = Br.ravel(order='F')# also the active scalars
    isos_br = mesh.contour(isosurfaces=1, rng=[0., 0.])

    vectors = np.empty((mesh.n_points, 3))
    vectors[:, 0] = Bx.ravel(order='F')
    vectors[:, 1] = By.ravel(order='F')
    vectors[:, 2] = Bz.ravel(order='F')
    mesh['vectors'] = vectors

    p = pyvista.Plotter()
    stream, src = mesh.streamlines('vectors', return_source=True, source_radius=6, n_points=100,
                                   progress_bar=True,
                                   max_time=50.)
    p.add_mesh(stream.tube(radius=0.05), color='white')
    p.add_mesh(isos_br, opacity=0.5)
    p.add_mesh(pyvista.Sphere(1))
    p.show_grid()
    p.show()

def lines_from_points(points):
    """Given an array of points, make a line set"""
    poly = pyvista.PolyData()
    poly.points = points
    cells = np.full((len(points) - 1, 3), 2, dtype=np.int_)
    cells[:, 1] = np.arange(0, len(points) - 1, dtype=np.int_)
    cells[:, 2] = np.arange(1, len(points), dtype=np.int_)
    poly.lines = cells
    return poly

def Trace_in_shl(data_shl,pos_target):
    r,lon,lat = np.array(data_shl['r']),np.deg2rad(np.array(data_shl['lon'])),np.deg2rad(np.array(data_shl['lat']))
    Bx,By,Bz = np.array(data_shl['Bx']),np.array(data_shl['By']),np.array(data_shl['Bz'])

    rv,lonv,latv = np.meshgrid(r,lon,lat,indexing='ij')

    xv = rv*np.cos(lonv)*np.cos(latv)
    yv = rv*np.sin(lonv)*np.cos(latv)
    zv = rv*np.sin(latv)

    Br = (Bx*xv+By*yv+Bz*zv)/np.sqrt(xv**2+yv**2+zv**2)

    line = lines_from_points(pos_target)

    mesh = pyvista.StructuredGrid(xv, yv, zv)

    mesh.point_data['values'] = Br.ravel(order='F')# also the active scalars
    isos_br = mesh.contour(isosurfaces=1, rng=[0., 0.])

    vectors = np.empty((mesh.n_points, 3))
    vectors[:, 0] = Bx.ravel(order='F')
    vectors[:, 1] = By.ravel(order='F')
    vectors[:, 2] = Bz.ravel(order='F')
    mesh['vectors'] = vectors
    streams = []
    p = pyvista.Plotter()
    for i in range(len(pos_target)):
        start_point = pos_target[i]
        stream = mesh.streamlines('vectors', progress_bar=True, start_position=start_point, return_source=False,
                              integration_direction='both',
                              max_time=100., max_error=1e-2)
        streams.append(stream)
        # p.add_mesh(stream.tube(radius=.1),color='white')

    p.add_mesh(isos_br, opacity=1.)
    p.add_mesh(pyvista.Sphere(1))
    p.add_mesh(line.tube(radius=0.1), color='r')
    p.show_grid()
    p.show()

def Trace_in_box(data_box):
    # r,lon,lat = np.array(data_shl['r']),np.deg2rad(np.array(data_shl['lon'])),np.deg2rad(np.array(data_shl['lat']))
    x,y,z = np.array(data_box['x']),np.array(data_box['y']),np.array(data_box['z'])
    Bx,By,Bz = np.array(data_box['Bx']),np.array(data_box['By']),np.array(data_box['Bz'])

    xv,yv,zv = np.meshgrid(x,y,z,indexing='ij')
    # rv,lonv,latv = np.meshgrid(r,lon,lat,indexing='ij')

    # xv = rv*np.cos(lonv)*np.cos(latv)
    # yv = rv*np.sin(lonv)*np.cos(latv)
    # zv = rv*np.sin(latv)

    # Br = (Bx*xv+By*yv+Bz*zv)/np.sqrt(xv**2+yv**2+zv**2)

    # line = lines_from_points(pos_target)

    mesh = pyvista.StructuredGrid(xv, yv, zv)

    # mesh.point_data['values'] = Br.ravel(order='F')# also the active scalars
    # isos_br = mesh.contour(isosurfaces=1, rng=[0., 0.])

    vectors = np.empty((mesh.n_points, 3))
    vectors[:, 0] = Bx.ravel(order='F')
    vectors[:, 1] = By.ravel(order='F')
    vectors[:, 2] = Bz.ravel(order='F')
    mesh['vectors'] = vectors
    streams = []
    p = pyvista.Plotter()
    # for i in range(len(pos_target)):
    #     start_point = pos_target[i]
        # stream = mesh.streamlines('vectors', progress_bar=True, start_position=start_point, return_source=False,
        #                       integration_direction='both',
        #                       max_time=100., max_error=1e-2)
    stream, src = mesh.streamlines('vectors', return_source=True, source_radius=400, n_points=100,
                                   progress_bar=True,
                                   integration_direction='both', max_time=1000.)
    streams.append(stream)
    p.add_mesh(stream.tube(radius=.1),color='white')

    # p.add_mesh(isos_br, opacity=1.)
    # p.add_mesh(pyvista.Sphere(1))
    # p.add_mesh(line.tube(radius=0.1), color='r')
    p.show_grid()
    p.show()
    return stream



if __name__ =='__main__':
    data_path = '/Users/ephe/THL8/Test_SC230315_2304/output_SCIH_6000SC/SC/'
    file_type = 'shl_mhd_3_n'
    n_iter = 100
    filename = file_type + str(int(n_iter)).zfill(8)
    filename = 'shl_mhd_5_t00000040_n00000041'
    print('Reading File: ', filename)
    print('File Path: ', data_path+filename+'.out')
    data_shl = IdlFile(data_path + filename + '.out')
    # HCS_from_shl(data_shl)
    x_target=np.array([34.11100479993646,30.20349439794439])
    y_target=np.array([-9.724387083851413,-8.721135506369109])
    z_target=np.array([1.5641191195150517,1.2014245530382486])
    pos_target = np.array([x_target,y_target,z_target]).T
    print(pos_target.shape)
    Trace_in_shl(data_shl,pos_target)
