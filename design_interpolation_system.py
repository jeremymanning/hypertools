import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

print("=== DESIGNING PROPER INTERPOLATION SYSTEM ===")

# Test data: 4 timepoints with 3 points each
data_trajectory = []
for t in range(4):
    x_values = np.array([t*2, t*2+1, t*2+2])  # [0,1,2], [2,3,4], [4,5,6], [6,7,8]
    y_values = np.array([0, 1, 2])            # Consistent
    
    df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 3)
    data_trajectory.append(df)

trajectory = pd.concat(data_trajectory)
print(f"Original data shape: {trajectory.shape}")
print(f"Timepoints: {trajectory.index.unique()}")

# Group by coordinate (each point's trajectory through time)
print(f"\n=== COORDINATE TRAJECTORIES ===")
# Each coordinate has a trajectory through time
unique_coords = trajectory.groupby(trajectory.index).apply(lambda x: x.reset_index(drop=True))
n_points_per_time = len(trajectory) // len(trajectory.index.unique())

coordinate_trajectories = []
for coord_idx in range(n_points_per_time):
    coord_path = []
    for t in trajectory.index.unique():
        subset = trajectory[trajectory.index == t]
        coord_path.append(subset.iloc[coord_idx])
    
    coord_df = pd.DataFrame(coord_path)
    coord_df['time'] = trajectory.index.unique()
    coordinate_trajectories.append(coord_df)
    
    print(f"Coordinate {coord_idx}: x={list(coord_df.x)}, y={list(coord_df.y)}")

print(f"\n=== INTERPOLATION DESIGN ===")

# Design 1: Spline interpolation for line plots
def create_interpolated_trajectory(coord_trajectories, n_frames=301):
    """Create smoothly interpolated trajectory for line plots"""
    
    # Original time points
    original_times = coord_trajectories[0]['time'].values
    print(f"Original times: {original_times}")
    
    # New interpolated time points
    interp_times = np.linspace(original_times[0], original_times[-1], n_frames)
    print(f"Interpolated to {n_frames} times: {interp_times[:5]}...{interp_times[-5:]}")
    
    interpolated_data = []
    
    for coord_idx, coord_traj in enumerate(coord_trajectories):
        # Interpolate x and y coordinates separately
        x_interp = interp1d(original_times, coord_traj['x'], kind='linear', 
                           bounds_error=False, fill_value='extrapolate')
        y_interp = interp1d(original_times, coord_traj['y'], kind='linear',
                           bounds_error=False, fill_value='extrapolate')
        
        # Generate interpolated coordinates
        x_smooth = x_interp(interp_times)
        y_smooth = y_interp(interp_times)
        
        # Create DataFrame for this coordinate's interpolated path
        for i, t in enumerate(interp_times):
            interpolated_data.append({
                'x': x_smooth[i],
                'y': y_smooth[i], 
                'time': t,
                'coord_id': coord_idx
            })
    
    return pd.DataFrame(interpolated_data), interp_times

# Test the interpolation
interp_data, interp_times = create_interpolated_trajectory(coordinate_trajectories, 10)  # Small test

print(f"\nInterpolated trajectory sample:")
print(f"  Original coord 0 at time 0: x={coordinate_trajectories[0].iloc[0]['x']}")
print(f"  Original coord 0 at time 1: x={coordinate_trajectories[0].iloc[1]['x']}")
print()

# Show interpolated values
for i in [0, 2, 4, 6, 8]:
    coord_0_data = interp_data[(interp_data.coord_id == 0) & (abs(interp_data.time - interp_times[i]) < 0.001)]
    if not coord_0_data.empty:
        x_val = coord_0_data.iloc[0]['x']
        time_val = coord_0_data.iloc[0]['time']
        print(f"  Interpolated coord 0 at time {time_val:.2f}: x={x_val:.2f}")

print(f"\n=== ANIMATION FRAME DESIGN ===")
print("For line plots:")
print("1. Each frame shows a sliding window of interpolated points")
print("2. Window size determines how much trajectory is visible")
print("3. Each frame advances by 1 interpolated timestep")
print("4. Result: smooth growth/sliding of the line")
print()
print("For scatter plots:")
print("1. No interpolation - use original discrete timepoints")
print("2. Frame rate matches number of actual timepoints")
print("3. Result: discrete jumps (appropriate for scatter)")
print()
print("For lines+markers:")
print("1. Lines use interpolated trajectory")
print("2. Markers only appear at original timepoint locations")
print("3. Result: smooth lines with discrete markers")