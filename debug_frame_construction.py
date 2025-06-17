import numpy as np
import pandas as pd
import plotly.graph_objects as go

print("=== DEBUGGING FRAME CONSTRUCTION STEP BY STEP ===")

# Replicate the exact interpolated window we saw in the debug
window_data = pd.DataFrame({
    'x': [0.0, 1.2, 1.0, 2.2, 2.0, 3.2],
    'y': [0.0, 0.0, 1.0, 1.0, 2.0, 2.0]
}, index=[0.0, 0.6, 0.0, 0.6, 0.0, 0.6])

print(f"Window data (from debug):")
print(window_data)

# Test get_datadict exactly as used in animate_helper
from hypertools.plot.animate import Animator
from hypertools.plot.static import flatten

print(f"\n=== TESTING GET_DATADICT ===")
mode = 'lines'

print(f"Data shape: {window_data.shape}")
print(f"Data values shape: {window_data.values.shape}")

# This is what get_datadict does:
x_raw = window_data.values[:, 0]
y_raw = window_data.values[:, 1]

print(f"Raw x: {x_raw}")
print(f"Raw y: {y_raw}")

x_flattened = flatten(x_raw)
y_flattened = flatten(y_raw)

print(f"Flattened x: {x_flattened}")
print(f"Flattened y: {y_flattened}")

# Create the scatter trace
trace = go.Scatter(x=x_flattened, y=y_flattened, mode=mode)

print(f"Trace created successfully!")
print(f"Trace x: {trace.x}")
print(f"Trace y: {trace.y}")

# Test creating a frame
frame = go.Frame(data=[trace], name="test_frame")
print(f"Frame created successfully!")
print(f"Frame data length: {len(frame.data)}")

# Test the frame data
if len(frame.data) > 0:
    frame_trace = frame.data[0]
    print(f"Frame trace x: {frame_trace.x}")
    print(f"Frame trace y: {frame_trace.y}")

print(f"\n=== TESTING SIMPLE PLOTLY FIGURE ===")
# Create a simple figure to test if this data works
fig = go.Figure()
fig.add_trace(trace)

try:
    # Try to render as HTML (this will fail if data format is wrong)
    html = fig.to_html()
    print(f"✅ Figure rendered successfully!")
    print(f"HTML length: {len(html)} characters")
except Exception as e:
    print(f"❌ Figure render failed: {e}")

print(f"\n=== DIAGNOSIS ===")
print("If this all works but animation is blank, the issue might be:")
print("1. Frame indexing/naming problems")
print("2. Animation controls not working") 
print("3. Base figure setup issues")
print("4. Multiple traces being treated incorrectly")