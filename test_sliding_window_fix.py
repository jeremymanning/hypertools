import numpy as np
import pandas as pd
import hypertools as hyp

# Create simple test data with 4 timepoints
data_simple = []
for t in range(4):
    x = np.array([0, 1, 2, 3, 4]) + t*5
    y = np.array([t, t, t, t, t])
    z = np.array([0, 0, 0, 0, 0])
    
    df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=[t] * 5)
    data_simple.append(df)

simple_trajectory = pd.concat(data_simple)

print("=== TESTING SLIDING WINDOW FIX ===")
print(f"Data timepoints: {simple_trajectory.index.unique()}")

# Create animator with new logic
from hypertools.plot.animate import Animator
animator = Animator(simple_trajectory, style='window', mode='lines')

print(f"Interpolated indices length: {len(animator.indices)}")
print(f"Discrete indices: {getattr(animator, 'discrete_indices', 'Not set')}")

# Test first few frames to see if window content changes
print("\n=== WINDOW CONTENT TEST ===")
for i in [0, 50, 100, 150, 200, 250]:
    if i < len(animator.window_starts):
        w_start = animator.window_starts[i]
        w_end = animator.window_ends[i]
        
        # Get window data using new logic
        window_data = animator.get_window(simple_trajectory, w_start, w_end)
        
        print(f"Frame {i}:")
        print(f"  Window indices: {w_start} -> {w_end}")
        if not window_data.empty:
            print(f"  Time indices: {sorted(window_data.index.unique())}")
            print(f"  Y values (timepoint indicator): {sorted(window_data['y'].unique())}")
        else:
            print(f"  ⚠ Empty window!")

print("\n=== SUCCESS CRITERIA ===")
print("✅ SUCCESS: Different frames show different timepoints")
print("❌ FAILED: All frames show same timepoint (0)")