import numpy as np
import pandas as pd

print("=== DEBUGGING INTERPOLATED DATA FORMAT ===")

# Create simple test trajectory
data_trajectory = []
for t in range(4):
    x_values = np.array([t*2, t*2+1, t*2+2])
    y_values = np.array([0, 1, 2])
    
    df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 3)
    data_trajectory.append(df)

trajectory = pd.concat(data_trajectory)

print(f"Original data format:")
print(f"  Columns: {trajectory.columns}")
print(f"  Index: {trajectory.index}")
print(f"  Shape: {trajectory.shape}")
print(f"  Sample:\n{trajectory.head()}")

# Test the interpolation
from hypertools.plot.animate import Animator

animator = Animator(trajectory, style='window', mode='lines', duration=2, framerate=5)

print(f"\n=== INTERPOLATED DATA FORMAT ===")
print(f"Interpolated data columns: {animator.interpolated_data.columns}")
print(f"Interpolated data shape: {animator.interpolated_data.shape}")
print(f"Sample interpolated data:")
print(animator.interpolated_data.head(10))

# Test window extraction
print(f"\n=== TESTING WINDOW EXTRACTION ===")
try:
    window = animator._get_interpolated_window(0, 1)
    print(f"Window shape: {window.shape}")
    print(f"Window columns: {window.columns}")
    print(f"Window index: {window.index}")
    print(f"Window data:")
    print(window)
except Exception as e:
    print(f"Window extraction error: {e}")
    import traceback
    traceback.print_exc()

# Test frame generation step by step
print(f"\n=== TESTING FRAME GENERATION ===")
try:
    # Try manual frame generation like animate_helper does
    w_start = animator.window_starts[0]
    w_end = animator.window_ends[0]
    window = animator.get_window(animator.data, w_start, w_end)
    
    print(f"Manual window extraction:")
    print(f"  w_start: {w_start}, w_end: {w_end}")
    print(f"  Window shape: {window.shape}")
    print(f"  Window columns: {window.columns}")
    print(f"  Window sample:\n{window.head()}")
    
except Exception as e:
    print(f"Manual frame generation error: {e}")
    import traceback
    traceback.print_exc()