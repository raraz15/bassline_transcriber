#!/usr/bin/env python
# coding: utf-8

import os

import numpy as np
import librosa.display
from matplotlib import pyplot as plt

from ..utilities import get_chorus_beat_positions, get_bar_positions, get_quarter_beat_positions

colors = ['0.5','tab:orange','tab:olive','moccasin','khaki','steelblue','b','g','r','c','m','y','k','c','w']
unk_colors = ['purple','hotpink','lime','firebrick','salmon','darkred','mistyrose']


def beat_plotting(title, directories):
    """
    Makes the beat-grid plottable.
    """
    
    beat_positions = get_chorus_beat_positions(title, directories)
    beat_positions -= beat_positions[0]
    bar_positions = get_bar_positions(beat_positions)
    beat_positions_plotting = [val for idx,val in enumerate(beat_positions) if idx%4]
    quarter_beat_positions = [val for idx,val in enumerate(get_quarter_beat_positions(beat_positions)) if idx%4]  
        
    return bar_positions, beat_positions_plotting, quarter_beat_positions


def form_beat_grid_waveform(title, directories, audio_array, fs, ax):
    """
    Plots the bar, beat and quarter beats on a given waveform plt.ax
    """

    bar_positions, beat_positions_plotting, quarter_beat_positions = beat_plotting(title, directories)

    librosa.display.waveplot(audio_array, sr=fs, ax=ax)
    ax.vlines(beat_positions_plotting, -0.9, 0.9, alpha=0.8, color='r',linestyle='dashed', linewidths=3)
    ax.vlines(quarter_beat_positions, -0.7, 0.7, alpha=0.8, color='k',linestyle='dashed', linewidths=3)
    ax.vlines(bar_positions, -1.1, 1.1, alpha=0.8, color='g',linestyle='dashed', linewidths=3)
    ax.set_xlim([-0.05, (len(audio_array)/fs)+0.05])
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_size(14)

    ax.set_title('Waveform', fontsize=15)


def form_beat_grid_spectrogram(title, directories, ax, spectrogram, fs, hop_length):
    """
    Plots the bar, beat and quarter beats on a given spectrogram plt.ax
    """

    bar_positions, beat_positions_plotting, quarter_beat_positions = beat_plotting(title, directories)

    librosa.display.specshow(spectrogram, sr=fs, hop_length=hop_length, x_axis='time', y_axis='log', ax=ax)

    ax.vlines(quarter_beat_positions, 0, 170, alpha=0.8, color='c',linestyle='dashed', linewidths=3)
    ax.vlines(beat_positions_plotting, 0, 256, alpha=0.8, color='w',linestyle='dashed', linewidths=4)
    ax.vlines(bar_positions, 0, 512, alpha=0.8, color='g',linestyle='dashed', linewidths=5)

    ax.set_xlim([-0.05, (spectrogram.shape[1]*hop_length/fs)+0.05])
    ax.set_ylim([-5,512]) 

    display_frequencies = np.array([0,32,48,64,96,128,256,512])
    ax.yaxis.set_ticks(display_frequencies)
    ax.set_yticklabels(display_frequencies, fontsize=12)  

    ax.yaxis.label.set_size(14)
    ax.xaxis.label.set_size(14)

    ax.set_title('Spectrogram', fontsize=15)

     
def form_pitch_track(F0_estimate, ax, color='b', label=''):
    """
    Plots the F0_estimate on a given plt.ax
    """

    time_axis, F0 = F0_estimate
    markerline, stemlines, baseline = ax.stem(time_axis, F0, basefmt=" ", label=label)
    markerline.set_markerfacecolor(color)
    markerline.set_markersize(9)
    stemlines.set_linewidth(0)


def form_notes(ax, notes, unk_notes):

    scale_notes = list(notes.keys())
    oos_notes =  list(unk_notes.keys())

    for i, note_dict in enumerate(list(notes.values())):

        if note_dict['time']:
            note = scale_notes[i]
            form_pitch_track((note_dict['time'], note_dict['frequency']), ax, color=colors[i], label=note)

    for j, note_dict in enumerate(list(unk_notes.values())):

        if note_dict['time']:
            note = oos_notes[j]
            form_pitch_track((note_dict['time'], note_dict['frequency']), ax, color=unk_colors[j], label='{}-OOS'.format(note))       


def form_note_legend(ax, notes, unk_notes):
    """
    Formats the legend based on the number of notes
    """

    total_notes = len(notes.keys()) + len(unk_notes.keys())

    if total_notes > 10:
        ax.legend(loc=1, ncol=3, fontsize=15)
    elif total_notes > 6:
        ax.legend(loc=1, ncol=2, fontsize=15)
    else:
        ax.legend(loc=1, fontsize=15)


def save_function(save, plot_dir, title, plot_title='', default_title=''):
    """
    Saves the plot to a given directory with a given default plot title or the provided plot title.
    """

    os.makedirs(plot_dir, exist_ok=True)
  
    if save:
        if not plot_title:
            plt.savefig(os.path.join(plot_dir,'{}-{}.png'.format(title, default_title)))
        else:
            plt.savefig(os.path.join(plot_dir,'{}-{}.png'.format(title, plot_title)))  