"""
Matplotlib Backend for HyperTools

This module provides the core matplotlib plotting functionality for hypertools,
supporting both 2D and 3D static and animated visualizations.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.collections as mcoll
import matplotlib.colors as mcolors
import seaborn as sns
from typing import Union, Optional, List, Tuple, Dict, Any
import warnings

# Set matplotlib style
plt.style.use('seaborn-v0_8-white')


class HyperToolsPlot:
    """
    Main plotting class for matplotlib backend.
    
    This class handles all static and animated plotting functionality,
    providing a consistent API for 2D and 3D visualizations.
    """
    
    def __init__(self, fig=None, ax=None, ndim=None):
        """
        Initialize HyperToolsPlot.
        
        Parameters
        ----------
        fig : matplotlib.figure.Figure, optional
            Existing figure to use
        ax : matplotlib.axes.Axes, optional
            Existing axes to use
        ndim : int, optional
            Number of dimensions (2 or 3)
        """
        self.fig = fig
        self.ax = ax
        self.ndim = ndim
        self._bounds = None
        
    def setup_axes(self, data, fig=None, ax=None, ndim=None):
        """
        Set up matplotlib figure and axes.
        
        Parameters
        ----------
        data : array-like or list of array-like
            Data to plot
        fig : matplotlib.figure.Figure, optional
            Existing figure
        ax : matplotlib.axes.Axes, optional
            Existing axes
        ndim : int, optional
            Force number of dimensions
            
        Returns
        -------
        fig, ax : matplotlib figure and axes objects
        """
        # Determine dimensionality
        if ndim is None:
            if isinstance(data, list):
                ndim = data[0].shape[1] if data[0].shape[1] <= 3 else 3
            else:
                ndim = data.shape[1] if data.shape[1] <= 3 else 3
        
        self.ndim = ndim
        
        # Create figure and axes if not provided
        if fig is None and ax is None:
            if ndim == 3:
                self.fig = plt.figure(figsize=(10, 8))
                self.ax = self.fig.add_subplot(111, projection='3d')
            else:
                self.fig, self.ax = plt.subplots(figsize=(10, 8))
        else:
            self.fig = fig if fig is not None else (ax.figure if ax is not None else plt.figure())
            self.ax = ax if ax is not None else (self.fig.add_subplot(111, projection='3d' if ndim == 3 else None))
            
        # Calculate and store bounds for consistent scaling
        self._calculate_bounds(data)
        self._apply_bounds()
        
        return self.fig, self.ax
    
    def _calculate_bounds(self, data):
        """Calculate axis bounds from data."""
        if isinstance(data, list):
            all_data = np.vstack([d.values if hasattr(d, 'values') else d for d in data])
        else:
            all_data = data.values if hasattr(data, 'values') else data
            
        # Add padding to bounds
        padding = 0.05
        mins = np.nanmin(all_data, axis=0)
        maxs = np.nanmax(all_data, axis=0)
        ranges = maxs - mins
        
        self._bounds = {
            'x': [mins[0] - padding * ranges[0], maxs[0] + padding * ranges[0]],
            'y': [mins[1] - padding * ranges[1], maxs[1] + padding * ranges[1]]
        }
        
        if self.ndim == 3 and all_data.shape[1] >= 3:
            self._bounds['z'] = [mins[2] - padding * ranges[2], maxs[2] + padding * ranges[2]]
    
    def _apply_bounds(self):
        """Apply calculated bounds to axes."""
        if self._bounds:
            self.ax.set_xlim(self._bounds['x'])
            self.ax.set_ylim(self._bounds['y'])
            if self.ndim == 3 and 'z' in self._bounds:
                self.ax.set_zlim(self._bounds['z'])
    
    def plot_data(self, data, mode='markers', color=None, marker='o', markersize=6,
                  linewidth=1.5, alpha=1.0, label=None, **kwargs):
        """
        Plot data using matplotlib.
        
        Parameters
        ----------
        data : pd.DataFrame or np.ndarray
            Data to plot (n_samples x n_dims)
        mode : str
            Plot mode: 'markers', 'lines', 'lines+markers', 'text'
        color : str or array-like
            Color specification
        marker : str
            Marker style
        markersize : float
            Marker size
        linewidth : float
            Line width
        alpha : float
            Transparency
        label : str
            Legend label
        **kwargs : dict
            Additional plotting arguments
            
        Returns
        -------
        artists : list
            List of matplotlib artists created
        """
        # Convert data to numpy array
        if hasattr(data, 'values'):
            points = data.values
        else:
            points = np.asarray(data)
            
        # Ensure we have at least 2D data
        if points.ndim == 1:
            points = points.reshape(-1, 1)
            
        # Pad to required dimensions
        if points.shape[1] < self.ndim:
            padding = np.zeros((points.shape[0], self.ndim - points.shape[1]))
            points = np.hstack([points, padding])
        
        artists = []
        
        # Handle color specification
        if color is None:
            color = 'C0'  # Default matplotlib color
        elif isinstance(color, (list, np.ndarray)) and len(color) == points.shape[0]:
            # Per-point colors - need to handle specially
            pass
        
        # Plot based on mode
        if self.ndim == 3:
            if 'markers' in mode and 'lines' in mode:
                # Plot both lines and markers
                line = self.ax.plot(points[:, 0], points[:, 1], points[:, 2],
                                   color=color if isinstance(color, str) else 'C0',
                                   linewidth=linewidth, alpha=alpha, label=label)[0]
                scatter = self.ax.scatter(points[:, 0], points[:, 1], points[:, 2],
                                        c=color, marker=marker, s=markersize**2,
                                        alpha=alpha)
                artists.extend([line, scatter])
            elif 'lines' in mode:
                # Plot lines only
                line = self.ax.plot(points[:, 0], points[:, 1], points[:, 2],
                                   color=color if isinstance(color, str) else 'C0',
                                   linewidth=linewidth, alpha=alpha, label=label)[0]
                artists.append(line)
            else:  # markers
                # Plot markers only
                scatter = self.ax.scatter(points[:, 0], points[:, 1], points[:, 2],
                                        c=color, marker=marker, s=markersize**2,
                                        alpha=alpha, label=label)
                artists.append(scatter)
        else:  # 2D
            if 'markers' in mode and 'lines' in mode:
                # Plot both lines and markers
                line = self.ax.plot(points[:, 0], points[:, 1],
                                   color=color if isinstance(color, str) else 'C0',
                                   linewidth=linewidth, alpha=alpha, label=label)[0]
                scatter = self.ax.scatter(points[:, 0], points[:, 1],
                                        c=color, marker=marker, s=markersize**2,
                                        alpha=alpha)
                artists.extend([line, scatter])
            elif 'lines' in mode:
                # Plot lines only
                line = self.ax.plot(points[:, 0], points[:, 1],
                                   color=color if isinstance(color, str) else 'C0',
                                   linewidth=linewidth, alpha=alpha, label=label)[0]
                artists.append(line)
            else:  # markers
                # Plot markers only
                scatter = self.ax.scatter(points[:, 0], points[:, 1],
                                        c=color, marker=marker, s=markersize**2,
                                        alpha=alpha, label=label)
                artists.append(scatter)
                
        return artists
    
    def style_axes(self, xlabel=None, ylabel=None, zlabel=None, title=None,
                   ticklabels=True, legend=False, **kwargs):
        """
        Style the plot axes.
        
        Parameters
        ----------
        xlabel, ylabel, zlabel : str, optional
            Axis labels
        title : str, optional
            Plot title
        ticklabels : bool
            Whether to show tick labels
        legend : bool or dict
            Whether to show legend or legend kwargs
        **kwargs : dict
            Additional styling arguments
        """
        # Set labels
        if xlabel:
            self.ax.set_xlabel(xlabel)
        if ylabel:
            self.ax.set_ylabel(ylabel)
        if zlabel and self.ndim == 3:
            self.ax.set_zlabel(zlabel)
        if title:
            self.ax.set_title(title)
            
        # Handle tick labels
        if not ticklabels:
            self.ax.set_xticklabels([])
            self.ax.set_yticklabels([])
            if self.ndim == 3:
                self.ax.set_zticklabels([])
                
        # Handle legend
        if legend:
            if isinstance(legend, dict):
                self.ax.legend(**legend)
            else:
                self.ax.legend()
                
        # Apply any additional styling
        for key, value in kwargs.items():
            if hasattr(self.ax, f'set_{key}'):
                getattr(self.ax, f'set_{key}')(value)


def plot_matplotlib(data, fmt=None, fig=None, ax=None, animate=None,
                   legend=None, labels=None, **kwargs):
    """
    Main matplotlib plotting function.
    
    Parameters
    ----------
    data : array-like or list of array-like
        Data to plot
    fmt : str or list of str, optional
        Format strings for each dataset
    fig : matplotlib.figure.Figure, optional
        Existing figure to use
    ax : matplotlib.axes.Axes, optional
        Existing axes to use
    animate : dict, optional
        Animation parameters
    legend : bool or dict, optional
        Legend parameters
    labels : list of str, optional
        Labels for each dataset
    **kwargs : dict
        Additional plotting parameters
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object
    """
    # Initialize plotter
    plotter = HyperToolsPlot()
    
    # Ensure data is a list
    if not isinstance(data, list):
        data = [data]
        
    # Parse format strings
    if fmt is not None:
        if not isinstance(fmt, list):
            fmt = [fmt]
        # Extend fmt to match data length if needed
        if len(fmt) < len(data):
            fmt = fmt + [None] * (len(data) - len(fmt))
    else:
        fmt = [None] * len(data)
    
    # Set up axes
    fig, ax = plotter.setup_axes(data, fig=fig, ax=ax)
    
    # Extract plotting parameters
    mode = kwargs.pop('mode', 'markers')
    color = kwargs.pop('color', None)
    marker = kwargs.pop('marker', 'o')
    markersize = kwargs.pop('markersize', 6)
    linewidth = kwargs.pop('linewidth', 1.5)
    alpha = kwargs.pop('alpha', 1.0)
    
    # Handle colors for multiple datasets
    if color is None:
        # Use default color cycle
        colors = [f'C{i}' for i in range(len(data))]
    elif isinstance(color, list) and len(color) == len(data):
        colors = color
    else:
        colors = [color] * len(data)
    
    # Plot each dataset
    for i, (dataset, fmt_str, c) in enumerate(zip(data, fmt, colors)):
        # Parse format string if provided
        if fmt_str:
            parsed = parse_format_string(fmt_str)
            plot_mode = parsed.get('mode', mode)
            plot_color = parsed.get('color', c)
            plot_marker = parsed.get('marker', marker)
            plot_linestyle = parsed.get('linestyle', '-')
        else:
            plot_mode = mode
            plot_color = c
            plot_marker = marker
            plot_linestyle = '-'
            
        # Get label
        if labels and i < len(labels):
            label = labels[i]
        elif legend and len(data) > 1:
            label = f'Dataset {i+1}'
        else:
            label = None
            
        # Plot data
        plotter.plot_data(dataset, mode=plot_mode, color=plot_color,
                         marker=plot_marker, markersize=markersize,
                         linewidth=linewidth, alpha=alpha, label=label,
                         linestyle=plot_linestyle)
    
    # Style axes
    plotter.style_axes(legend=legend, **kwargs)
    
    # Handle animation if requested
    if animate:
        return create_animation(fig, ax, data, animate, plotter, **kwargs)
    
    return fig


def parse_format_string(fmt):
    """
    Parse matplotlib format string.
    
    Parameters
    ----------
    fmt : str
        Format string like 'ro-', 'b--', etc.
        
    Returns
    -------
    dict
        Parsed format parameters
    """
    result = {}
    
    # Color codes
    colors = {'b': 'blue', 'g': 'green', 'r': 'red', 'c': 'cyan',
              'm': 'magenta', 'y': 'yellow', 'k': 'black', 'w': 'white'}
    
    # Marker codes
    markers = {'.': '.', ',': ',', 'o': 'o', 'v': 'v', '^': '^',
               '<': '<', '>': '>', '1': '1', '2': '2', '3': '3',
               '4': '4', '8': '8', 's': 's', 'p': 'p', 'P': 'P',
               '*': '*', 'h': 'h', 'H': 'H', '+': '+', 'x': 'x',
               'X': 'X', 'd': 'd', 'D': 'D', '|': '|', '_': '_'}
    
    # Line styles
    linestyles = {'-': '-', '--': '--', '-.': '-.', ':': ':'}
    
    # Parse color
    for char, color in colors.items():
        if char in fmt:
            result['color'] = color
            fmt = fmt.replace(char, '', 1)
            break
    
    # Parse marker
    for char, marker in markers.items():
        if char in fmt:
            result['marker'] = marker
            fmt = fmt.replace(char, '', 1)
            break
    
    # Parse line style
    for style_str, style in sorted(linestyles.items(), key=lambda x: -len(x[0])):
        if style_str in fmt:
            result['linestyle'] = style
            fmt = fmt.replace(style_str, '', 1)
            break
    
    # Determine mode
    has_line = 'linestyle' in result
    has_marker = 'marker' in result
    
    if has_line and has_marker:
        result['mode'] = 'lines+markers'
    elif has_line:
        result['mode'] = 'lines'
    elif has_marker:
        result['mode'] = 'markers'
    
    return result


def create_animation(fig, ax, data, animate_params, plotter, **kwargs):
    """
    Create matplotlib animation.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object
    ax : matplotlib.axes.Axes
        Axes object
    data : list of array-like
        Data to animate
    animate_params : dict
        Animation parameters
    plotter : HyperToolsPlot
        Plotter instance
    **kwargs : dict
        Additional parameters
        
    Returns
    -------
    anim : matplotlib.animation.FuncAnimation
        Animation object
    """
    # This is a placeholder - full animation implementation
    # will be done when updating animate.py
    warnings.warn("Animation not yet fully implemented in matplotlib backend")
    return fig