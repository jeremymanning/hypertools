# noinspection PyPackageRequirements
import datawrangler as dw
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from scipy.spatial.distance import cdist

from ..manip import manip
from ..core import get, get_default_options, eval_dict

from .static import static_plot, get_bounds, flatten, plot_bounding_box, get_empty_canvas, expand_range

defaults = eval_dict(get_default_options()['animate'])


def template_wrangler(a, b):
    if type(a) is list:
        if type(b) is list:
            return [template_wrangler(i, j) for i, j in zip(a, b)]
        else:
            return [template_wrangler(i, b) for i in a]

    a = dw.wrangle(a)
    b = dw.wrangle(b)

    return pd.DataFrame(data=a.values, index=b.index, columns=a.columns)


class Animator:
    def __init__(self, data, **kwargs):
        self.data = data

        self.fig = kwargs.pop('fig', get_empty_canvas())
        self.style = kwargs.pop('style', defaults['style'])
        self.focused = kwargs.pop('focused', defaults['focused'])
        self.focused_alpha = kwargs.pop('focused_alpha', defaults['focused_alpha'])
        self.unfocused = kwargs.pop('unfocused', defaults['unfocused'])
        self.unfocused_alpha = kwargs.pop('unfocused_alpha', defaults['unfocused_alpha'])
        self.rotations = kwargs.pop('rotations', defaults['rotations'])
        self.framerate = kwargs.pop('framerate', defaults['framerate'])
        self.duration = kwargs.pop('duration', defaults['duration'])
        self.elevation = kwargs.pop('elevation', defaults['elevation'])
        self.zooms = kwargs.pop('zoom', defaults['zoom'])
        self.bounding_box = kwargs.pop('bounding_box', False)
        self.opts = kwargs.copy()

        assert data is not None, ValueError('No dataset provided.')

        stacked_data = dw.stack(data)
        self.center = np.atleast_2d(stacked_data.mean(axis=0).values)
        self.proj = f'{stacked_data.shape[1]}d'

        # self.zooms = np.multiply(self.zooms, np.max(cdist(self.center, stacked_data.values)))
        self.indices = None

        if dw.zoo.is_dataframe(data):
            index_vals = set(data.index.values)
        else:  # data is a list
            index_vals = set()
            for d in data:
                index_vals = index_vals.union(set(d.index.values))

        if 'color' in self.opts.keys():
            self.opts['color'] = template_wrangler(self.opts['color'], self.data)

        # union of unique indices
        indices = list(index_vals)
        unique_indices = sorted(list(set(indices)))

        # NEW: For line plots with sliding window, create interpolated data
        if self.opts.get('mode', 'markers') == 'lines' and self.style == 'window':
            print("Creating interpolated trajectory for smooth line animation...")
            self.interpolated_data, self.interp_times = self._create_interpolated_trajectory(
                self.data, unique_indices, self.duration * self.framerate + 1
            )
            self.indices = self.interp_times
            self.discrete_indices = np.array(unique_indices)
            self.use_interpolation = True
        else:
            # For other animations, use discrete timepoints
            self.indices = np.array(unique_indices)
            self.discrete_indices = self.indices
            self.use_interpolation = False
        
        n_frames = len(self.indices)
        print(f"Animation: {self.opts.get('mode', 'markers')} mode -> {n_frames} frames")

        window_length = int(np.floor(n_frames * self.focused / self.duration))
        self.window_starts = np.concatenate([np.zeros([window_length]),
                                             np.arange(1, len(self.indices) - window_length)])
        self.window_ends = np.arange(1, self.window_starts[-1] + window_length + 1)

        tail_window_length = int(np.round(n_frames * self.unfocused / self.duration))
        self.tail_window_starts = np.concatenate([np.zeros([tail_window_length]),
                                                  np.arange(1, len(self.indices) - tail_window_length)])
        self.tail_window_ends = self.window_ends
        self.tail_window_precogs = np.concatenate([tail_window_length +
                                                   np.arange(1, len(self.indices) - tail_window_length),
                                                   self.indices[-1] * np.ones([tail_window_length])])

        self.angles = np.linspace(0, self.rotations * 360, len(self.window_starts) + 1)[:-1]

    def generate_frames_optimized(self):
        """Optimized frame generation - pre-compute all frame data in batch"""
        frames = []
        mode = self.opts.get('mode', 'markers')
        
        # Pre-extract data once
        if type(self.data) is list:
            data_values = [d.values for d in self.data]
            data_indices = [d.index.values for d in self.data]
        else:
            data_values = [self.data.values]
            data_indices = [self.data.index.values]
        
        # Generate frames in batch
        for i in range(len(self.angles)):
            frame_data = []
            
            if self.style == 'window':
                # Get window data efficiently
                window_start = self.window_starts[i] 
                window_end = self.window_ends[i]
                
                for dv, di in zip(data_values, data_indices):
                    # Find indices in window
                    start_idx = self.indices[int(window_start)]
                    end_idx = self.indices[int(window_end)]
                    
                    mask = (di >= start_idx) & (di <= end_idx)
                    if np.any(mask):
                        windowed_data = dv[mask]
                        
                        if windowed_data.shape[1] == 2:
                            trace = go.Scatter(
                                x=windowed_data[:, 0],
                                y=windowed_data[:, 1],
                                mode=mode,
                                opacity=self.focused_alpha
                            )
                        else:  # 3D
                            trace = go.Scatter3d(
                                x=windowed_data[:, 0],
                                y=windowed_data[:, 1], 
                                z=windowed_data[:, 2],
                                mode=mode,
                                opacity=self.focused_alpha
                            )
                        frame_data.append(trace)
            
            frames.append(go.Frame(data=frame_data, name=str(i)))
        
        return frames

    def build_animation(self):
        frame_duration = 1000 * self.duration / len(self.angles)

        # set up base figure
        fig = self.fig.to_dict().copy()

        # add buttons and slider and define transitions
        # Use smoother transition settings
        transition_duration = min(frame_duration * 0.3, 100)  # Smooth but not too slow
        
        fig['layout']['updatemenus'] = [{'buttons': [{
            'label': ' ▶',  # play button
            'args': [None, {'frame': {'duration': frame_duration, 'redraw': False},  # Disable redraw
                            'fromcurrent': True,
                            'transition': {'duration': transition_duration}}],  # Add smooth transition
            'method': 'animate'}, {
            'label': ' ||',  # stop/pause button
            'args': [[None], {'frame': {'duration': 0, 'redraw': False},  # Disable redraw
                              'mode': 'immediate',
                              'transition': {'duration': 0}}],
            'method': 'animate'}],
            # slider
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'}]

        bounds = get_bounds(self.data)
        scene = {'xaxis': {'range': expand_range([bounds[0, 0], bounds[1, 0]]), 'autorange': False},
                 'yaxis': {'range': expand_range([bounds[0, 1], bounds[1, 1]]), 'autorange': False}}
        if bounds.shape[1] == 3:
            scene['zaxis'] = {'range': expand_range([bounds[0, 2], bounds[1, 2]]), 'autorange': False}

        # fig['layout']['xaxis'] = {'range': [bounds[0, 0], bounds[1, 0]], 'autorange': False}
        # fig['layout']['yaxis'] = {'range': [bounds[0, 1], bounds[1, 1]], 'autorange': False}
        # if bounds.shape[1] == 3:
        #    fig['layout']['zaxis'] = {'range': [bounds[0, 2], bounds[1, 2]], 'autorange': False}

        # define slider behavior
        slider = {
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 12},
                'prefix': 'Frame ',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 0},
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': []
        }
        for i in range(len(self.angles)):
            slider_step = {'args': [[i],
                                    {'frame': {'duration': frame_duration, 'redraw': False},  # Disable redraw
                                     'mode': 'immediate',
                                     'transition': {'duration': transition_duration}}],  # Add smooth transition
                           'label': str(i),
                           'method': 'animate'}
            slider['steps'].append(slider_step)

        # connect slider to frames
        fig['layout']['sliders'] = [slider]

        # add frames - use optimized batch generation
        init = self.get_frame(0)
        fig['data'] = init.data
        fig['frames'] = self.generate_frames_optimized()

        # convert to figure object and make bounds consistent across frames
        fig = go.Figure(fig)
        fig.update_layout(scene=scene)

        if self.proj == '3d':
            lengths = np.abs(np.diff(get_bounds(self.data), axis=0)).ravel()
            fig.update_layout(scene_aspectmode='manual',
                              scene_aspectratio={'x': 1, 'y': lengths[1] / lengths[0], 'z': lengths[2] / lengths[0]},
                              scene={'camera': init.layout.scene.camera})
        elif self.proj == '2d':
            fig.update_xaxes(range=scene['xaxis']['range'])
            fig.update_yaxes(range=scene['yaxis']['range'])

        return fig

    def get_frame(self, i, simplify=False):
        kwargs = {}
        if self.proj == '3d':
            bounds = get_bounds(self.data)

            scale = 1 # np.max(cdist(self.center, bounds))

            center = np.zeros_like(dw.stack(self.data).mean(axis=0).values)
            angle = np.deg2rad(get(self.angles, i))
            zoom = get(self.zooms, i)
            elevation = zoom * scale * np.sin(np.deg2rad(self.elevation)) + self.center[0, 2]

            camera = dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=center[0], y=center[1], z=center[2]),
                eye=dict(x=center[0] + zoom * scale * np.cos(angle), y=center[1] + zoom * scale * np.sin(angle),
                         z=elevation)
            )

            if not simplify:
                self.fig.update_layout(scene_camera=camera)
            else:
                kwargs = {'layout': {'scene': {'camera': camera}}}

        if self.style == 'window':
            return self.animate_window(i, simplify=simplify, **kwargs)
        elif self.style == 'chemtrails':
            return self.animate_chemtrails(i, simplify=simplify, **kwargs)
        elif self.style == 'precog':
            return self.animate_precog(i, simplify=simplify, **kwargs)
        elif self.style == 'bullettime':
            return self.animate_bullettime(i, simplify=simplify, **kwargs)
        elif self.style == 'grow':
            return self.animate_grow(i, simplify=simplify, **kwargs)
        elif self.style == 'shrink':
            return self.animate_shrink(i, simplify=simplify, **kwargs)
        elif self.style == 'spin':
            return self.animate_spin(i, simplify=simplify, **kwargs)
        else:
            raise ValueError(f'unknown animation mode: {self.mode}')

    def get_window(self, x, w_start, w_end):
        if type(x) is list:
            return [self.get_window(i, w_start, w_end) for i in x]

        # NEW: For interpolated line animations, use interpolated data
        # BUT only for the main data, not for color arrays or other metadata
        if (hasattr(self, 'use_interpolation') and self.use_interpolation and 
            hasattr(x, 'equals') and x.equals(self.data)):
            return self._get_interpolated_window(w_start, w_end)
        
        # For sliding window animations with interpolated indices, map to actual data timepoints
        elif hasattr(self, 'discrete_indices') and len(self.discrete_indices) != len(self.indices):
            # Calculate which discrete timepoints should be included in this window
            frame_progress = int(w_end) / len(self.indices)  # 0.0 to 1.0
            
            # Determine sliding window size (e.g., show 2 consecutive timepoints)
            window_size = max(1, int(len(self.discrete_indices) * self.focused / self.duration))
            
            # Calculate starting position in discrete timepoints
            max_start = len(self.discrete_indices) - window_size
            start_idx = int(frame_progress * max_start)
            end_idx = start_idx + window_size
            
            # Get the actual timepoint range
            start_time = self.discrete_indices[start_idx]
            end_time = self.discrete_indices[min(end_idx - 1, len(self.discrete_indices) - 1)]
        else:
            # Use original logic for non-interpolated animations
            start_time = self.indices[int(w_start)]
            end_time = self.indices[int(w_end)]
        
        # Filter data by time index
        mask = (x.index >= start_time) & (x.index <= end_time)
        return x[mask]

    def _get_interpolated_window(self, w_start, w_end):
        """Get sliding window from interpolated trajectory data"""
        
        # Determine current frame and window size
        current_frame = int(w_end)
        window_size = max(1, int(len(self.indices) * self.focused / self.duration))
        
        # Calculate window range in interpolated frames
        window_start_frame = max(0, current_frame - window_size + 1)
        window_end_frame = current_frame + 1
        
        # Get interpolated data for this window
        window_data = self.interpolated_data[
            (self.interpolated_data.frame >= window_start_frame) & 
            (self.interpolated_data.frame < window_end_frame)
        ]
        
        if window_data.empty:
            # Return empty dataframe with correct columns
            return pd.DataFrame(columns=['x', 'y'] if 'z' not in self.interpolated_data.columns else ['x', 'y', 'z'])
        
        # CRITICAL FIX: For line plots, we need to create a single continuous trajectory
        # Group by frame and coordinate, then order properly for continuous lines
        
        # Get the coordinate columns
        coord_cols = ['x', 'y'] if 'z' not in window_data.columns else ['x', 'y', 'z']
        
        # Create continuous trajectory by ordering points by time for each coordinate
        trajectory_points = []
        
        # Sort by time and coord_id to ensure proper ordering
        sorted_data = window_data.sort_values(['time', 'coord_id'])
        
        # For a line plot, we want to connect all points of the same coordinate through time
        for coord_id in sorted_data['coord_id'].unique():
            coord_data = sorted_data[sorted_data['coord_id'] == coord_id]
            
            for _, row in coord_data.iterrows():
                trajectory_points.append({
                    col: row[col] for col in coord_cols
                })
        
        # Convert to DataFrame with sequential index (no grouping by coordinates)
        result_df = pd.DataFrame(trajectory_points)
        
        # Use sequential numeric index for line connectivity
        result_df.index = range(len(result_df))
        
        return result_df

    def _create_interpolated_trajectory(self, data, timepoints, n_frames):
        """Create interpolated trajectory for smooth line animations"""
        from scipy.interpolate import interp1d
        
        # Handle list of dataframes or single dataframe
        if type(data) is list:
            # For now, focus on single trajectory case
            data = data[0] if len(data) == 1 else pd.concat(data)
        
        print(f"Interpolating trajectory: {len(timepoints)} timepoints -> {n_frames} frames")
        
        # Group data by timepoint to get coordinate sets
        timepoint_data = {}
        for t in timepoints:
            subset = data[data.index == t]
            if not subset.empty:
                timepoint_data[t] = subset[['x', 'y', 'z'] if 'z' in subset.columns else ['x', 'y']].values
        
        # Number of coordinates per timepoint
        n_coords = len(timepoint_data[timepoints[0]])
        n_dims = timepoint_data[timepoints[0]].shape[1]
        
        # Create interpolated timeline
        interp_times = np.linspace(timepoints[0], timepoints[-1], n_frames)
        
        # Interpolate each coordinate's trajectory through time
        interpolated_data = []
        
        for coord_idx in range(n_coords):
            # Extract this coordinate's path through time
            coord_paths = []
            for dim in range(n_dims):
                path = [timepoint_data[t][coord_idx, dim] for t in timepoints]
                coord_paths.append(path)
            
            # Create interpolation functions for each dimension
            interp_functions = []
            for dim in range(n_dims):
                interp_func = interp1d(timepoints, coord_paths[dim], kind='linear', 
                                     bounds_error=False, fill_value='extrapolate')
                interp_functions.append(interp_func)
            
            # Generate smooth interpolated values
            for i, t in enumerate(interp_times):
                coord_data = {
                    'time': t,
                    'frame': i,
                    'coord_id': coord_idx
                }
                
                # Add interpolated coordinates
                dim_names = ['x', 'y', 'z'][:n_dims]
                for dim, name in enumerate(dim_names):
                    coord_data[name] = interp_functions[dim](t)
                
                interpolated_data.append(coord_data)
        
        interpolated_df = pd.DataFrame(interpolated_data)
        print(f"Created interpolated trajectory: {len(interpolated_df)} total points")
        
        return interpolated_df, interp_times

    @classmethod
    def get_datadict(cls, data, mode='markers', **kwargs):
        if type(data) is list:
            return [cls.get_datadict(d, mode=mode, **kwargs)[0] for d in data]
        elif data.shape[1] == 2:
            return [go.Scatter(x=flatten(data.values[:, 0]), y=flatten(data.values[:, 1]), 
                              mode=mode, **kwargs)]
        elif data.shape[1] == 3:
            return [go.Scatter3d(x=flatten(data.values[:, 0]), y=flatten(data.values[:, 1]),
                                 z=flatten(data.values[:, 2]), mode=mode, **kwargs)]
        else:
            raise ValueError(f'data must be either 2D or 3D; given: {data.shape[1]}D')

    def get_opts(self, starts=None, ends=None):
        opts = self.opts.copy()
        opts = dw.core.update_dict(opts, {'opacity': self.focused_alpha})

        color = opts.pop('color', None)
        if all([x is not None for x in [color, starts, ends]]):
            color = self.get_window(color, starts, ends)
        opts['color'] = color
        return opts

    def tail_opts(self, starts=None, ends=None):
        return dw.core.update_dict(self.get_opts(starts=starts, ends=ends), {'opacity': self.unfocused_alpha})

    def animate_helper(self, i, starts=None, ends=None, extra_starts=None, extra_ends=None, simplify=False, **kwargs):
        if starts is None:
            starts = self.window_starts
        if ends is None:
            ends = self.window_ends

        window = self.get_window(self.data, starts[i], ends[i])
        if extra_starts is not None:
            extra = self.get_window(self.data, extra_starts[i], extra_ends[i])
        else:
            extra = None

        if simplify:
            if self.bounding_box:
                bb = plot_bounding_box(get_bounds(self.data), simplify=True)
            else:
                bb = []

            # Extract mode from opts for frame generation
            mode = self.opts.get('mode', 'markers')
            
            if extra is not None:
                # noinspection PyTypeChecker
                return go.Frame(data=[*bb, *Animator.get_datadict(window, mode=mode), 
                                     *Animator.get_datadict(extra, mode=mode, opacity=self.unfocused_alpha)], 
                               name=str(i), **kwargs)
            else:
                return go.Frame(data=[*bb, *Animator.get_datadict(window, mode=mode)], name=str(i), **kwargs)
        else:
            if self.bounding_box:
                self.fig = plot_bounding_box(get_bounds(self.data), fig=self.fig)

            static_plot(window, **self.get_opts(starts=starts[i], ends=ends[i]), fig=self.fig)
            if extra is not None:
                static_plot(extra, **self.tail_opts(starts=extra_starts[i], ends=extra_ends[i]), fig=self.fig,
                            showlegend=False)
            return self.fig

    def animate_window(self, i, simplify=False, **kwargs):
        return self.animate_helper(i, self.window_starts, self.window_ends, simplify=simplify, **kwargs)

    def animate_chemtrails(self, i, simplify=False, **kwargs):
        return self.animate_helper(i, extra_starts=self.tail_window_starts,
                                   extra_ends=self.tail_window_ends,
                                   simplify=simplify, **kwargs)

    def animate_precog(self, i, simplify=False, **kwargs):
        return self.animate_helper(i, extra_starts=self.window_starts, extra_ends=self.tail_window_precogs,
                                   simplify=simplify, **kwargs)

    def animate_bullettime(self, i, simplify=False, **kwargs):
        return self.animate_helper(i, extra_starts=np.zeros_like(self.window_starts),
                                   extra_ends=-1 * np.ones_like(self.window_ends),
                                   simplify=simplify, **kwargs)

    def animate_grow(self, i, simplify=False, **kwargs):
        return self.animate_helper(i, starts=np.zeros_like(self.window_starts), simplify=simplify, **kwargs)

    def animate_shrink(self, i, simplify=False, **kwargs):
        return self.animate_helper(i, starts=self.window_ends, ends=-1 * np.ones_like(self.window_ends),
                                   simplify=simplify, **kwargs)

    def animate_spin(self, i, simplify=False, **kwargs):
        return self.animate_helper(i, starts=np.zeros_like(self.window_starts),
                                   ends=-1 * np.ones_like(self.window_ends),
                                   simplify=simplify, **kwargs)
