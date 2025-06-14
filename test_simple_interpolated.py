import numpy as np
import pandas as pd
import hypertools as hyp

print("=== TESTING BYPASSED ANIMATION ===")

# Create simple trajectory
data_trajectory = []
for t in range(3):  # Even simpler - just 3 timepoints
    x_values = np.array([t*2, t*2+1])  # Just 2 points per timepoint
    y_values = np.array([0, 1])        
    
    df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 2)
    data_trajectory.append(df)

trajectory = pd.concat(data_trajectory)

print(f"Simple trajectory:")
print(trajectory)

# Test just the frame generation (not full animation)
from hypertools.plot.animate import Animator

animator = Animator(trajectory, style='window', mode='lines', duration=1, framerate=3)

print(f"\n=== TESTING SIMPLE FRAME ===")
try:
    # Try to get frame with simplify=True (avoids static_plot)
    frame = animator.get_frame(0, simplify=True)
    print(f"✅ Frame generated with simplify=True")
    print(f"Frame data: {len(frame.data)} traces")
    
    if len(frame.data) > 0:
        trace = frame.data[0]
        print(f"Trace x: {trace.x}")
        print(f"Trace y: {trace.y}")
        
        # Create minimal animation directly
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0, 1, 2], y=[0, 1, 0], mode='lines', name='test'))
        
        # Add this frame
        frames = [frame]
        fig.frames = frames
        
        # Add basic animation controls
        fig.update_layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {'label': 'Play', 'method': 'animate', 'args': [None]},
                    {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0}}]}
                ]
            }]
        )
        
        # Save minimal test
        with open('test_minimal_animation.html', 'w') as f:
            f.write(fig.to_html(include_plotlyjs=True))
        
        print(f"✅ Minimal animation saved to test_minimal_animation.html")
        
except Exception as e:
    print(f"❌ Frame generation failed: {e}")
    import traceback
    traceback.print_exc()

print(f"\n=== DIAGNOSIS ===")
print("If this works, the issue is in build_animation() color handling")
print("If this fails, the issue is in frame data structuring")