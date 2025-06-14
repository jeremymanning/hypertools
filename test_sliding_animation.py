import numpy as np
import pandas as pd
import hypertools as hyp

print("=== TESTING SLIDING WINDOW ANIMATION ===")

# Create simple 2D trajectory data that's easy to visualize
data_trajectory = []
for t in range(4):
    # Create a simple line that moves across the plot over time
    x_values = np.array([t, t+1, t+2])  # Line moves right with each timepoint
    y_values = np.array([0, 1, 2])      # Consistent diagonal line
    
    df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 3)
    data_trajectory.append(df)

trajectory = pd.concat(data_trajectory)
print(f"Trajectory data:")
print(trajectory.groupby(trajectory.index).apply(lambda x: f"Time {x.index[0]}: x=[{x.x.min()}-{x.x.max()}], y=[{x.y.min()}-{x.y.max()}]"))

# Create sliding window animation
print(f"\nGenerating sliding window animation...")

try:
    fig = hyp.plot(trajectory, animate='window', mode='lines', save_path='test_sliding_animation.html')
    print(f"✅ Animation generated successfully!")
    print(f"✅ Saved to: test_sliding_animation.html")
    
    # Test that the animation object has the expected properties
    print(f"\nAnimation properties:")
    print(f"  Number of frames: {len(fig.frames) if hasattr(fig, 'frames') else 'No frames'}")
    print(f"  Frame names: {[f.name for f in fig.frames[:5]] if hasattr(fig, 'frames') else 'No frames'}")
    
    if hasattr(fig, 'frames') and len(fig.frames) > 0:
        # Check first and last frames to see if they have different data
        first_frame = fig.frames[0]
        last_frame = fig.frames[-1]
        
        print(f"  First frame data points: {len(first_frame.data[0].x) if first_frame.data else 0}")
        print(f"  Last frame data points: {len(last_frame.data[0].x) if last_frame.data else 0}")
        
        if first_frame.data and last_frame.data:
            first_x = list(first_frame.data[0].x)
            last_x = list(last_frame.data[0].x)
            print(f"  First frame X values: {first_x}")
            print(f"  Last frame X values: {last_x}")
            
            if first_x != last_x:
                print(f"  ✅ SUCCESS: Frames have different data (sliding window working!)")
            else:
                print(f"  ❌ FAILED: Frames have identical data")
    
except Exception as e:
    print(f"❌ Animation failed: {e}")
    import traceback
    traceback.print_exc()

print(f"\n=== TEST SUMMARY ===")
print(f"The sliding window animation should show:")
print(f"- Early frames: Lines starting from left side (x=0,1,2)")
print(f"- Later frames: Lines moving right (x=3,4,5)")
print(f"- Progressive sliding through timepoints 0→1→2→3")