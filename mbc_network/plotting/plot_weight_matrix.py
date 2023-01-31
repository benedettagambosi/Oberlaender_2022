""" TODO
"""

import os

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import sys, os
sys.path.append('/home/benedetta/.pyenv/versions/3.8.6/envs/mbc/mbc_replication/')
from mbc_network.helper import training_helper
from mbc_network.helper import plot_helper


def plot_weight_matrices(axes: Axes = None):

    assert axes is not None, 'Need axes object.'

    data_path = get_data_path()
    path_old_weights = os.path.join(data_path, 'ee_connections_before.npy')
    path_new_weights = os.path.join(data_path, 'ee_connections.npy')

    old_connections = np.load(path_old_weights)
    new_connections = np.load(path_new_weights)

    plot_helper.plot_weight_matrix(ax=axes[0], connections=old_connections, title='old weight matrix')
    plot_helper.plot_weight_matrix(ax=axes[1], connections=new_connections, title='new weight matrix')
    plot_helper.plot_diff_weight_matrix(ax=axes[2], connections_new=new_connections, connections_old=old_connections, title='difference of matrices')

    # print(np.allclose(plot_helper.matrix_from_connections(old_connections), plot_helper.matrix_from_connections(new_connections)))
# def plot_weight_matrices(axes=None):

#     assert axes is not None, 'Need axes object.'

#     data_path = get_data_path()
#     path_old_weights = os.path.join(data_path, 'ei_connections_before.npy')
#     path_new_weights = os.path.join(data_path, 'ei_connections.npy')

#     old_connections = np.load(path_old_weights)
#     new_connections = np.load(path_new_weights)

#     plot_helper.plot_weight_matrix(ax=axes[0], connections=old_connections, title='old weight matrix')
#     plot_helper.plot_weight_matrix(ax=axes[1], connections=new_connections, title='new weight matrix')
#     plot_helper.plot_diff_weight_matrix(ax=axes[2], connections_new=new_connections, connections_old=old_connections, title='difference of matrices')

#     print(np.allclose(plot_helper.matrix_from_connections(old_connections), plot_helper.matrix_from_connections(new_connections)))


def plot_2_mins_weight_matrix(ax: Axes = None, filename: str = None):
    assert ax is not None, 'Need axes object.'
    assert filename is not None, 'Need filename.'

    connections = np.load(filename)
    plot_helper.plot_weight_matrix(ax=ax, connections=connections, title='weight strength')


def get_data_path():
    path_dict = {}
    path_dict['data_root_path'] = 'data'
    path_dict['project_name'] = 'sequence_learning_performance'
    path_dict['parameterspace_label'] = 'sequence_learning_and_prediction'

    # get parameters
    PS, PS_path = training_helper.get_parameter_set(path_dict)  # TODO remove helper.parameter_set_list() and fix data path
    replay = False
    PL = training_helper.parameter_set_list(PS)
    params = PL[0]

    # get data path
    if replay:
        data_path = training_helper.get_data_path(params['data_path'], params['label'], 'replay')
    else:
        data_path = training_helper.get_data_path(params['data_path'], params['label'])

    return data_path


if __name__ == '__main__':
    with plt.rc_context({
                        # plot settings
                        'font.size': 8,
                        'legend.fontsize': 6,
                        'figure.figsize': (10, 5),
                        'font.family': 'sans-serif',
                        'text.usetex': False
                        }):
        figure, axes = plt.subplots(1, 3)
        plot_weight_matrices(axes)
        figure.tight_layout()
        plt.show()
