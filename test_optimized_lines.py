import numpy as np
import pandas as pd
import hypertools as hyp
import time

print("Testing optimized line animations...")

# Create simple test data for line animation
np.random.seed(42)
n_timepoints = 8
n_points = 30

data = []
for t in range(n_timepoints):
    # Create connected line segments 
    x = np.linspace(0, 4*np.pi, n_points)
    y = np.sin(x + t*0.5) * (1 + t*0.1)
    z = np.cos(x + t*0.5) * 0.3
    
    df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=[t] * n_points)
    data.append(df)

trajectory = pd.concat(data)
print(f"Data: {trajectory.shape} ({n_timepoints} timepoints)")

# Test line animation performance
print("\n=== OPTIMIZED LINE ANIMATION ===")

start_time = time.time()
fig = hyp.plot(trajectory, animate='window', mode='lines', duration=4, framerate=20)
creation_time = time.time() - start_time

print(f"✓ Creation time: {creation_time:.3f} seconds")
print(f"  Frames generated: {len(fig.frames)}")
print(f"  Performance: {len(fig.frames)/creation_time:.1f} frames/second")

# Save for testing
fig.write_html("optimized_line_animation.html")

# Test scatter animation for comparison
print("\n=== SCATTER ANIMATION COMPARISON ===")

start_time = time.time()
fig_scatter = hyp.plot(trajectory, animate='window', mode='markers', duration=4, framerate=20)
scatter_time = time.time() - start_time

print(f"✓ Scatter creation: {scatter_time:.3f} seconds")
print(f"  Frames generated: {len(fig_scatter.frames)}")
print(f"  Performance: {len(fig_scatter.frames)/scatter_time:.1f} frames/second")

fig_scatter.write_html("optimized_scatter_animation.html")

print(f"\n=== PERFORMANCE COMPARISON ===")
print(f"Line animation:    {creation_time:.3f}s for {len(fig.frames)} frames")
print(f"Scatter animation: {scatter_time:.3f}s for {len(fig_scatter.frames)} frames")

if len(fig.frames) > len(fig_scatter.frames):
    print(f"✓ Line animation uses {len(fig.frames)} frames (interpolated)")
    print(f"✓ Scatter animation uses {len(fig_scatter.frames)} frames (discrete)")
else:
    print("⚠ Frame count optimization may not be working correctly")

print("\nTest files created:")
print("- optimized_line_animation.html (smooth interpolated)")
print("- optimized_scatter_animation.html (discrete frames)")

# Check if animations are smooth
import os
line_size = os.path.getsize("optimized_line_animation.html")
scatter_size = os.path.getsize("optimized_scatter_animation.html")

print(f"\nFile sizes:")
print(f"- Line: {line_size/1024/1024:.1f} MB")
print(f"- Scatter: {scatter_size/1024/1024:.1f} MB")