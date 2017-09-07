"""Create data plots for ERP-SCANR project - plots for group analysis."""

import os
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hier

from erpsc.core.db import check_db

#########################################################################################
#########################################################################################
#########################################################################################

def plot_time_assocs(dat, save_fig=False):
    """Plot top associations for each ERP across time.

    Parameters
    ----------
    dat : list of list of [str, str, int]
        ERP data - [association, P or N, latency]
    """

    # Plot params
    offsets = {'P': 50, 'N': -50}
    rotations = {'P': 45, 'N': -45}

    # Initialize Plot
    fig = plt.figure(figsize=(12, 5))
    fig.suptitle('ERP Correlates Across Time', fontsize=24, fontweight='bold')
    ax = fig.add_subplot(111)

    # Set plot limits
    ax.set_xlim([50, 600])
    ax.set_ylim([-100, 100])

    # Add x-ticks
    plt.xticks([250, 500], ['250 ms', '500 ms'])
    ax.set_yticks([])

    # Set ticks and plot lines
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)

    # Add data to plot from
    for d in dat:

        # Text takes: [X-pos, Y-pos, word, rotation]
        #  Where X-pos is latency, y-pos & rotation are defaults given +/-
        ax.text(d[2], offsets[d[1]], d[0], rotation=rotations[d[1]], fontsize=20)

    # Save out - if requested
    if save_fig:

        db = check_db(db)
        s_file = os.path.join(db.figs_path, 'LatencyAssociations' + '.svg')

        plt.savefig(s_file, transparent=True)


def plot_matrix(dat, x_labels, y_labels, square=False, figsize=(10, 12), save_fig=False, save_name='Matrix'):
    """Plot the matrix of percent asscociations between ERPs & terms."""

    f, ax = plt.subplots(figsize=figsize)

    sns.heatmap(dat, square=square, xticklabels=x_labels, yticklabels=y_labels)

    f.tight_layout()

    # Save out - if requested
    if save_fig:

        db = check_db(db)
        s_file = os.path.join(db.figs_path, save_name + '.svg')

        plt.savefig(s_file)


def plot_clustermap(dat, cmap='purple', save_fig=False, save_name='Clustermap'):
    """Plot clustermap.

    Parameters
    ----------
    dat : pandas.DataFrame
        Data to create clustermap from.
    """

    # Set up plotting and aesthetics
    sns.set()
    sns.set_context("paper", font_scale=1.5)

    # Set colourmap
    if cmap == 'purple':
        cmap = sns.cubehelix_palette(as_cmap=True)
    elif cmap == 'blue':
        cmap = sns.cubehelix_palette(as_cmap=True, rot=-.3, light=0.9, dark=0.2)

    # Create the clustermap
    cg = sns.clustermap(dat, cmap=cmap, method='complete', metric='cosine', figsize=(12, 10))

    # Fix axes
    cg.cax.set_visible(True)
    _ = plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=60, ha='right')
    _ = plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)

    # Save out - if requested
    if save_fig:

        db = check_db(db)
        s_file = os.path.join(db.figs_path, save_name + '.svg')

        cg.savefig(s_file, transparent=True)


def plot_dendrogram(dat, labels, save_fig=False, save_name='Dendrogram'):
    """Plot dendrogram."""

    plt.figure(figsize=(3, 15))

    Y = hier.linkage(dat, method='complete', metric='cosine')

    Z = hier.dendrogram(Y, orientation='left', labels=labels,
                        color_threshold=0.25, leaf_font_size=12)

    # Save out - if requested
    if save_fig:

        db = check_db(db)
        s_file = os.path.join(db.figs_path, save_name + '.svg')

        cg.savefig(s_file, transparent=True)
