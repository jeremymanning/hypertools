import numpy as np
import pandas as pd
import hypertools as hyp

print("=== DEBUGGING EXACT ANIMATION FLOW ===")

# Create the exact same trajectory as in our test
data_trajectory = []
for t in range(4):
    x_values = np.array([t*2, t*2+1, t*2+2])
    y_values = np.array([0, 1, 2])
    
    df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 3)
    data_trajectory.append(df)

trajectory = pd.concat(data_trajectory)

# Create animator and inspect every step
from hypertools.plot.animate import Animator

animator = Animator(trajectory, style='window', mode='lines', duration=1, framerate=5)

print(f"=== FRAME 0 DETAILED ANALYSIS ===")
frame_0 = animator.get_frame(0, simplify=True)

print(f"Frame type: {type(frame_0)}")
print(f"Frame name: {frame_0.name}")
print(f"Frame data count: {len(frame_0.data)}")

for i, trace in enumerate(frame_0.data):
    print(f"\nTrace {i}:")
    print(f"  Type: {type(trace)}")
    print(f"  Mode: {getattr(trace, 'mode', 'unknown')}")
    print(f"  X data: {trace.x}")
    print(f"  Y data: {trace.y}")
    print(f"  X type: {type(trace.x)}")
    print(f"  Y type: {type(trace.y)}")

# Compare with frame 1
print(f"\n=== FRAME 1 DETAILED ANALYSIS ===")
if len(animator.window_starts) > 1:
    frame_1 = animator.get_frame(1, simplify=True)
    
    print(f"Frame 1 data count: {len(frame_1.data)}")
    for i, trace in enumerate(frame_1.data):
        print(f"\nTrace {i}:")
        print(f"  X data: {trace.x}")
        print(f"  Y data: {trace.y}")

# Test the complete animation build
print(f"\n=== TESTING COMPLETE ANIMATION BUILD ===")
try:
    full_animation = animator.build_animation()
    print(f"Animation built successfully!")
    print(f"Animation frames: {len(full_animation.frames)}")
    print(f"Animation layout keys: {list(full_animation.layout.keys())}")
    
    # Check first frame in full animation
    if len(full_animation.frames) > 0:
        first_frame = full_animation.frames[0]
        print(f"First frame data count: {len(first_frame.data)}")
        if len(first_frame.data) > 0:
            print(f"First frame trace x: {first_frame.data[0].x}")
            
except Exception as e:
    print(f"❌ Animation build failed: {e}")
    import traceback
    traceback.print_exc()

print(f"\n=== KEY DIAGNOSTICS ===")
print("1. Are frame data different between frames?")
print("2. Are the traces correctly formatted?")
print("3. Is the animation layout correct?")
print("4. Are there any empty traces?")