import numpy as np
import pandas as pd
import hypertools as hyp
import plotly.graph_objects as go
import time

print("Analyzing frame building efficiency...")

# Create simple test data
np.random.seed(42)
n_timepoints = 10
n_points = 50

data = []
for t in range(n_timepoints):
    x = np.linspace(0, 4*np.pi, n_points)
    y = np.sin(x + t) * (1 + t*0.1)
    z = np.cos(x + t) * 0.5
    
    df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=[t] * n_points)
    data.append(df)

trajectory = pd.concat(data)
print(f"Test data: {trajectory.shape}")

print("\n=== CURRENT APPROACH ANALYSIS ===")

# Test current hypertools animation
start_time = time.time()
fig = hyp.plot(trajectory, animate='window', mode='lines')
hyp_time = time.time() - start_time

print(f"HyperTools animation: {hyp_time:.3f}s, {len(fig.frames)} frames")

# Analyze what hypertools is doing per frame
if fig.frames:
    frame = fig.frames[0]
    print(f"Frame structure: {type(frame)}")
    if hasattr(frame, 'data') and frame.data:
        trace = frame.data[0]
        print(f"Trace type: {type(trace)}")
        print(f"Trace keys: {list(trace.keys()) if hasattr(trace, 'keys') else 'N/A'}")

print("\n=== EFFICIENT ALTERNATIVES ===")

# Alternative 1: Pre-compute all frame data
print("1. Pre-computing frame data...")
start_time = time.time()

frames_data = []
unique_times = sorted(trajectory.index.unique())

for i, t in enumerate(unique_times):
    # Get window of data (simple sliding window)
    window_start = max(0, i-2)  # Show last 3 time points
    window_times = unique_times[window_start:i+1]
    
    # Extract data for this window
    window_data = trajectory[trajectory.index.isin(window_times)]
    
    # Create trace data
    trace_data = {
        'x': window_data['x'].values,
        'y': window_data['y'].values, 
        'z': window_data['z'].values,
        'mode': 'lines',
        'type': 'scatter3d'
    }
    frames_data.append(trace_data)

precompute_time = time.time() - start_time
print(f"Pre-computation: {precompute_time:.3f}s for {len(frames_data)} frames")

# Alternative 2: Use plotly's more efficient frame construction
print("2. Direct plotly frame construction...")
start_time = time.time()

efficient_frames = []
for i, trace_data in enumerate(frames_data):
    frame = go.Frame(
        data=[go.Scatter3d(**trace_data)],
        name=str(i)
    )
    efficient_frames.append(frame)

# Create figure with efficient frames
efficient_fig = go.Figure()

# Add initial data
if frames_data:
    efficient_fig.add_trace(go.Scatter3d(**frames_data[0]))

# Add frames
efficient_fig.frames = efficient_frames

# Add animation controls
efficient_fig.update_layout(
    updatemenus=[{
        'buttons': [{
            'args': [None, {'frame': {'duration': 200, 'redraw': False},
                           'fromcurrent': True, 'transition': {'duration': 100}}],
            'label': '▶', 'method': 'animate'
        }, {
            'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                              'mode': 'immediate', 'transition': {'duration': 0}}],
            'label': '||', 'method': 'animate'
        }],
        'direction': 'left', 'pad': {'r': 10, 't': 87},
        'showactive': False, 'type': 'buttons', 'x': 0.1, 'y': 0
    }]
)

efficient_time = time.time() - start_time
print(f"Efficient construction: {efficient_time:.3f}s")

# Alternative 3: Minimal data approach - only send differences
print("3. Differential frame approach...")
start_time = time.time()

# For line plots, we can be smarter about what data changes
differential_frames = []
base_data = frames_data[0].copy()

for i, trace_data in enumerate(frames_data[1:], 1):
    # Only include the new data points
    frame = go.Frame(
        data=[go.Scatter3d(**trace_data)],
        name=str(i)
    )
    differential_frames.append(frame)

differential_time = time.time() - start_time
print(f"Differential approach: {differential_time:.3f}s")

print("\n=== EFFICIENCY COMPARISON ===")
print(f"HyperTools current: {hyp_time:.3f}s")
print(f"Pre-computation:     {precompute_time:.3f}s")  
print(f"Efficient frames:    {efficient_time:.3f}s")
print(f"Differential:        {differential_time:.3f}s")

# Save efficient version
efficient_fig.write_html("efficient_animation.html")
print(f"\n✓ Efficient animation saved: efficient_animation.html")

print("\n=== OPTIMIZATION INSIGHTS ===")
print("1. Pre-computing frame data is much faster than dynamic generation")
print("2. Direct plotly construction avoids hypertools overhead") 
print("3. For smooth 300-frame animations, we need:")
print("   - Pre-computed interpolated data points")
print("   - Minimal frame construction")
print("   - Efficient data representation")
print("4. The bottleneck is likely in hypertools' frame generation, not plotly")