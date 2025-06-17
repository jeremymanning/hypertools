import numpy as np
import pandas as pd
import hypertools as hyp

print("=== DEBUGGING DATA FLOW - WHY BLANK PLOT ===")

# Create simple test trajectory
data_trajectory = []
for t in range(4):
    x_values = np.array([t*2, t*2+1, t*2+2])
    y_values = np.array([0, 1, 2])
    
    df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 3)
    data_trajectory.append(df)

trajectory = pd.concat(data_trajectory)

print(f"Original trajectory:")
print(trajectory)

# Step 1: Test the Animator creation
print(f"\n=== STEP 1: ANIMATOR CREATION ===")
from hypertools.plot.animate import Animator

animator = Animator(trajectory, style='window', mode='lines', duration=1, framerate=5)

print(f"Interpolation enabled: {getattr(animator, 'use_interpolation', False)}")
if hasattr(animator, 'interpolated_data'):
    print(f"Interpolated data shape: {animator.interpolated_data.shape}")
    print(f"Interpolated data sample:")
    print(animator.interpolated_data.head())
else:
    print("❌ No interpolated_data attribute!")

# Step 2: Test window extraction
print(f"\n=== STEP 2: WINDOW EXTRACTION ===")
try:
    window = animator.get_window(animator.data, 0, 1)
    print(f"Window shape: {window.shape}")
    print(f"Window data:")
    print(window)
    
    if window.empty:
        print("❌ PROBLEM: Window is empty!")
    else:
        print(f"✅ Window has data: {len(window)} rows")
        
except Exception as e:
    print(f"❌ Window extraction failed: {e}")
    import traceback
    traceback.print_exc()

# Step 3: Test frame generation
print(f"\n=== STEP 3: FRAME GENERATION ===")
try:
    frame = animator.get_frame(0, simplify=True)
    print(f"Frame type: {type(frame)}")
    
    if hasattr(frame, 'data'):
        print(f"Frame has {len(frame.data)} data traces")
        if len(frame.data) > 0:
            trace = frame.data[0]
            print(f"Trace type: {type(trace)}")
            if hasattr(trace, 'x') and hasattr(trace, 'y'):
                print(f"Trace x: {list(trace.x)}")
                print(f"Trace y: {list(trace.y)}")
            else:
                print("❌ PROBLEM: Trace missing x/y data!")
        else:
            print("❌ PROBLEM: Frame has no data traces!")
    else:
        print("❌ PROBLEM: Frame has no data attribute!")
        
except Exception as e:
    print(f"❌ Frame generation failed: {e}")
    import traceback
    traceback.print_exc()

# Step 4: Test manual interpolated window
print(f"\n=== STEP 4: MANUAL INTERPOLATED WINDOW ===")
if hasattr(animator, '_get_interpolated_window'):
    try:
        manual_window = animator._get_interpolated_window(0, 1)
        print(f"Manual window shape: {manual_window.shape}")
        print(f"Manual window data:")
        print(manual_window)
        
        if manual_window.empty:
            print("❌ PROBLEM: Manual interpolated window is empty!")
        else:
            print(f"✅ Manual window has data: {len(manual_window)} rows")
            
    except Exception as e:
        print(f"❌ Manual interpolated window failed: {e}")
        import traceback
        traceback.print_exc()

print(f"\n=== DIAGNOSIS ===")
print("If the plot is blank, likely issues:")
print("1. Interpolated window returns empty data")
print("2. Frame generation doesn't use interpolated data") 
print("3. Data format incompatible with plotting system")
print("4. Animation frames not properly constructed")