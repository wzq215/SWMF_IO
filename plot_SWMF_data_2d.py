import os

import imageio
import matplotlib.pyplot as plt
import numpy as np
from spacepy.pybats import IdlFile

data_path = '/Users/ephe/THL8/Test_Comet_2303/output_comet_161616_40_100_amrtest/GM/'
file_name = 'z=0_var_1_n'
n_iters = np.linspace(10, 40, 4)

axes_str = 'xyz'
cut_str = file_name[0]
axis1_str = axes_str.replace(cut_str,'')[0]
axis2_str = axes_str.replace(cut_str,'')[1]
print('Read data '+cut_str+'=0, plot on '+axis1_str+'O'+axis2_str+' plane...')

test_data = IdlFile(data_path + '' + file_name + str(int(40)).zfill(8) + '.out')
var_list = list(test_data.keys())
unit_list = test_data.meta['header'].split()[1:]
print('Variables: ', var_list)
print('Units: ', unit_list)

plot_var = input('Input Plot Var: ', )
# plot_var = 'SwRho'
plot_ind = var_list.index(plot_var)
plot_unit = unit_list[plot_ind]
plot_var_min = test_data[plot_var].min()
plot_var_max = test_data[plot_var].max()


print('Plot variable '+plot_var+', unit: '+plot_unit+'...')


is_log = False
if is_log:
    plot_var_min = np.log10(plot_var_min)
    plot_var_max = np.log10(plot_var_max)
    print('Log it.')

if not os.path.exists(data_path + plot_var + '_viz/'):
    os.mkdir(data_path + plot_var + '_viz/')

frames = []
for n_iter in n_iters:
    file_str = file_name + str(int(n_iter)).zfill(8)
    data_2d = IdlFile(data_path + '' + file_str + '.out')
    print('grid num: ',data_2d['grid'])
    fig, ax = plt.subplots()
    if not is_log:
        tpc = ax.tripcolor(data_2d[axis1_str], data_2d[axis2_str], np.array(data_2d[plot_var]))
        plt.title(plot_var + ' [' + unit_list[plot_ind] + '] (n' + str(int(n_iter)).zfill(8) + ')')
    else:
        tpc = ax.tripcolor(data_2d[axis1_str], data_2d[axis2_str], np.log10(np.array(data_2d[plot_var])))
        plt.title('log10('+plot_var + ') [' + unit_list[plot_ind] + '] (n' + str(int(n_iter)).zfill(8) + ')')

    plt.colorbar(tpc)
    tpc.set_clim(plot_var_min,plot_var_max)
    tpc.set_cmap('jet')
    plt.axis('equal')
    plt.xlabel(axis1_str+'['+unit_list[1]+']')
    plt.ylabel(axis2_str+'['+unit_list[2]+']')
    plt.savefig(data_path + plot_var + '_viz/' + plot_var + '_' + file_str + '.png')
    plt.close()
    frames.append(imageio.imread(data_path + plot_var + '_viz/' + plot_var + '_' + file_str + '.png'))
print('Done with plot, generating movie...')
print('Plots and movie in '+data_path + plot_var + '_viz/')
imageio.mimsave(data_path + plot_var + '_viz/' + plot_var + '_' + file_str + '.mp4', frames, fps=4)
