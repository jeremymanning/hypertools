import numpy as np
import pandas as pd
import hypertools as hyp

print("=== TESTING INTERPOLATED LINE ANIMATION ===")

# Create simple test trajectory
data_trajectory = []
for t in range(4):
    x_values = np.array([t*2, t*2+1, t*2+2])  # Moving line
    y_values = np.array([0, 1, 2])            # Diagonal
    
    df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 3)
    data_trajectory.append(df)

trajectory = pd.concat(data_trajectory)

print(f"Original trajectory:")
for t in trajectory.index.unique():
    subset = trajectory[trajectory.index == t]
    print(f"  Time {t}: x={list(subset.x)}")

print(f"\n=== TESTING NEW INTERPOLATION SYSTEM ===")

try:
    # Test the interpolation system
    from hypertools.plot.animate import Animator
    
    animator = Animator(trajectory, style='window', mode='lines', duration=2, framerate=10)
    
    print(f"Animation created successfully!")
    print(f"Using interpolation: {getattr(animator, 'use_interpolation', False)}")
    print(f"Total frames: {len(animator.angles)}")
    
    # Test a few frames
    print(f"\n=== TESTING FRAME GENERATION ===")
    for frame_i in [0, 5, 10, 15, 19]:
        if frame_i < len(animator.window_starts):
            try:
                frame = animator.get_frame(frame_i, simplify=True)
                if hasattr(frame, 'data') and frame.data and len(frame.data) > 0:
                    x_data = list(frame.data[0].x)[:6]  # First 6 points
                    x_formatted = [f'{x:.1f}' for x in x_data]
                    print(f"Frame {frame_i}: x={x_formatted}...")
                else:
                    print(f"Frame {frame_i}: No data")
            except Exception as e:
                print(f"Frame {frame_i}: Error - {e}")
    
    print(f"\n=== GENERATING FULL ANIMATION ===")
    try:
        fig = hyp.plot(trajectory, animate='window', mode='lines', 
                      duration=2, framerate=10, save_path='test_interpolated.html')
        print(f"✅ Animation saved to test_interpolated.html")
    except Exception as e:
        print(f"❌ Animation generation failed: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()

print(f"\n=== EXPECTED RESULTS ===")
print("✅ Should see smooth interpolated x values progressing")
print("✅ Each frame should have different x coordinates")  
print("✅ No more discrete jumps every 25+ frames")