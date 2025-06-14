import numpy as np
import pandas as pd
import hypertools as hyp

# Create a simple time series that should animate smoothly
np.random.seed(42)
n_timepoints = 20
n_points_per_frame = 50

print("Creating simple line plot animation test...")

# Create a smooth trajectory that evolves over time
time_data = []
for t in range(n_timepoints):
    # Create a smooth 3D trajectory (like a helix)
    theta = np.linspace(0, 2*np.pi, n_points_per_frame)
    
    # Helix that progresses over time
    x = np.cos(theta + t*0.3) * (1 + t*0.1)
    y = np.sin(theta + t*0.3) * (1 + t*0.1)  
    z = np.linspace(t*0.5, (t+1)*0.5, n_points_per_frame)
    
    # Create DataFrame with time index
    df = pd.DataFrame({
        'x': x,
        'y': y,
        'z': z
    }, index=[t] * n_points_per_frame)
    
    time_data.append(df)

# Combine data
trajectory_data = pd.concat(time_data)
print(f"Trajectory data shape: {trajectory_data.shape}")
print(f"Time points: {trajectory_data.index.min()} to {trajectory_data.index.max()}")

# Test static line plot first
print("\n1. Testing static line plot...")
try:
    static_fig = hyp.plot(trajectory_data, mode='lines')
    print("✓ Static line plot successful")
except Exception as e:
    print(f"✗ Static line plot failed: {e}")

# Test simple animation with line mode
print("\n2. Testing simple line animation...")
try:
    anim_fig = hyp.plot(trajectory_data, animate='window', mode='lines')
    print("✓ Line animation successful")
    
    # Save for inspection
    anim_fig.write_html("debug_line_animation.html")
    print("  Saved as: debug_line_animation.html")
    
    # Check animation properties
    if hasattr(anim_fig, 'frames') and anim_fig.frames:
        print(f"  Number of frames: {len(anim_fig.frames)}")
        
        # Check first few frames
        for i in range(min(3, len(anim_fig.frames))):
            frame = anim_fig.frames[i]
            if hasattr(frame, 'data') and frame.data:
                print(f"  Frame {i}: {len(frame.data)} traces")
            
except Exception as e:
    print(f"✗ Line animation failed: {e}")
    import traceback
    traceback.print_exc()

# Test with different parameters for smoother animation
print("\n3. Testing with smoother parameters...")
try:
    smooth_fig = hyp.plot(trajectory_data, 
                         animate='window',
                         mode='lines',
                         duration=5,  # 5 second duration
                         framerate=30,  # 30 fps
                         focused=1.0)  # Show 1 second of data
    print("✓ Smooth line animation successful")
    
    smooth_fig.write_html("debug_smooth_animation.html")
    print("  Saved as: debug_smooth_animation.html")
    
except Exception as e:
    print(f"✗ Smooth animation failed: {e}")

print("\nAnimation test complete!")
print("Check the HTML files to see if animations are smooth.")