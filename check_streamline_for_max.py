import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt

msh = pv.read('data/pfssa_0001.vtu')
# %%
msh.point_data['B_vec'] = np.column_stack((msh['b1'], msh['b2'], msh['b3']))*1e9
msh.point_data['V_vec'] = np.column_stack((msh['v1'], msh['v2'], msh['v3']))
msh.point_data['r'] = np.linalg.norm(msh.points,axis=1)
msh.point_data['Btot'] = np.linalg.norm(msh['B_vec'],axis=1)
msh.set_active_scalars('br')
msh.set_active_vectors('B_vec')
surf = msh.extract_surface()

# %%
plt.figure(dpi=300)
plt.scatter(np.log10(msh['r'].ravel()),np.log10(msh['Btot'].ravel()),s=0.1)
plt.xlabel('log10(r)')
plt.ylabel('log10(Btot*1e9)')
plt.title('MAX')
plt.show()
# %%
field_lines = msh.streamlines(source_radius=2.0, n_points=100,
                              # max_time = 10000,
                              # max_steps=5000,
                              # initial_step_length=0.001,
                              # min_step_length=0.0001,
                              # terminal_speed=1e-1,
                              progress_bar=True,)
# field_lines = msh.streamlines_from_source(surf,'B_vec',integration_direction='both',surface_streamlines=True,
#                                           progress_bar=True)
print(field_lines)
p = pv.Plotter()
p.add_mesh(msh.slice_orthogonal())
p.add_mesh(field_lines.tube(radius=0.1))
p.add_arrows(msh.points,msh['B_vec'],mag=1e-11)
p.show_bounds()
p.show()



