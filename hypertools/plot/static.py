# noinspection PyPackageRequirements
import datawrangler as dw
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ..core import get_default_options, eval_dict, get, fullfact

defaults = eval_dict(get_default_options()['plot'])


def match_color(img, c):
    img = np.atleast_2d(img)
    c = np.atleast_2d(c)

    if np.ndim(img) == 3:
        all_inds = np.squeeze(np.zeros_like(img)[:, :, 0])
    else:
        all_inds = np.squeeze(np.zeros_like(img[:, 0]))
    for i in range(c.shape[0]):
        # noinspection PyShadowingNames
        inds = np.zeros_like(img)
        for j in range(c.shape[1]):
            if np.ndim(img) == 3:
                inds[:, :, j] = np.isclose(img[:, :, j], c[i, j])
            else:
                inds[:, j] = np.isclose(img[:, j], c[i, j])

        all_inds = (all_inds + (np.sum(inds, axis=np.ndim(img) - 1) == c.shape[1])) > 0
    return np.where(all_inds)


def group_mean(x):
    @dw.decorate.apply_unstacked
    def helper(y):
        return pd.DataFrame(y.mean(axis=0)).T

    means = helper(x)
    if hasattr(means.index, 'levels'):
        n_levels = len(means.index.levels)
        if n_levels > 1:
            index = pd.MultiIndex.from_frame(means.index.to_frame().iloc[:, :-1])
            return pd.DataFrame(data=means.values, columns=means.columns, index=index)
    return means


def get_continuous_inds(x):
    x = np.sort(x.ravel())
    diffs = np.diff(x)
    breaks = np.where(diffs > 1)[0]
    if len(breaks) == 0:
        return [x]
    else:
        breaks = np.concatenate([[0], breaks + 1, [len(x)]])
        return [x[breaks[i]:breaks[i + 1]] for i in range(len(breaks) - 1)]


def get_empty_canvas(fig=None, ax=None, projection=None, figsize=(10, 8)):
    """Create empty matplotlib figure and axes."""
    if fig is None and ax is None:
        fig = plt.figure(figsize=figsize)
        if projection == '3d':
            ax = fig.add_subplot(111, projection='3d')
        else:
            ax = fig.add_subplot(111)
    elif ax is None:
        if projection == '3d':
            ax = fig.add_subplot(111, projection='3d')
        else:
            ax = fig.add_subplot(111)
    elif fig is None:
        fig = ax.figure
    
    # Style the axes
    ax.set_facecolor('#F8F8F9')
    if projection != '3d':
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    return fig, ax


def normalize_color(c):
    """Normalize color to matplotlib format."""
    if isinstance(c, list):
        return [normalize_color(i) for i in c]
    elif isinstance(c, str):
        return c  # Already a valid color string
    elif isinstance(c, (tuple, np.ndarray)):
        # Ensure RGB values are in [0, 1] range
        c = np.array(c)
        if c.max() > 1.0:
            c = c / 255.0
        return mpl.colors.to_hex(c)
    else:
        return c


def get_bounds(data):
    x = dw.stack(data)
    return np.vstack([np.nanmin(x, axis=0), np.nanmax(x, axis=0)])


def expand_range(x, b=0.025):
    length = np.max(x) - np.min(x)
    return [np.min(x) - b * length, np.max(x) + b * length]


def plot_bounding_box(bounds, color='k', linewidth=2, alpha=0.9, fig=None, ax=None, buffer=0.025):
    """Plot bounding box using matplotlib."""
    n_dims = bounds.shape[1]
    assert n_dims in [2, 3], ValueError(f'only 2D or 3D coordinates are supported; given: {n_dims}D')
    
    if fig is None or ax is None:
        fig, ax = get_empty_canvas(projection='3d' if n_dims == 3 else None)
    
    n_vertices = np.power(2, n_dims)
    lengths = np.abs(np.diff(bounds, axis=0))
    vertices = fullfact(n_dims * [2]) - 1
    vertices = np.multiply(vertices, np.repeat(lengths, n_vertices, axis=0))
    vertices += np.repeat(np.atleast_2d(np.min(bounds, axis=0)), n_vertices, axis=0)
    
    # Draw edges
    for i in range(n_vertices):
        for j in range(i):
            # Check for adjacent vertex (match every coordinate except 1)
            if np.sum([a == b for a, b in zip(vertices[i], vertices[j])]) == n_dims - 1:
                if n_dims == 3:
                    ax.plot([vertices[i][0], vertices[j][0]],
                           [vertices[i][1], vertices[j][1]],
                           [vertices[i][2], vertices[j][2]],
                           color=color, linewidth=linewidth, alpha=alpha)
                else:
                    ax.plot([vertices[i][0], vertices[j][0]],
                           [vertices[i][1], vertices[j][1]],
                           color=color, linewidth=linewidth, alpha=alpha)
    
    # Set axis limits
    ax.set_xlim(expand_range(bounds[:, 0], b=buffer))
    ax.set_ylim(expand_range(bounds[:, 1], b=buffer))
    if n_dims == 3:
        ax.set_zlim(expand_range(bounds[:, 2], b=buffer))
    
    return fig, ax


# noinspection PyIncorrectDocstring
def flatten(y, depth=0):
    """
    Turn an array, series, or dataframe into a flat list

    Parameters
    ----------
    :param y: the object to flatten
    Returns
    -------
    :return: the flattened object
    """
    if type(y) is list:
        if len(y) == 1:
            return [flatten(y[0], depth=depth + 1)]
        else:
            return [flatten(i, depth=depth + 1) for i in y]
    elif (not np.isscalar(y)) and dw.zoo.is_array(y):
        return flatten(y.ravel().tolist(), depth=depth + 1)
    elif dw.zoo.is_dataframe(y):
        return flatten(y.values, depth=depth + 1)
    else:
        if depth == 0:
            return [y]
        else:
            return y


def plot_data_matplotlib(ax, x, mode='markers', color=None, linewidth=1.5, markersize=6,
                        marker='o', linestyle='-', alpha=1.0, label=None, **kwargs):
    """Plot data using matplotlib."""
    x = np.asarray(x)
    
    if x.shape[1] == 2:
        if 'lines' in mode and 'markers' in mode:
            ax.plot(x[:, 0], x[:, 1], color=color, linewidth=linewidth,
                   marker=marker, markersize=markersize, linestyle=linestyle,
                   alpha=alpha, label=label, **kwargs)
        elif 'lines' in mode:
            ax.plot(x[:, 0], x[:, 1], color=color, linewidth=linewidth,
                   linestyle=linestyle, alpha=alpha, label=label, **kwargs)
        else:  # markers
            ax.scatter(x[:, 0], x[:, 1], c=color, s=markersize**2,
                      marker=marker, alpha=alpha, label=label, **kwargs)
    elif x.shape[1] == 3:
        if 'lines' in mode and 'markers' in mode:
            ax.plot(x[:, 0], x[:, 1], x[:, 2], color=color, linewidth=linewidth,
                   marker=marker, markersize=markersize, linestyle=linestyle,
                   alpha=alpha, label=label, **kwargs)
        elif 'lines' in mode:
            ax.plot(x[:, 0], x[:, 1], x[:, 2], color=color, linewidth=linewidth,
                   linestyle=linestyle, alpha=alpha, label=label, **kwargs)
        else:  # markers
            ax.scatter(x[:, 0], x[:, 1], x[:, 2], c=color, s=markersize**2,
                      marker=marker, alpha=alpha, label=label, **kwargs)
    else:
        raise ValueError(f'data must be 2D or 3D (given: {x.shape[1]}D)')


def static_plot(data, fig=None, ax=None, **kwargs):
    """Static plotting with matplotlib."""
    kwargs = dw.core.update_dict(defaults, kwargs)
    
    # Extract parameters
    color = kwargs.pop('color', None)
    mode = kwargs.pop('mode', 'markers')
    linewidth = kwargs.pop('linewidth', 1.5)
    markersize = kwargs.pop('markersize', 6)
    marker = kwargs.pop('marker', 'o')
    linestyle = kwargs.pop('linestyle', '-')
    alpha = kwargs.pop('alpha', 1.0)
    showlegend = kwargs.pop('showlegend', True)
    
    # Determine dimensionality
    if isinstance(data, list):
        ndim = data[0].shape[1] if data[0].shape[1] <= 3 else 3
    else:
        ndim = data.shape[1] if data.shape[1] <= 3 else 3
    
    # Create figure and axes if needed
    if fig is None or ax is None:
        fig, ax = get_empty_canvas(projection='3d' if ndim == 3 else None)
    
    # Handle list of datasets
    if isinstance(data, list):
        names = kwargs.pop('name', [f'Dataset {i+1}' for i in range(len(data))])
        for i, d in enumerate(data):
            c = get(color, i) if color is not None else f'C{i}'
            label = names[i] if showlegend else None
            plot_data_matplotlib(ax, d, mode=mode, color=c, linewidth=linewidth,
                               markersize=markersize, marker=marker, linestyle=linestyle,
                               alpha=alpha, label=label)
    else:
        # Single dataset
        if color is None:
            color = 'C0'
        elif isinstance(color, (list, np.ndarray)) and len(color) == data.shape[0]:
            # Per-point colors
            unique_colors = np.unique(color, axis=0)
            for uc in unique_colors:
                c_inds = match_color(color, uc)[0]
                for inds in get_continuous_inds(c_inds):
                    if len(inds) == 1:
                        inds = np.array([inds[0], min(inds[0] + 1, data.shape[0] - 1)])
                    plot_data_matplotlib(ax, data.values[inds, :] if hasattr(data, 'values') else data[inds, :],
                                       mode=mode, color=normalize_color(uc), linewidth=linewidth,
                                       markersize=markersize, marker=marker, linestyle=linestyle,
                                       alpha=alpha)
        else:
            # Single color for all points
            plot_data_matplotlib(ax, data, mode=mode, color=color, linewidth=linewidth,
                               markersize=markersize, marker=marker, linestyle=linestyle,
                               alpha=alpha)
    
    # Show legend if requested
    if showlegend and ax.get_legend_handles_labels()[0]:
        ax.legend()
    
    return fig, ax
