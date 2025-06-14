"""
Three.js Backend for HyperTools

Unified Three.js rendering system providing both 2D and 3D visualization
with interactive capabilities and matplotlib conversion.
"""

import numpy as np
import pandas as pd
import pythreejs as p3js
from typing import Union, Optional, Any, Dict, List
import pickle
import warnings
import re
from scipy.interpolate import interp1d
import matplotlib.colors as mcolors
import seaborn as sns

def rgb_to_hex(rgb):
    """Convert RGB array to hex color string for Three.js"""
    if isinstance(rgb, str):
        return rgb  # Already a color string
    
    # Ensure RGB values are in [0, 1] range
    rgb = np.array(rgb)
    if rgb.max() > 1.0:
        rgb = rgb / 255.0
    
    # Convert to hex
    return mcolors.to_hex(rgb)

def mat2colors_threejs(m, **kwargs):
    """
    Three.js-compatible version of mat2colors
    
    Converts data matrix to HTML color strings suitable for Three.js materials.
    """
    # Handle different input types
    if isinstance(m, str):
        return rgb_to_hex(mcolors.to_rgb(m))
    elif isinstance(m, list):
        # Handle list of datasets
        colors = []
        for item in m:
            colors.append(mat2colors_threejs(item, **kwargs))
        return colors
    
    # Get color palette
    cmap_name = kwargs.get('cmap', 'viridis')
    n_colors = kwargs.get('n_colors', 250)
    
    try:
        cmap = sns.color_palette(cmap_name, n_colors=n_colors, as_cmap=False)
        cmap = np.array(cmap)
    except:
        # Fallback to matplotlib colormap
        cmap = np.array(sns.color_palette('viridis', n_colors=n_colors))
    
    # Convert data to numpy array
    m = np.squeeze(np.array(m))
    
    if m.ndim < 2:
        # 1D data - map to color palette
        if len(np.unique(m)) == 1:
            # Single value - return single color
            return rgb_to_hex(cmap[0])
        
        # Normalize to [0, n_colors-1] range
        m_norm = (m - m.min()) / (m.max() - m.min()) if m.max() != m.min() else np.zeros_like(m)
        color_indices = (m_norm * (n_colors - 1)).astype(int)
        
        # Return list of hex colors
        return [rgb_to_hex(cmap[i]) for i in color_indices]
    
    else:
        # Multi-dimensional data - use first 3 components for RGB
        # This is a simplified version - full implementation would reduce dimensionality
        if m.shape[1] >= 3:
            rgb = m[:, :3]
        else:
            # Pad with zeros if needed
            rgb = np.column_stack([m, np.zeros((m.shape[0], 3 - m.shape[1]))])
        
        # Normalize RGB values to [0, 1]
        for i in range(3):
            col = rgb[:, i]
            if col.max() != col.min():
                rgb[:, i] = (col - col.min()) / (col.max() - col.min())
        
        # Convert to hex colors
        return [rgb_to_hex(rgb[i]) for i in range(rgb.shape[0])]

def labels2colors_threejs(labels, **kwargs):
    """
    Three.js-compatible version of labels2colors
    
    Converts categorical labels to HTML color strings.
    """
    # Handle different input types
    if isinstance(labels, list):
        labels = np.array(labels)
    
    # Get unique labels
    unique_labels = np.unique(labels)
    n_labels = len(unique_labels)
    
    # Get color palette
    cmap_name = kwargs.get('cmap', 'viridis')
    try:
        cmap = sns.color_palette(cmap_name, n_colors=n_labels, as_cmap=False)
        cmap = np.array(cmap)
    except:
        cmap = np.array(sns.color_palette('Set1', n_colors=min(n_labels, 9)))
    
    # Create label to color mapping
    label_to_color = {}
    for i, label in enumerate(unique_labels):
        color_idx = i % len(cmap)
        label_to_color[label] = rgb_to_hex(cmap[color_idx])
    
    # Map labels to colors
    colors = [label_to_color[label] for label in labels]
    
    return colors, label_to_color

class HyperToolsFigure:
    """
    Universal figure object using Three.js backend
    
    This class encapsulates all plot data and provides methods for:
    - Interactive display via Three.js
    - Export to various formats (SVG, PNG, HTML)
    - Conversion to matplotlib for fine-tuning
    - Persistence (save/load figure objects)
    """
    
    def __init__(self, data: Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]], 
                 fmt: Union[str, List[str]] = None, **kwargs):
        """
        Initialize HyperTools figure with Three.js backend
        
        Parameters
        ----------
        data : DataFrame, ndarray, or list of DataFrames/ndarrays
            Input data for plotting. If list, each element is a separate dataset.
        fmt : str or list of str, optional
            Matplotlib-style format strings (e.g., 'ro-', 'b--', 'g:')
            If list, must match length of data list.
        **kwargs : dict
            Additional plotting parameters (linewidth, markersize, etc.)
        """
        # Handle multiple datasets
        if isinstance(data, list):
            self.datasets = [self._standardize_data(d) for d in data]
            self.n_datasets = len(self.datasets)
        else:
            self.datasets = [self._standardize_data(data)]
            self.n_datasets = 1
        
        # Parse format strings and kwargs
        self.plot_styles = self._parse_plot_styles(fmt, **kwargs)
        self.kwargs = kwargs
        
        # Three.js objects
        self.scene = None
        self.camera = None
        self.renderer = None
        self.controls = None
        
        # Plot properties  
        self.dimensionality = self._detect_dimensionality()
        self.is_animated = kwargs.get('animate', False)
        
        # Create the Three.js plot
        self._create_threejs_plot()
    
    def _standardize_data(self, data: Union[pd.DataFrame, np.ndarray]) -> pd.DataFrame:
        """Convert input data to standard DataFrame format"""
        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                # 1D array - assume y values, create x values
                df = pd.DataFrame({
                    'x': np.arange(len(data)),
                    'y': data
                })
            elif data.ndim == 2:
                if data.shape[1] == 2:
                    df = pd.DataFrame(data, columns=['x', 'y'])
                elif data.shape[1] == 3:
                    df = pd.DataFrame(data, columns=['x', 'y', 'z'])
                else:
                    raise ValueError(f"Unsupported data shape: {data.shape}")
            else:
                raise ValueError(f"Unsupported data dimensions: {data.ndim}")
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
            # Ensure we have standard column names
            if df.shape[1] >= 2:
                # Rename columns to standard format
                if df.shape[1] == 2:
                    df.columns = ['x', 'y']
                elif df.shape[1] == 3:
                    df.columns = ['x', 'y', 'z']
                elif df.shape[1] > 3:
                    # Take first 3 dimensions and rename
                    df = df.iloc[:, :3]
                    df.columns = ['x', 'y', 'z']
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")
        
        return df
    
    def _parse_plot_styles(self, fmt: Union[str, List[str]], **kwargs) -> List[Dict]:
        """Parse matplotlib-style format strings and kwargs into plot styles"""
        # Default style (line plot as requested)
        default_style = {
            'linestyle': 'solid',
            'marker': None,
            'color': 'black',
            'linewidth': 2,
            'markersize': 8,
            'alpha': 0.8,
            'interpolation_samples': 100
        }
        
        styles = []
        
        for i in range(self.n_datasets):
            style = default_style.copy()
            
            # Get format string for this dataset
            if fmt is None:
                fmt_str = None
            elif isinstance(fmt, str):
                fmt_str = fmt
            elif isinstance(fmt, list):
                fmt_str = fmt[i] if i < len(fmt) else None
            else:
                fmt_str = None
            
            # Parse format string
            if fmt_str:
                parsed = self._parse_format_string(fmt_str)
                style.update(parsed)
            
            # Handle single datapoint case
            dataset = self.datasets[i]
            if len(dataset) == 1:
                style['linestyle'] = None
                style['marker'] = 'o'
                style['markersize'] = 12  # Larger for single points
            
            # Override with kwargs
            for key, value in kwargs.items():
                if key in style:
                    if isinstance(value, list):
                        style[key] = value[i] if i < len(value) else value[0]
                    else:
                        style[key] = value
            
            # Ensure we always have a valid color
            if style['color'] is None:
                style['color'] = 'black'
            
            # Handle color lists from mat2colors_threejs
            if isinstance(style['color'], list) and len(style['color']) > 0:
                # For multiple colors, use the first one for this dataset
                # TODO: Implement per-point coloring for gradient effects
                style['color'] = style['color'][0] if isinstance(style['color'][0], str) else 'black'
            
            styles.append(style)
        
        return styles
    
    def _parse_format_string(self, fmt_str: str) -> Dict:
        """Parse matplotlib format string like 'ro-', 'b--', 'g:'"""
        style = {}
        
        # Color mapping
        color_map = {
            'r': 'red', 'g': 'green', 'b': 'blue', 'c': 'cyan',
            'm': 'magenta', 'y': 'yellow', 'k': 'black', 'w': 'white'
        }
        
        # Marker mapping
        marker_map = {
            'o': 'circle', '.': 'point', ',': 'pixel', 'v': 'triangle_down',
            '^': 'triangle_up', '<': 'triangle_left', '>': 'triangle_right',
            's': 'square', 'p': 'pentagon', '*': 'star', 'h': 'hexagon1',
            'H': 'hexagon2', '+': 'plus', 'x': 'x', 'D': 'diamond',
            'd': 'thin_diamond', '|': 'vline', '_': 'hline'
        }
        
        # Line style mapping
        linestyle_map = {
            '-': 'solid', '--': 'dashed', '-.': 'dashdot', ':': 'dotted'
        }
        
        # Extract color (single character)
        for char in fmt_str:
            if char in color_map:
                style['color'] = color_map[char]
                break
        
        # Extract marker (single character)
        for char in fmt_str:
            if char in marker_map:
                style['marker'] = marker_map[char]
                break
        
        # Extract line style (can be multi-character) - check longest patterns first
        linestyle_found = False
        linestyle_patterns = sorted(linestyle_map.items(), key=lambda x: len(x[0]), reverse=True)
        for ls_key, ls_value in linestyle_patterns:
            if ls_key in fmt_str:
                style['linestyle'] = ls_value
                linestyle_found = True
                break
        
        # If marker is specified but no line style, disable lines (marker-only plot)
        if 'marker' in style and not linestyle_found:
            style['linestyle'] = None
        
        return style
    
    def _detect_dimensionality(self) -> str:
        """Detect if data is 2D or 3D"""
        # Check all datasets for dimensionality
        for dataset in self.datasets:
            if 'z' in dataset.columns:
                return '3d'
        return '2d'
    
    def _interpolate_line_data(self, data: pd.DataFrame, n_samples: int) -> pd.DataFrame:
        """Interpolate line data for smooth curves"""
        if len(data) < 2:
            return data  # Can't interpolate single point
        
        # Create parameter for interpolation (cumulative distance along curve)
        if self.dimensionality == '2d':
            coords = data[['x', 'y']].values
        else:
            coords = data[['x', 'y', 'z']].values
        
        # Calculate cumulative distances
        distances = np.sqrt(np.sum(np.diff(coords, axis=0)**2, axis=1))
        cumulative_distances = np.concatenate(([0], np.cumsum(distances)))
        
        # Use more samples if original data has more points
        actual_samples = max(n_samples, len(data))
        
        # Create interpolation functions
        t_new = np.linspace(0, cumulative_distances[-1], actual_samples)
        
        interpolated_data = {}
        for col in data.columns:
            if col in ['x', 'y', 'z']:
                f = interp1d(cumulative_distances, data[col], kind='cubic', bounds_error=False, fill_value='extrapolate')
                interpolated_data[col] = f(t_new)
        
        return pd.DataFrame(interpolated_data)
    
    def _create_threejs_plot(self):
        """Create the Three.js scene, camera, and objects"""
        # Create scene
        self.scene = p3js.Scene()
        
        # Create camera based on dimensionality
        if self.dimensionality == '2d':
            self._setup_2d_camera()
        else:
            self._setup_3d_camera()
        
        # Add data to scene
        self._add_data_to_scene()
        
        # Set up lighting
        self._setup_lighting()
        
        # Create renderer
        self._create_renderer()
    
    def _setup_2d_camera(self):
        """Set up orthographic camera for 2D plots"""
        # Calculate data bounds across all datasets
        all_x = pd.concat([dataset['x'] for dataset in self.datasets])
        all_y = pd.concat([dataset['y'] for dataset in self.datasets])
        x_min, x_max = all_x.min(), all_x.max()
        y_min, y_max = all_y.min(), all_y.max()
        
        # Add padding
        x_range = x_max - x_min
        y_range = y_max - y_min
        padding = 0.1
        
        x_pad = x_range * padding
        y_pad = y_range * padding
        
        # Create orthographic camera
        self.camera = p3js.OrthographicCamera(
            left=x_min - x_pad,
            right=x_max + x_pad,
            top=y_max + y_pad,
            bottom=y_min - y_pad,
            near=0.1,
            far=1000
        )
        self.camera.position = [0, 0, 1]
        
        # 2D controls (pan and zoom only, no rotation)
        self.controls = [p3js.OrbitControls(
            controlling=self.camera,
            enableRotate=False,
            enableDamping=True
        )]
    
    def _setup_3d_camera(self):
        """Set up perspective camera for 3D plots"""
        # Calculate data center and bounds across all datasets
        all_x = pd.concat([dataset['x'] for dataset in self.datasets])
        all_y = pd.concat([dataset['y'] for dataset in self.datasets])
        all_z = pd.concat([dataset['z'] for dataset in self.datasets if 'z' in dataset.columns])
        
        center = [
            all_x.mean(),
            all_y.mean(),
            all_z.mean() if len(all_z) > 0 else 0
        ]
        
        # Position camera at reasonable distance
        distance = self._calculate_camera_distance()
        
        self.camera = p3js.PerspectiveCamera(
            fov=75,
            aspect=1.0,
            near=0.1,
            far=1000
        )
        self.camera.position = [
            center[0] + distance,
            center[1] + distance,
            center[2] + distance
        ]
        
        # 3D controls (full orbit)
        self.controls = [p3js.OrbitControls(
            controlling=self.camera,
            target=center,
            enableDamping=True
        )]
    
    def _calculate_camera_distance(self) -> float:
        """Calculate appropriate camera distance based on data bounds"""
        ranges = []
        
        # Calculate ranges across all datasets
        for col in ['x', 'y', 'z']:
            all_values = []
            for dataset in self.datasets:
                if col in dataset.columns:
                    all_values.extend(dataset[col].values)
            
            if all_values:
                ranges.append(max(all_values) - min(all_values))
        
        max_range = max(ranges) if ranges else 1.0
        return max_range * 2.0  # Position camera at 2x the data range
    
    def _add_data_to_scene(self):
        """Add data visualization objects to the scene"""
        # Plot each dataset with its own style
        for i, (dataset, style) in enumerate(zip(self.datasets, self.plot_styles)):
            self._create_dataset_plot(dataset, style, i)
    
    def _create_dataset_plot(self, dataset: pd.DataFrame, style: Dict, dataset_idx: int):
        """Create plot objects for a single dataset with given style"""
        
        # Handle single point special case
        if len(dataset) == 1:
            self._create_single_point(dataset, style, dataset_idx)
            return
        
        # Create line plot if linestyle is specified
        if style['linestyle'] and style['linestyle'] != 'None':
            # Interpolate for smooth lines
            if style['interpolation_samples'] > len(dataset):
                interpolated_data = self._interpolate_line_data(dataset, style['interpolation_samples'])
            else:
                interpolated_data = dataset
            
            self._create_line_object(interpolated_data, style, dataset_idx)
        
        # Create markers if marker style is specified
        if style['marker'] and style['marker'] != 'None':
            self._create_marker_object(dataset, style, dataset_idx)
    
    def _create_single_point(self, dataset: pd.DataFrame, style: Dict, dataset_idx: int):
        """Create a single large marker for single-point datasets"""
        positions = self._data_to_positions(dataset)
        
        geometry = p3js.BufferGeometry(
            attributes={
                'position': p3js.BufferAttribute(
                    array=positions.astype(np.float32),
                    itemSize=3
                )
            }
        )
        
        material = p3js.PointsMaterial(
            color=style['color'],
            size=style['markersize'] / 100.0,  # Scale for Three.js
            sizeAttenuation=False,
            transparent=True,
            opacity=style['alpha']
        )
        
        points = p3js.Points(geometry=geometry, material=material)
        self.scene.add(points)
    
    def _create_line_object(self, dataset: pd.DataFrame, style: Dict, dataset_idx: int):
        """Create line object with specified style"""
        positions = self._data_to_positions(dataset)
        
        geometry = p3js.BufferGeometry(
            attributes={
                'position': p3js.BufferAttribute(
                    array=positions.astype(np.float32),
                    itemSize=3
                )
            }
        )
        
        # Handle different line styles
        if style['linestyle'] == 'dashed':
            # Use LineDashedMaterial for dashed lines
            material = p3js.LineDashedMaterial(
                color=style['color'],
                linewidth=style['linewidth'],
                transparent=True,
                opacity=style['alpha'],
                dashSize=0.1,
                gapSize=0.05
            )
            line = p3js.Line(geometry=geometry, material=material)
            # Note: computeLineDistances() may not be available in all pythreejs versions
            # The dashed effect should still work without it in most cases
        else:
            material = p3js.LineBasicMaterial(
                color=style['color'],
                linewidth=style['linewidth'],
                transparent=True,
                opacity=style['alpha']
            )
            line = p3js.Line(geometry=geometry, material=material)
        
        self.scene.add(line)
    
    def _create_marker_object(self, dataset: pd.DataFrame, style: Dict, dataset_idx: int):
        """Create marker objects at data points"""
        positions = self._data_to_positions(dataset)
        
        geometry = p3js.BufferGeometry(
            attributes={
                'position': p3js.BufferAttribute(
                    array=positions.astype(np.float32),
                    itemSize=3
                )
            }
        )
        
        # For now, use points for all markers (can be extended for different shapes)
        material = p3js.PointsMaterial(
            color=style['color'],
            size=style['markersize'] / 100.0,  # Scale for Three.js
            sizeAttenuation=False,
            transparent=True,
            opacity=style['alpha']
        )
        
        points = p3js.Points(geometry=geometry, material=material)
        self.scene.add(points)
    
    def _data_to_positions(self, dataset: pd.DataFrame = None) -> np.ndarray:
        """Convert DataFrame to Three.js positions array"""
        if dataset is None:
            dataset = self.datasets[0]  # Fallback for backward compatibility
        
        if self.dimensionality == '2d':
            # 2D data - set z=0
            positions = np.column_stack([
                dataset['x'].values,
                dataset['y'].values,
                np.zeros(len(dataset))
            ])
        else:
            # 3D data
            positions = np.column_stack([
                dataset['x'].values,
                dataset['y'].values,
                dataset['z'].values
            ])
        
        return positions.flatten()
    
    def _setup_lighting(self):
        """Add appropriate lighting to the scene"""
        # Ambient light for overall illumination
        ambient = p3js.AmbientLight(color='#404040', intensity=0.6)
        self.scene.add(ambient)
        
        # Directional light for 3D depth
        if self.dimensionality == '3d':
            directional = p3js.DirectionalLight(color='#ffffff', intensity=0.8)
            directional.position = [1, 1, 1]
            self.scene.add(directional)
    
    def _create_renderer(self):
        """Create the Three.js renderer widget"""
        self.renderer = p3js.Renderer(
            camera=self.camera,
            scene=self.scene,
            controls=self.controls,
            width=self.kwargs.get('width', 800),
            height=self.kwargs.get('height', 600)
        )
    
    # Public API methods
    
    def show(self):
        """Display the interactive Three.js plot"""
        if self.renderer is None:
            raise RuntimeError("Plot not properly initialized")
        return self.renderer
    
    def to_matplotlib(self):
        """Convert to matplotlib figure for fine-tuning"""
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        
        # Create matplotlib figure
        fig = plt.figure(figsize=(8, 6))
        
        if self.dimensionality == '3d':
            ax = fig.add_subplot(111, projection='3d')
        else:
            ax = fig.add_subplot(111)
        
        # Plot each dataset
        for i, (dataset, style) in enumerate(zip(self.datasets, self.plot_styles)):
            self._add_dataset_to_matplotlib(ax, dataset, style, i)
        
        # Clean styling: remove labels and tick labels
        ax.set_xlabel('')
        ax.set_ylabel('')
        if self.dimensionality == '3d':
            ax.set_zlabel('')
            # Keep grid for 3D plots
            ax.grid(True, alpha=0.3)
        else:
            # Keep bounding box for 2D plots but remove tick labels
            ax.tick_params(labelbottom=False, labelleft=False)
        
        # Remove tick labels for all plots
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        if self.dimensionality == '3d':
            ax.set_zticklabels([])
        
        # Adjust layout
        plt.tight_layout()
        
        return fig
    
    def _add_dataset_to_matplotlib(self, ax, dataset, style, dataset_idx):
        """Add a single dataset to matplotlib axes"""
        
        # Apply interpolation for line plots if needed (same logic as Three.js rendering)
        plot_lines = style['linestyle'] is not None and style['linestyle'] != 'None'
        if plot_lines and style['interpolation_samples'] > len(dataset):
            dataset = self._interpolate_line_data(dataset, style['interpolation_samples'])
        
        # Extract coordinates
        x = dataset['x'].values
        y = dataset['y'].values
        z = dataset['z'].values if 'z' in dataset.columns else None
        
        # Convert Three.js color to matplotlib color
        color = style['color']
        alpha = style['alpha']
        
        # Convert line style
        linestyle_map = {
            'solid': '-',
            'dashed': '--',
            'dotted': ':',
            'dashdot': '-.'
        }
        linestyle = linestyle_map.get(style['linestyle'], '-')
        
        # Convert marker style
        marker_map = {
            'circle': 'o',
            'square': 's',
            'triangle_up': '^',
            'triangle_down': 'v',
            'triangle_left': '<',
            'triangle_right': '>',
            'star': '*',
            'plus': '+',
            'x': 'x',
            'diamond': 'D',
            'point': '.',
            'pixel': ','
        }
        marker = marker_map.get(style['marker'], 'o') if style['marker'] else None
        
        # Determine plot type
        plot_lines = style['linestyle'] is not None and style['linestyle'] != 'None'
        plot_markers = style['marker'] is not None and style['marker'] != 'None'
        
        # Plot based on dimensionality
        if self.dimensionality == '3d':
            if plot_lines and plot_markers:
                ax.plot(x, y, z, color=color, linestyle=linestyle, 
                       marker=marker, markersize=style['markersize']/2, 
                       linewidth=style['linewidth'], alpha=alpha)
            elif plot_lines:
                ax.plot(x, y, z, color=color, linestyle=linestyle,
                       linewidth=style['linewidth'], alpha=alpha)
            elif plot_markers:
                ax.scatter(x, y, z, color=color, s=style['markersize']**2,
                          marker=marker, alpha=alpha)
        else:
            if plot_lines and plot_markers:
                ax.plot(x, y, color=color, linestyle=linestyle,
                       marker=marker, markersize=style['markersize']/2,
                       linewidth=style['linewidth'], alpha=alpha)
            elif plot_lines:
                ax.plot(x, y, color=color, linestyle=linestyle,
                       linewidth=style['linewidth'], alpha=alpha)
            elif plot_markers:
                ax.scatter(x, y, color=color, s=style['markersize']**2,
                          marker=marker, alpha=alpha)
    
    def save(self, filename: str):
        """Save figure object for later reloading"""
        if not filename.endswith('.hyp'):
            filename += '.hyp'
        
        # Create serializable representation
        save_data = {
            'datasets': self.datasets,
            'plot_styles': self.plot_styles,
            'kwargs': self.kwargs,
            'dimensionality': self.dimensionality
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(save_data, f)
    
    def export(self, filename: str, **export_kwargs):
        """Export plot in various formats"""
        # This will be implemented in Week 5 (SVG export)
        raise NotImplementedError("Export functionality will be implemented in Week 5")
    
    @classmethod
    def load(cls, filename: str) -> 'HyperToolsFigure':
        """Load a saved figure object"""
        if not filename.endswith('.hyp'):
            filename += '.hyp'
        
        with open(filename, 'rb') as f:
            save_data = pickle.load(f)
        
        # Reconstruct figure from saved data
        fig = cls.__new__(cls)
        fig.datasets = save_data['datasets']
        fig.plot_styles = save_data['plot_styles']
        fig.kwargs = save_data['kwargs']
        fig.dimensionality = save_data['dimensionality']
        fig.n_datasets = len(fig.datasets)
        fig.is_animated = fig.kwargs.get('animate', False)
        
        # Recreate Three.js plot
        fig.scene = None
        fig.camera = None
        fig.renderer = None
        fig.controls = None
        fig._create_threejs_plot()
        
        return fig


class ThreeJSBackend:
    """
    Main backend class for HyperTools Three.js integration
    """
    
    @staticmethod
    def plot(data: Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]], 
             fmt: Union[str, List[str]] = None, **kwargs) -> HyperToolsFigure:
        """
        Create a plot using Three.js backend
        
        Parameters
        ----------
        data : DataFrame, ndarray, or list thereof
            Input data for plotting
        fmt : str or list of str, optional
            Matplotlib-style format strings (e.g., 'ro-', 'b--', 'g:')
        **kwargs : dict
            Additional plotting parameters (linewidth, markersize, color, etc.)
            
        Returns
        -------
        HyperToolsFigure
            Figure object with Three.js backend
        """
        return HyperToolsFigure(data, fmt=fmt, **kwargs)


# Global functions for HyperTools integration

def load(filename: str) -> HyperToolsFigure:
    """Load a saved HyperTools figure"""
    return HyperToolsFigure.load(filename)