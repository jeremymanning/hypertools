import numpy as np
import pandas as pd
import hypertools as hyp

print("=== DEBUGGING CURRENT INTERPOLATION LOGIC ===")

# Create simple trajectory data to understand what's happening
data_trajectory = []
for t in range(4):
    # Simple line that moves right with each timepoint
    x_values = np.array([t*2, t*2+1, t*2+2])  # t=0: [0,1,2], t=1: [2,3,4], etc.
    y_values = np.array([0, 1, 2])            # Consistent diagonal
    
    df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 3)
    data_trajectory.append(df)

trajectory = pd.concat(data_trajectory)
print(f"Original data:")
for t in trajectory.index.unique():
    subset = trajectory[trajectory.index == t]
    print(f"  Time {t}: x={list(subset.x)}, y={list(subset.y)}")

# Create animator and examine the interpolation logic
from hypertools.plot.animate import Animator

animator = Animator(trajectory, style='window', mode='lines')

print(f"\n=== CURRENT LOGIC ANALYSIS ===")
print(f"Discrete indices: {animator.discrete_indices}")
print(f"Interpolated indices: {len(animator.indices)} values from {animator.indices[0]:.3f} to {animator.indices[-1]:.3f}")
print(f"Total frames: {len(animator.angles)}")

# Debug window calculation for first few frames
print(f"\n=== WINDOW CALCULATION DEBUG ===")
for frame_i in [0, 50, 100, 150, 200, 250]:
    if frame_i < len(animator.window_starts):
        w_start = animator.window_starts[frame_i]
        w_end = animator.window_ends[frame_i]
        
        # See what get_window returns
        window_data = animator.get_window(trajectory, w_start, w_end)
        
        print(f"Frame {frame_i}:")
        print(f"  Window indices: {w_start} -> {w_end}")
        if not window_data.empty:
            print(f"  Discrete timepoints shown: {sorted(window_data.index.unique())}")
            print(f"  X data: {list(window_data.x)}")
        else:
            print(f"  ⚠ Empty window!")

print(f"\n=== PROBLEM DIAGNOSIS ===")
print("Current behavior:")
print("1. We create 301 interpolated time values [0.0, 0.01, 0.02, ..., 3.0]")
print("2. But get_window() still filters by discrete timepoints [0, 1, 2, 3]") 
print("3. So frames just show jumps between original timepoints")
print("")
print("What SHOULD happen for line plots:")
print("1. Create spline through original data points")
print("2. Resample spline to 301 interpolated points")
print("3. Each frame shows next interpolated point along the smooth trajectory")
print("4. Result: smooth motion instead of discrete jumps")

print(f"\n=== REQUIRED CHANGES ===")
print("For line plots, we need:")
print("1. Spline interpolation of the actual data coordinates")
print("2. Frame-by-frame advancement along interpolated trajectory")
print("3. Sliding window that shows smooth progression, not discrete jumps")
print("")
print("For scatter plots:")
print("1. No interpolation - just show original timepoints")
print("2. Adjust frame rate to match number of actual timepoints")
print("")
print("For lines+markers:")
print("1. Interpolated lines for smooth motion")
print("2. Markers only at original data locations")