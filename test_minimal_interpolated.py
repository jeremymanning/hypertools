import numpy as np
import pandas as pd
import hypertools as hyp

print("=== MINIMAL INTERPOLATED ANIMATION TEST ===")

# Very simple 2-timepoint trajectory
data_simple = []
for t in [0, 1]:  # Just 2 timepoints for simplicity
    x_values = np.array([t, t+1])  # [0,1] and [1,2]
    y_values = np.array([0, 1])    # [0,1] and [0,1]
    
    df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 2)
    data_simple.append(df)

trajectory = pd.concat(data_simple)
print(f"Simple trajectory:")
print(trajectory)

try:
    # Test with minimal parameters to avoid color issues
    print(f"\n=== TESTING MINIMAL ANIMATION ===")
    fig = hyp.plot(trajectory, animate='window', mode='lines', 
                  duration=1, framerate=5,  # Very short animation
                  color=None,  # Explicit no color to avoid color issues
                  save_path='test_minimal.html')
    print(f"✅ Minimal animation successful!")
    
except Exception as e:
    print(f"❌ Minimal animation failed: {e}")
    
    # Try with even simpler approach - test the plotting without animation first
    print(f"\n=== TESTING STATIC PLOT FIRST ===")
    try:
        static_fig = hyp.plot(trajectory, mode='lines', color=None)
        print(f"✅ Static plot successful!")
        
        # Now try animation without save
        print(f"\n=== TESTING ANIMATION WITHOUT SAVE ===")
        anim_fig = hyp.plot(trajectory, animate='window', mode='lines', 
                           duration=1, framerate=5, color=None)
        print(f"✅ Animation without save successful!")
        
    except Exception as e2:
        print(f"❌ Even simpler test failed: {e2}")
        import traceback
        traceback.print_exc()