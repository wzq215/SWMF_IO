import imageio
import matplotlib.pyplot as plt
import numpy as np
from spacepy.pybats import IdlFile

# 如果是2d cut的文件：
data_path = '/Users/ephe/THL8/output_0203.SCIH/output_0203.orig/SC/'
file_name = 'z=0_var_3_n'
n_iters = np.linspace(0, 100, 11)
para_str = 'bz'
frames = []
for n_iter in n_iters:
    file_str = file_name + str(int(n_iter)).zfill(8)
    data_2d = IdlFile(data_path + '' + file_str + '.out')
    fig, ax = plt.subplots()
    # tpc=ax.tripcolor(data_2d['x'], data_2d['y'], np.log10(np.array(data_2d[para_str])))
    tpc = ax.tripcolor(data_2d['x'], data_2d['y'], np.array(data_2d[para_str]))
    # plt.title('log Rho [log(g/cm^3)]'+'(n'+str(int(n_iter)).zfill(8)+')')
    plt.title('Bz [G]' + '(n' + str(int(n_iter)).zfill(8) + ')')
    plt.colorbar(tpc)
    tpc.set_clim(-1e-4, 1e-4)
    # tpc.set_clim(-16,-13)
    plt.axis('equal')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig(data_path + file_str + '_' + para_str + '.png')
    plt.close()
    # plt.show()
    frames.append(imageio.imread(data_path + file_str + '_' + para_str + '.png'))
imageio.mimsave(data_path + file_str + '_' + para_str + '.mp4', frames, fps=4)
