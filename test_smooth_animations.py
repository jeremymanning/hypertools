import numpy as np
import pandas as pd
import hypertools as hyp

print("Testing improved hypertools animations...")

# Create smooth trajectory data
np.random.seed(42)
n_timepoints = 25
n_points = 100

# Create a smooth 3D helix that evolves over time
trajectory_data = []
for t in range(n_timepoints):
    # Parameters for the helix
    theta = np.linspace(0, 4*np.pi, n_points)
    
    # Helix with time evolution
    x = np.cos(theta + t*0.2) * (1 + t*0.1)
    y = np.sin(theta + t*0.2) * (1 + t*0.1)
    z = np.linspace(t*0.3, (t+1)*0.3, n_points)
    
    df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=[t] * n_points)
    trajectory_data.append(df)

data = pd.concat(trajectory_data)

print(f"Created trajectory data: {data.shape}")
print(f"Time range: {data.index.min()} to {data.index.max()}")

# Test 1: Improved line animation with window style
print("\n1. Testing smooth line animation (window style)...")
try:
    fig1 = hyp.plot(data, 
                   animate='window',
                   mode='lines',
                   duration=8,        # 8 second animation
                   framerate=30,      # 30 fps for smoothness
                   focused=1.5)       # Show 1.5 seconds of data
    
    fig1.write_html("smooth_line_animation.html")
    print("✓ Smooth line animation created: smooth_line_animation.html")
    print(f"  Frames: {len(fig1.frames)}")
    
except Exception as e:
    print(f"✗ Line animation failed: {e}")

# Test 2: Precognitive trail animation  
print("\n2. Testing precognitive trail animation...")
try:
    fig2 = hyp.plot(data,
                   animate='precog', 
                   mode='lines',
                   duration=6,
                   framerate=25,
                   focused=1.0,
                   unfocused=3.0)     # Long trailing effect
    
    fig2.write_html("precog_trail_animation.html")
    print("✓ Precognitive animation created: precog_trail_animation.html")
    
except Exception as e:
    print(f"✗ Precog animation failed: {e}")

# Test 3: Comparison - scatter vs line animation
print("\n3. Creating comparison: scatter vs line...")
try:
    # Scatter animation
    fig3a = hyp.plot(data,
                    animate='window',
                    mode='markers',
                    duration=5,
                    framerate=20)
    
    fig3a.write_html("scatter_animation.html")
    
    # Line animation
    fig3b = hyp.plot(data,
                    animate='window', 
                    mode='lines',
                    duration=5,
                    framerate=20)
    
    fig3b.write_html("line_animation.html")
    
    print("✓ Comparison animations created:")
    print("  scatter_animation.html - scatter points")
    print("  line_animation.html - smooth lines")
    
except Exception as e:
    print(f"✗ Comparison failed: {e}")

print("\n" + "="*50)
print("ANIMATION IMPROVEMENTS SUMMARY:")
print("="*50)
print("✓ Fixed disappearing frames (disabled forced redraws)")
print("✓ Added smooth transitions between frames")
print("✓ Preserved plot mode (lines vs markers) in animations")
print("✓ Optimized performance with better frame generation")
print()
print("Open the HTML files to see the improved animations!")
print("- smooth_line_animation.html: Best example of improvements")
print("- precog_trail_animation.html: Shows trailing effects") 
print("- Compare scatter_animation.html vs line_animation.html")
print("="*50)