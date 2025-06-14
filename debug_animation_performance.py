import numpy as np
import pandas as pd
import hypertools as hyp
import time

print("Analyzing animation performance issues...")

# Create simple test data
np.random.seed(42)
n_timepoints = 10  # Small number to start
n_points = 20      # Small number of points

print(f"Test data: {n_timepoints} timepoints, {n_points} points each")

# Create simple trajectory
data = []
for t in range(n_timepoints):
    x = np.linspace(0, t, n_points)
    y = np.sin(x + t)
    z = np.cos(x + t) * 0.5
    
    df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=[t] * n_points)
    data.append(df)

trajectory = pd.concat(data)
print(f"Combined data shape: {trajectory.shape}")

# Test current performance
print("\n=== PERFORMANCE ANALYSIS ===")

start_time = time.time()
try:
    fig = hyp.plot(trajectory, animate='window', mode='lines')
    creation_time = time.time() - start_time
    
    print(f"✓ Animation creation time: {creation_time:.2f} seconds")
    print(f"  Number of frames: {len(fig.frames) if fig.frames else 0}")
    
    # Analyze frame size
    if fig.frames:
        frame_sizes = []
        for i, frame in enumerate(fig.frames[:3]):  # Check first 3 frames
            if hasattr(frame, 'data') and frame.data:
                frame_sizes.append(len(frame.data))
                print(f"  Frame {i}: {len(frame.data)} data objects")
                
                # Look at first data object
                if frame.data[0]:
                    d = frame.data[0]
                    if hasattr(d, 'x') and d.x:
                        print(f"    Data points in frame {i}: {len(d.x)}")
        
        print(f"  Average data objects per frame: {np.mean(frame_sizes):.1f}")
    
    # Save and check file size
    filename = "performance_test.html"
    fig.write_html(filename)
    
    import os
    file_size = os.path.getsize(filename)
    print(f"  HTML file size: {file_size / 1024 / 1024:.1f} MB")
    
except Exception as e:
    print(f"✗ Animation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== PROPOSED OPTIMIZATIONS ===")
print("1. Reduce frame count (currently generating too many frames)")
print("2. Optimize data representation (avoid redundant data)")
print("3. Use more efficient plotly animation approach")
print("4. Pre-calculate sliding windows instead of dynamic generation")

# Test with reduced parameters
print("\n=== TESTING OPTIMIZED PARAMETERS ===")

start_time = time.time()
try:
    fig_opt = hyp.plot(trajectory, 
                      animate='window', 
                      mode='lines',
                      duration=3,      # Shorter duration
                      framerate=10,    # Lower framerate  
                      focused=2.0)     # Longer window
    
    opt_time = time.time() - start_time
    print(f"✓ Optimized animation time: {opt_time:.2f} seconds")
    print(f"  Frames: {len(fig_opt.frames) if fig_opt.frames else 0}")
    
    fig_opt.write_html("performance_optimized.html")
    file_size_opt = os.path.getsize("performance_optimized.html")
    print(f"  Optimized file size: {file_size_opt / 1024 / 1024:.1f} MB")
    
except Exception as e:
    print(f"✗ Optimized animation failed: {e}")

print("\n=== ANALYSIS COMPLETE ===")
print("Check performance_test.html vs performance_optimized.html")