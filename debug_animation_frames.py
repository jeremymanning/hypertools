import numpy as np
import pandas as pd
import hypertools as hyp

print("=== DEBUGGING ANIMATION FRAME GENERATION ===")

# Create simple test data
data_simple = []
for t in range(4):
    x = np.array([t, t+1, t+2])  # Each timepoint has different x values
    y = np.array([0, 1, 2])      # Consistent y values
    
    df = pd.DataFrame({'x': x, 'y': y}, index=[t] * 3)
    data_simple.append(df)

simple_trajectory = pd.concat(data_simple)
print(f"Data timepoints: {simple_trajectory.index.unique()}")
print(f"X ranges by timepoint:")
for t in simple_trajectory.index.unique():
    subset = simple_trajectory[simple_trajectory.index == t]
    print(f"  Time {t}: x=[{subset.x.min()}-{subset.x.max()}]")

# Create animator and examine frame generation
from hypertools.plot.animate import Animator

print(f"\n=== TESTING SLIDING WINDOW ===")
animator = Animator(simple_trajectory, style='window', mode='lines')

print(f"Total frames: {len(animator.angles)}")
print(f"Animation indices: {len(animator.indices)} values")
print(f"Window starts: {len(animator.window_starts)} values")

# Test first few frames manually
print(f"\n=== FRAME CONTENT ANALYSIS ===")
for i in [0, 25, 50, 75, 100]:
    if i < len(animator.window_starts):
        try:
            frame = animator.get_frame(i, simplify=True)
            if hasattr(frame, 'data') and frame.data:
                x_data = frame.data[0].x if hasattr(frame.data[0], 'x') else []
                y_data = frame.data[0].y if hasattr(frame.data[0], 'y') else []
                print(f"Frame {i}: x={list(x_data)[:5]}..., y={list(y_data)[:5]}...")
            else:
                print(f"Frame {i}: No data")
        except Exception as e:
            print(f"Frame {i}: Error - {e}")

print(f"\n=== TESTING SPINNING ANIMATION ===")
spinner = Animator(simple_trajectory, style='spin', mode='markers')
print(f"Spin animation angles: {len(spinner.angles)} frames")
print(f"Angle range: {spinner.angles[0]:.1f} to {spinner.angles[-1]:.1f} degrees")

# Test a few spinning frames
for i in [0, 25, 50, 75]:
    if i < len(spinner.angles):
        try:
            frame = spinner.get_frame(i, simplify=True)
            print(f"Spin frame {i}: angle={spinner.angles[i]:.1f}°")
        except Exception as e:
            print(f"Spin frame {i}: Error - {e}")

print(f"\n=== DIAGNOSIS ===")
print("Potential issues:")
print("1. Frame generation not creating different data")
print("2. Plotly animation controls not working")
print("3. Window calculation still incorrect") 
print("4. Camera rotation not being applied to frames")