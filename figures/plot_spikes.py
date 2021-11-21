import os
import sys 
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from collections import defaultdict

from shtm.helper import load_data, load_spike_data
import utils 

path_dict = {} 
path_dict['data_root_path'] = 'data'
path_dict['project_name'] = 'sequence_learning_performance' 
#path_dict['parameterspace_label'] = 'prediction_performance_stdp'
path_dict['parameterspace_label'] = 'continuous_learning_video'
#path_dict['parameterspace_label'] = 'stimulus_timing_analysis'

# get parameters 
PS, PS_path = utils.get_parameter_set(path_dict)
replay = False

#PS['DeltaT'] = 40.
PL = utils.parameter_set_list(PS)
params = PL[0]

# get trained sequences
# TODO load data training fails if the sequences are not of the same length
sequences = load_data(PS_path, 'training_data')
vocabulary = load_data(PS_path, 'vocabulary')

print('#### sequences used for training ### ')
for i, sequence in enumerate(sequences): 
    seq = '' 
    for char in sequence:
        seq += str(char).ljust(2) 
    print('sequence %d: %s' % (i, seq))

# get data path
if replay:
    data_path = utils.get_data_path(params['data_path'], params['label'], 'replay')
else:
    data_path = utils.get_data_path(params['data_path'], params['label'])

# load spikes from reference data
#inh_spikes = []
inh_spikes = load_spike_data(data_path, 'inh_spikes')
somatic_spikes = load_spike_data(data_path, 'somatic_spikes')
dendritic_current = load_spike_data(data_path, 'idend_last_episode')
#dendritic_current = load_spike_data(data_path, 'idend_eval')

# get recoding times of dendriticAP
characters_to_subpopulations = load_data(data_path, 'characters_to_subpopulations')

# get excitation times
excitation_times = load_data(data_path, 'excitation_times')

# organize the characters for plotting purpose
subpopulation_indices = []
chars_per_subpopulation = []
for char in vocabulary:
    # shift the subpopulation indices for plotting purposes 
    char_to_subpopulation_indices = characters_to_subpopulations[char]
    subpopulation_indices.extend(char_to_subpopulation_indices)

    chars_per_subpopulation.extend(char * len(characters_to_subpopulations[char]))

shifted_subpopulation_indices = np.array(subpopulation_indices) + 0.5

# plot settings 
plt.rcParams['font.size'] = 8
plt.rcParams['legend.fontsize'] = 6
plt.rcParams['figure.figsize'] = (5.2,3)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.usetex'] = False
panel_label_pos = (-0.1,1.0)

# plot spiking data of last network realization
#TODO here we assume that the sequences are of the same length

if replay: 
    number_elements_per_batch = 3 #sum([len(seq) for seq in sequences])
    start_time = 0.
    end_time = excitation_times[number_elements_per_batch] 
else:
    number_elements_per_batch = sum([len(seq) for seq in sequences])
    start_time = excitation_times[-number_elements_per_batch] 
    end_time = excitation_times[-1] + 5

utils.plot_spikes(somatic_spikes, inh_spikes, dendritic_current, start_time, end_time, params['soma_params']['I_p']-5, params['M']*params['n_E'], params['M'])

ticks_pos = shifted_subpopulation_indices * params['n_E']
ticks_label = chars_per_subpopulation
subpopulation_indices_background = np.arange(params['M'])*params['n_E']

plt.yticks(ticks_pos, ticks_label)

for i in range(params['M'])[::2]:
    plt.axhspan(subpopulation_indices_background[i], subpopulation_indices_background[i]+params['n_E'], facecolor='0.2', alpha=0.1)

print('--------------------------------------------------')
path = 'img'
if replay == True:
    fname = 'spiking_data_replay'
else:
    fname = 'spiking_data_prediction'

print('save here: %s/%s.pdf ...' % (path, fname))
os.system('mkdir -p %s' % (path))
plt.savefig('%s/%s.pdf' % (path, fname))
plt.savefig('%s/%s.png' % (path, fname))

plt.show()
