""" Custom plots for the jupyter notebook """

import matplotlib.pyplot as plt
import numpy as np
import ompy as om
from matplotlib.legend_handler import HandlerTuple
from matplotlib.collections import PolyCollection


def ensemble_plot(ensemble, *, ax = None, vmin = None, vmax = None,
                  add_cbar = True, **kwargs):
    """ Plot matrices from ensemble

    Args:
        ensemble: Ensemble instance
        ax (optional): A matplotlib axis to plot onto.
        vmin (optional, float): The lower cutoff for colors.
        vmax (optional, float): The upper cutoff for colors.
        add_cbar (optional, bool): Whether to add a colorbar.
            Defaults to True.
        scale_by (optional, str): Which std matrix to set color
            limits by. Can be "raw", "unfolded", "firstgen" or "all".
            Defaults to "all".

    Returns:
        The matplotlib figure and axis
    """
    if ax is not None:
        if len(ax) < 3:
            raise ValueError("Three axes must be provided")
        fig = ax.figure
    else:
        fig, ax = plt.subplots(ncols=3, sharey=True, constrained_layout=True)

    raw = ensemble.raw
    unfolded = ensemble.unfolder(raw)
    firstgen = ensemble.first_generation_method(unfolded)

    # # mean values
    # raw = om.Matrix(np.mean(ensemble.raw_ensemble, axis=0),
    #                 Ex=ensemble.raw.Ex, Eg=ensemble.raw.Eg)
    # unfolded = om.Matrix(np.mean(ensemble.unfolded_ensemble, axis=0),
    #                      Ex=ensemble.raw.Ex,
    #                      Eg=ensemble.raw.Eg)
    # firstgen = om.Matrix(np.mean(ensemble.firstgen_ensemble, axis=0),
    #                      Ex=ensemble.firstgen.Ex,
    #                      Eg=ensemble.firstgen.Eg)

    extrema = lambda x: (np.min(x), np.max(x)) # noqa
    choices = [raw.values, unfolded.values, firstgen.values]
    counts_extrema = extrema([v for v in choices])

    vminset = True
    if vmin is None:
        vminset = False
        vmin = counts_extrema[0]
        vmin = 1 if vmin == 0 else vmin
    vmaxset = True
    if vmax is None:
        vmaxset = False
        vmax = counts_extrema[1]

    # Actual plotting
    raw.plot(ax=ax[0], title='(a) raw', add_cbar=False,
             vmin=vmin, vmax=vmax, **kwargs)
    unfolded.plot(ax=ax[1], title='(b) unfolded', add_cbar=False,
                  vmin=vmin, vmax=vmax, **kwargs)
    im, _, _ = firstgen.plot(ax=ax[2], title='(c) first-generation',
                             vmin=vmin, vmax=vmax, add_cbar=False, **kwargs)

    # Y labels only clutter
    ax[1].set_ylabel(None)
    ax[2].set_ylabel(None)

    # Handle the colorbar
    if add_cbar:
        fig.colorbar(im, extend='both')
#     fig.suptitle("Standard Deviation")
    return fig, ax


class HandlerTupleVertical(HandlerTuple):
    """Plots all the given Lines vertical stacked."""

    def __init__(self, **kwargs):
        """Run Base Handler."""
        HandlerTuple.__init__(self, **kwargs)
        self.base = HandlerTuple(**kwargs)

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        """Create artists (the symbol) for legend entry."""
        # How many lines are there.
        numlines = len(orig_handle)
        handler_map = legend.get_legend_handler_map()

        # divide the vertical space where the lines will go
        # into equal parts based on the number of lines
        height_y = (height / numlines)

        leglines = []
        for i, handle in enumerate(orig_handle):
            containspoly = False
            try:
                for subhandle in handle:
                    if isinstance(subhandle, PolyCollection):
                        containspoly = True
                        break
            except Exception:
                pass
            
            if containspoly:
                handler = self.base
                legline = handler.create_artists(legend, handle,
                                             xdescent,
                                             0*height,
                                             width,
                                             height,
                                             fontsize, trans)
            else:
                handler = legend.get_legend_handler(handler_map, handle)
                legline = handler.create_artists(legend, handle,
                                             xdescent,
                                             (3*i + 1)*height_y,
                                             width,
                                             2*height,
                                             fontsize, trans)
            leglines.extend(legline)
        return leglines
