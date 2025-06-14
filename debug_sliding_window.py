import numpy as np
import pandas as pd
import hypertools as hyp

print("Debugging sliding window animation content...")

# Create very simple test data - just 4 timepoints
data_simple = []
for t in range(4):
    # Simple line: 5 points per timepoint
    x = np.array([0, 1, 2, 3, 4]) + t*5  # Each timepoint offset by 5
    y = np.array([t, t, t, t, t])        # Constant y per timepoint  
    z = np.array([0, 0, 0, 0, 0])        # Flat z
    
    df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=[t] * 5)
    data_simple.append(df)

simple_trajectory = pd.concat(data_simple)

print("Simple trajectory data:")
for t in range(4):
    t_data = simple_trajectory[simple_trajectory.index == t]
    print(f"Time {t}: x={t_data['x'].values}, y={t_data['y'].values}")

# What should sliding window animation show?
print("\n=== EXPECTED SLIDING WINDOW BEHAVIOR ===")
print("Frame 0: Show timepoint 0 only")
print("Frame 1: Show timepoints 0-1 connected")  
print("Frame 2: Show timepoints 0-2 connected")
print("Frame 3: Show timepoints 0-3 connected")
print("OR with sliding window:")
print("Frame 0: Show timepoint 0")
print("Frame 1: Show timepoint 1") 
print("Frame 2: Show timepoint 2")
print("Frame 3: Show timepoint 3")

# Test actual animation
print("\n=== TESTING ACTUAL ANIMATION ===")

fig = hyp.plot(simple_trajectory, animate='window', mode='lines')

print(f"Generated {len(fig.frames)} frames")

# Examine first few frames
for i in range(min(4, len(fig.frames))):
    frame = fig.frames[i]
    if hasattr(frame, 'data') and frame.data:
        trace = frame.data[0]
        if hasattr(trace, 'x'):
            x_vals = trace.x if hasattr(trace, 'x') else []
            y_vals = trace.y if hasattr(trace, 'y') else []
            print(f"Frame {i}: {len(x_vals)} points, x={x_vals[:5]}..., y={y_vals[:5]}...")

fig.write_html("debug_sliding_window.html")
print("\n✓ Saved debug_sliding_window.html")

print("\n=== ANALYSIS ===")
print("Check debug_sliding_window.html to see:")
print("1. Does each frame show the correct time window?")
print("2. Are the line segments connected properly?") 
print("3. Does the window slide smoothly?")
print("4. Are we getting proper sliding window behavior vs growing?")

# Also test static plot for comparison
static_fig = hyp.plot(simple_trajectory, mode='lines')
static_fig.write_html("debug_static_reference.html")
print("\n✓ Static reference: debug_static_reference.html")