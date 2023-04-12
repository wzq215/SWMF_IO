import os

import imageio
import matplotlib.pyplot as plt
import numpy as np
from spacepy.pybats import IdlFile

# data_path = '/Users/ephe/THL8/Test_Comet_2303/output_comet_161616_realconst/GM/'
data_path = '/Users/ephe/THL8/Test_SC230315_2304/output_SCIH_6000SC/SC/'

file_name = 'y=0_var_2_n'
n_iters = np.linspace(100, 6000, 60)

axes_str = 'xyz'
cut_str = file_name[0]
axis1_str = axes_str.replace(cut_str,'')[0]
axis2_str = axes_str.replace(cut_str,'')[1]
print('Read data '+cut_str+'=0, plot on '+axis1_str+'O'+axis2_str+' plane...')

test_data = IdlFile(data_path + '' + file_name + str(int(4000)).zfill(8) + '.out')
var_list = list(test_data.keys())
unit_list = test_data.meta['header'].split()[1:]
print('Variables: ', var_list)
print('Units: ', unit_list)
print('Supported derived variables: Btot [nT], U [km/s], SwU [km/s], HpU [km/s], H2OpU [km/s]')

plot_var = input('Input Plot Var: ', )
# plot_var = 'SwRho'
is_derived= False
if plot_var in var_list:
    plot_ind = var_list.index(plot_var)
    plot_unit = unit_list[plot_ind]
    plot_var_min = test_data[plot_var].min()
    plot_var_max = test_data[plot_var].max()
else:
    if plot_var == 'Btot':
        plot_unit = 'nT'
        plot_var_min = 2.765
        plot_var_max = 2.777
        is_derived = True
    elif plot_var == 'SwU':
        plot_unit= 'km/s'
        plot_var_min = np.nanmin(np.sqrt(test_data['SwUx']**2+test_data['SwUy']**2+test_data['SwUz']**2))
        plot_var_max = np.nanmax(np.sqrt(test_data['SwUx']**2+test_data['SwUy']**2+test_data['SwUz']**2))
        is_derived = True
    elif plot_var == 'HpU':
        plot_unit = 'km/s'
        plot_var_min = np.nanmin(np.sqrt(test_data['HpUx'] ** 2 + test_data['HpUy'] ** 2 + test_data['HpUz'] ** 2))
        plot_var_max = np.nanmax(np.sqrt(test_data['HpUx'] ** 2 + test_data['HpUy'] ** 2 + test_data['HpUz'] ** 2))
        is_derived = True
    elif plot_var == 'H2OpU':
        plot_unit = 'km/s'
        plot_var_min = np.nanmin(np.sqrt(test_data['H2OpUx'] ** 2 + test_data['H2OpUy'] ** 2 + test_data['H2OpUz'] ** 2))
        plot_var_max = np.nanmax(np.sqrt(test_data['H2OpUx'] ** 2 + test_data['H2OpUy'] ** 2 + test_data['H2OpUz'] ** 2))
        is_derived = True
    elif plot_var == 'U':
        plot_unit = 'km/s'
        plot_var_min = np.nanmin(np.sqrt(test_data['Ux'] ** 2 + test_data['Uy'] ** 2 + test_data['Uz'] ** 2))
        plot_var_max = np.nanmax(np.sqrt(test_data['Ux'] ** 2 + test_data['Uy'] ** 2 + test_data['Uz'] ** 2))
        is_derived = True

print('Plot variable '+plot_var+', unit: '+plot_unit+'...')


is_log = True
if is_log:
    plot_var_min = np.log10(plot_var_min)
    plot_var_max = np.log10(plot_var_max)
    print('Log it.')

if not os.path.exists(data_path + plot_var + '_viz/'):
    os.mkdir(data_path + plot_var + '_viz/')
if not os.path.exists(data_path  + 'movies/'):
    os.mkdir(data_path  + 'movies/')

frames = []
for n_iter in n_iters:
    file_str = file_name + str(int(n_iter)).zfill(8)
    data_2d = IdlFile(data_path + '' + file_str + '.out')
    print('grid num: ',data_2d['grid'])
    fig, ax = plt.subplots()

    if is_derived:
        if plot_var=='Btot':
            plot_data = np.sqrt(data_2d['Bx']**2+data_2d['By']**2+data_2d['Bz']**2)
        elif plot_var=='U':
            plot_data = np.sqrt(data_2d['Ux']**2+data_2d['Uy']**2+data_2d['Uz']**2)
        elif plot_var=='SwU':
            plot_data = np.sqrt(data_2d['SwUx']**2+data_2d['SwUy']**2+data_2d['SwUz']**2)
        elif plot_var=='HpU':
            plot_data = np.sqrt(data_2d['HpUx']**2+data_2d['HpUy']**2+data_2d['HpUz']**2)
        elif plot_var=='H2OpU':
            plot_data = np.sqrt(data_2d['H2OpUx']**2+data_2d['H2OpUy']**2+data_2d['H2OpUz']**2)
    else:
        plot_data = data_2d[plot_var]

    if not is_log:
        tpc = ax.tripcolor(data_2d[axis1_str], data_2d[axis2_str], np.array(plot_data))
        plt.title(plot_var + ' [' + plot_unit + '] (n' + str(int(n_iter)).zfill(8) + ')')
    else:
        tpc = ax.tripcolor(data_2d[axis1_str], data_2d[axis2_str], np.log10(np.array(plot_data)))
        plt.title('log10('+plot_var + ') [' + plot_unit + '] (n' + str(int(n_iter)).zfill(8) + ')')
    # plt.scatter(data_2d['x'],data_2d['y'],s=1.)
    plt.colorbar(tpc)
    tpc.set_clim(plot_var_min,plot_var_max)
    tpc.set_cmap('jet')
    plt.axis('equal')
    plt.xlabel(axis1_str+'['+unit_list[1]+']')
    plt.ylabel(axis2_str+'['+unit_list[2]+']')
    plt.savefig(data_path + plot_var + '_viz/' + plot_var + '_' + file_str + '.png')
    # plt.show()
    plt.close()
    frames.append(imageio.imread(data_path + plot_var + '_viz/' + plot_var + '_' + file_str + '.png'))
print('Done with plot, generating movie...')
print('Plots in '+data_path + plot_var + '_viz/' +' and movies in '+data_path  + 'movies/')
imageio.mimsave(data_path  + 'movies/' + plot_var + '_' + file_str + '.mp4', frames, fps=4)
