import numpy as np
import pandas as pd
import hypertools as hyp

# Create the same simple test data
data_simple = []
for t in range(4):
    x = np.array([0, 1, 2, 3, 4]) + t*5
    y = np.array([t, t, t, t, t])
    z = np.array([0, 0, 0, 0, 0])
    
    df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=[t] * 5)
    data_simple.append(df)

simple_trajectory = pd.concat(data_simple)

print("=== DEBUGGING WINDOW CALCULATIONS ===")

# Manually examine what the Animator is calculating
from hypertools.plot.animate import Animator

# Create animator and examine its window calculations
animator = Animator(simple_trajectory, style='window', mode='lines')

print(f"Data indices: {simple_trajectory.index.unique()}")
print(f"Animator indices: {animator.indices}")
print(f"Window starts: {animator.window_starts}")
print(f"Window ends: {animator.window_ends}")

# Check what get_window returns for first few frames
for i in range(min(4, len(animator.window_starts))):
    w_start = animator.window_starts[i]
    w_end = animator.window_ends[i]
    
    print(f"\nFrame {i}:")
    print(f"  Window start/end indices: {w_start} -> {w_end}")
    print(f"  Time range: {animator.indices[int(w_start)]} -> {animator.indices[int(w_end)]}")
    
    # Get window data
    window_data = animator.get_window(simple_trajectory, w_start, w_end)
    print(f"  Window data shape: {window_data.shape}")
    if not window_data.empty:
        print(f"  Time indices in window: {window_data.index.unique()}")
        print(f"  X range: {window_data['x'].min()} -> {window_data['x'].max()}")
        print(f"  Y range: {window_data['y'].min()} -> {window_data['y'].max()}")
    else:
        print(f"  ⚠ Empty window!")

print("\n=== EXPECTED BEHAVIOR ===")
print("For a sliding window animation, we should see:")
print("- Frame 0: Only timepoint 0")
print("- Frame N: Window slides to show different timepoints")
print("- Each frame should show a subset of consecutive timepoints")

print("\n=== DIAGNOSIS ===")
print("If all frames show the same data, the issue is likely:")
print("1. Window start/end calculations are wrong")
print("2. Time filtering in get_window is incorrect") 
print("3. Animation parameters (focused, duration) are causing problems")