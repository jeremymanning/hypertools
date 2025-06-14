import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import plotly.graph_objects as go

print("=== IMPLEMENTING LINEPLOT INTERPOLATION ===")

# Create simple test trajectory
def create_test_trajectory():
    data_trajectory = []
    for t in range(4):
        # Simple moving line: each timepoint shifts right
        x_values = np.array([t*2, t*2+1, t*2+2])  # [0,1,2], [2,3,4], [4,5,6], [6,7,8] 
        y_values = np.array([0, 1, 2])            # Consistent diagonal
        
        df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 3)
        data_trajectory.append(df)
    
    return pd.concat(data_trajectory)

def interpolate_trajectory_for_lines(trajectory, n_frames=20):
    """Create interpolated trajectory for smooth line animation"""
    
    # Get original timepoints
    timepoints = sorted(trajectory.index.unique())
    print(f"Original timepoints: {timepoints}")
    
    # Group data by timepoint to get coordinate sets
    timepoint_data = {}
    for t in timepoints:
        subset = trajectory[trajectory.index == t]
        timepoint_data[t] = subset[['x', 'y']].values
    
    # Number of coordinates per timepoint
    n_coords = len(timepoint_data[timepoints[0]])
    print(f"Coordinates per timepoint: {n_coords}")
    
    # Create interpolated timeline
    interp_times = np.linspace(timepoints[0], timepoints[-1], n_frames)
    print(f"Interpolated to {n_frames} frames: {interp_times[0]:.2f} to {interp_times[-1]:.2f}")
    
    # Interpolate each coordinate's trajectory through time
    interpolated_data = []
    
    for coord_idx in range(n_coords):
        # Extract this coordinate's path through time
        coord_x_path = [timepoint_data[t][coord_idx, 0] for t in timepoints]
        coord_y_path = [timepoint_data[t][coord_idx, 1] for t in timepoints]
        
        print(f"Coordinate {coord_idx}: x_path={coord_x_path}, y_path={coord_y_path}")
        
        # Create interpolation functions
        x_interp = interp1d(timepoints, coord_x_path, kind='linear', 
                           bounds_error=False, fill_value='extrapolate')
        y_interp = interp1d(timepoints, coord_y_path, kind='linear',
                           bounds_error=False, fill_value='extrapolate')
        
        # Generate smooth interpolated values
        x_smooth = x_interp(interp_times)
        y_smooth = y_interp(interp_times)
        
        # Store interpolated trajectory for this coordinate
        for i, t in enumerate(interp_times):
            interpolated_data.append({
                'x': x_smooth[i],
                'y': y_smooth[i],
                'time': t,
                'frame': i,
                'coord_id': coord_idx
            })
    
    return pd.DataFrame(interpolated_data), interp_times

def create_sliding_window_frames(interp_data, interp_times, window_size=5):
    """Create frames for sliding window animation"""
    
    frames = []
    n_frames = len(interp_times)
    
    for frame_i in range(n_frames):
        # Determine window range
        window_start = max(0, frame_i - window_size + 1)
        window_end = frame_i + 1
        
        # Get data for this window
        window_data = interp_data[
            (interp_data.frame >= window_start) & 
            (interp_data.frame < window_end)
        ]
        
        if not window_data.empty:
            # Create line trace for this frame
            trace = go.Scatter(
                x=window_data['x'],
                y=window_data['y'],
                mode='lines',
                name=f'Frame {frame_i}',
                line=dict(color='blue')
            )
            
            frame = go.Frame(
                data=[trace],
                name=str(frame_i)
            )
            frames.append(frame)
            
            print(f"Frame {frame_i}: window {window_start}->{window_end}, {len(window_data)} points, x range: {window_data.x.min():.1f}-{window_data.x.max():.1f}")
    
    return frames

# Test the implementation
print("\n=== TESTING IMPLEMENTATION ===")

trajectory = create_test_trajectory()
print(f"Original trajectory:")
for t in trajectory.index.unique():
    subset = trajectory[trajectory.index == t]
    print(f"  Time {t}: x={list(subset.x)}, y={list(subset.y)}")

# Create interpolated data
interp_data, interp_times = interpolate_trajectory_for_lines(trajectory, n_frames=20)

print(f"\n=== INTERPOLATION RESULTS ===")
# Show interpolated samples
for frame in [0, 5, 10, 15, 19]:
    frame_data = interp_data[interp_data.frame == frame]
    if not frame_data.empty:
        x_vals = list(frame_data.x)
        print(f"Frame {frame} (t={interp_times[frame]:.2f}): x={[f'{x:.1f}' for x in x_vals]}")

# Create sliding window frames
print(f"\n=== SLIDING WINDOW FRAMES ===")
frames = create_sliding_window_frames(interp_data, interp_times, window_size=8)

print(f"\n=== SUCCESS CRITERIA ===")
print("✅ Each frame should show different x values (smooth progression)")
print("✅ Window should grow initially, then slide")
print("✅ Should be much smoother than discrete jumps")