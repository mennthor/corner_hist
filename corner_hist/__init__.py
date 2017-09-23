# coding: utf8

"""
Creates corner plots similar to github.com/dfm/corner.py which are a great way
to view MCMC chains for example.

Here, instead of giving data points, an already created histogram is put in.
This can be useful when only multidimensional histograms are available and we
quickly need to view all the 1D and 2D marginalizations.
"""

import numpy as _np
import matplotlib.pyplot as _plt
from matplotlib.colors import LogNorm


def corner_hist(h, bins, label=None, color="k", cmap="inferno",
                hist_args={}, hist2D_args={}):
    """
    Plot marginalized 1D and 2D disgtributions of given histogram.

    Parameter
    ---------
    h : array
        nD array with shape (nbins 1st dim, ..., nbins last dim).
    bins : list
        List of len nD. Each item is an arrays containing the bin borders in
        that dimension
    label : list of strings
        Axis label

    kwargs
    ------
    hist_args : dict
        Arguments passed to matplotlib 1D hist function
    hist2D_args : dict
        Arguments passed to matplotlib 2D hist function

    Returns
    -------
    fig, ax : matplotlib figure and axis object
        The figure object and array (nD x nD) of axes objects.
    """
    h = _np.atleast_1d(h)
    dim = len(h.shape)
    if dim != len(bins):
        raise ValueError("For each dimension a list of bins must be " +
                         "provided. Dimensionality of hist and bins doesn't " +
                         "match.")

    # Get bin mids for the "plot existing hist as weights trick"
    mids = []
    for b in bins:
        mids.append(0.5 * (b[:-1] + b[1:]))

    # Labels are manually handled further below
    fig, ax = _plt.subplots(dim, dim, sharex=False,
                            sharey=False, figsize=(4 * dim, 4 * dim))

    # First set correct axes limits
    for row in range(dim):
        for col in range(dim):
            if col > row:  # Uper diagonal is turned off
                ax[row, col].axis("off")
            else:
                ax[row, col].set_xlim(bins[col][0], bins[col][-1])
                if row != col:
                    # 2D case: y limits are set with respect to bins
                    ax[row, col].set_ylim(bins[row][0], bins[row][-1])
                else:
                    # Set ticks right in 1D to distinguish from 2D yaxis
                    ax[row, col].yaxis.tick_right()

    # Diagonal is 1D, else are 2D marginalization = sum over all remaining dims
    for row in range(dim):
        for col in range(row + 1):
            if row == col:
                # For the 1D case we sum over n-1 dimensions
                axis = _np.ones(dim, dtype=bool)
                axis[row] = False

                axis = tuple(_np.arange(dim)[axis])
                hist = _np.sum(h, axis=axis)

                ax[row, col].hist(mids[row], bins=bins[row], weights=hist,
                                  **hist_args)
            else:
                # For the 2D case we sum over n-2 dimensions
                xx, yy = _np.meshgrid(mids[col], mids[row])
                XX = xx.flatten()
                YY = yy.flatten()
                axis = _np.ones(dim, dtype=bool)

                axis[row] = False
                axis[col] = False
                axis = tuple(_np.arange(dim)[axis])
                # We need to transpose, because dimensions are swapped between
                # meshgrid and numpy.histogrammdd
                hflat = _np.sum(h, axis=axis).T.flatten()

                ax[row, col].hist2d(XX, YY, bins=[bins[col], bins[row]],
                                    weights=hflat, **hist2D_args)

    # Set axis label
    if label is not None:
        for col in range(dim):
            ax[-1, col].set_xlabel(label[col])
            ax[col, col].set_ylabel("counts")
            ax[col, col].yaxis.set_label_position("right")
        for row in range(1, dim):
            ax[row, 0].set_ylabel(label[row])

    # Rotate lower xticklabel so they don't interfere
    for col in range(dim):
        for label in ax[-1, col].get_xticklabels():
            label.set_rotation(60)

    # Unset x label and ticks manually for internal axes
    if dim > 1:
        for row in range(0, dim - 1):
            for col in range(0, row + 1):
                ax[row, col].get_xaxis().set_ticklabels([])

        # Unset y label and ticks manually for internal axes.
        for row in range(1, dim):
            for col in range(1, row):
                ax[row, col].get_yaxis().set_ticklabels([])

    # Make plots square. Set aspect needs the correct ratio.
    # "Equal" just equals the axis range
    for row in range(dim):
        for col in range(dim):
            ax[row, col].set_aspect(1. / ax[row, col].get_data_ratio())

    fig.tight_layout(h_pad=-1, w_pad=-3)

    return fig, ax
