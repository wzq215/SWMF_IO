# SWMF_IO
Codes to process input and output files of SWMF

## remap_magnetogram.py
Codes from SWMF/utils/DATAREAD/srcMagnetogram.
!!! Modified to use astropy.io.fits due to version trouble.

## plot_SWMF_data_2d.py
Read z=0_mhd (2d cuts) files. Plot 2d cuts and generate animations with tripcolor.
* 230314 UPDATE 
  * Renamed from plot_SWMF_data.py. 
  * Specified to read 2d cut outputs and plot movies. Better IO.

## plot_SWMF_data_shl.py
Read shl_mhd files. Visualize HCS and magnetic field lines with pyvista.
* 230314 UPDATE
  * Renamed from plot_SWMF_Bxyz.py
  * Specified to read shl outputs. Plot streamlines from Bxyz or Uxyz.

## plot_SWMF_data_box.py
* 230314 UPDATE
  * Renamed from plot_SWMF_data_3d.py
  * Specified to read box outputs. Plot streamlines. Volume rendering by pyvista

## Requirements 230314
* imageio~=2.9.0 
* matplotlib~=3.5.1 
* numpy~=1.19.5 
* spacepy~=0.3.0 
* astropy~=5.0 
* scipy~=1.4.1 
* pyvista~=0.38.3
