import numpy as np
import pyvista as pv
def xyz2rlonlat_in_Carrington(xyz_carrington, for_psi=False):
    """
    Convert (x,y,z) to (r,t,p) in Carrington Coordination System.
        (x,y,z) follows the definition of SPP_HG in SPICE kernel.
        (r,lon,lat) is (x,y,z) converted to heliographic lon/lat, where lon \in [0,360], lat \in [-90,90] .
    :param xyz_carrington:
    :return:
    """
    r_carrington = np.linalg.norm(xyz_carrington[0:3], 2)

    lon_carrington = np.arcsin(xyz_carrington[1] / np.sqrt(xyz_carrington[0] ** 2 + xyz_carrington[1] ** 2))
    if xyz_carrington[0] < 0:
        lon_carrington = np.pi - lon_carrington
    if lon_carrington < 0:
        lon_carrington += 2 * np.pi

    lat_carrington = np.pi / 2 - np.arccos(xyz_carrington[2] / r_carrington)
    if for_psi:
        lat_carrington = np.pi / 2 - lat_carrington
    return r_carrington, np.rad2deg(lon_carrington), np.rad2deg(lat_carrington)

def rlonlat2line(r_Rs_vect,lon_deg_vect,lat_deg_vect,to_xyz=True):
    rlonlat = np.vstack([r_Rs_vect,
                              np.deg2rad(lon_deg_vect),
                              np.deg2rad(lat_deg_vect)])
    if to_xyz:
        xyz = np.array(rlonlat2xyz_in_Carrington(rlonlat))
    else:
        xyz = np.vstack([lon_deg_vect,lat_deg_vect,r_Rs_vect])

    line = pv.lines_from_points(np.array(xyz).T)
    return line

def rlonlat2xyz_in_Carrington(rtp_carrington, for_psi=False):
    if for_psi:
        rtp_carrington[2] = np.pi / 2 - rtp_carrington[2]

    z_carrington = rtp_carrington[0] * np.cos(np.pi / 2 - rtp_carrington[2])
    y_carrington = rtp_carrington[0] * np.sin(np.pi / 2 - rtp_carrington[2]) * np.sin(rtp_carrington[1])
    x_carrington = rtp_carrington[0] * np.sin(np.pi / 2 - rtp_carrington[2]) * np.cos(rtp_carrington[1])
    return x_carrington, y_carrington, z_carrington

