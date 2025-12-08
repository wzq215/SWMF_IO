import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt

# msh = pv.read('data/pfssa_0001.vtu')
msh = pv.read('data/(SphR2d5Ref3-SphR1Ref3_Ref0)dipole.vtk')
field_lines = msh.streamlines('Bxyz',source_radius=1.1,n_points=100,progress_bar=True,
                              max_time=50,)

msh['r'] = np.linalg.norm(msh.points,axis=1)
plt.figure(dpi=300)
plt.scatter(np.log10(msh['r'].ravel()),np.log10(msh['Btot'].ravel()),s=0.1)
plt.xlabel('log10(r)')
plt.ylabel('log10(Btot)')
plt.title('ZIQI')
plt.show()
# %%
# field_lines = msh.streamlines('Bxyz',source_radius=1.1,n_points=100,progress_bar=True,
#                               max_time=50,
#                               )
# print(field_lines)
p = pv.Plotter()
# p.add_mesh(msh.slice_orthogonal())
p.add_arrows(msh.points,msh['Bxyz'],mag=1e-9)
# p.add_mesh(field_lines.tube(radius=0.01))
p.show_bounds()
p.show()


