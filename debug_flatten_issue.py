import numpy as np
import pandas as pd

# Test the flatten function issue
from hypertools.plot.static import flatten

print("=== DEBUGGING FLATTEN FUNCTION ISSUE ===")

# Create sample interpolated window data (like we get from interpolation)
window_data = pd.DataFrame({
    'x': [0.0, 1.2, 1.0, 2.2, 2.0, 3.2],
    'y': [0.0, 0.0, 1.0, 1.0, 2.0, 2.0]
})

print(f"Window data:")
print(window_data)

print(f"\n=== TESTING FLATTEN ===")
x_values = window_data.values[:, 0]
print(f"Raw x values: {x_values}")
print(f"Raw x type: {type(x_values)}")

flattened_x = flatten(x_values)
print(f"Flattened x: {flattened_x}")
print(f"Flattened x type: {type(flattened_x)}")

print(f"\n=== WHAT PLOTLY EXPECTS ===")
print(f"Plotly expects: [0.0, 1.2, 1.0, 2.2, 2.0, 3.2]")
print(f"We're giving: {flattened_x}")

print(f"\n=== TESTING SIMPLE CONVERSION ===")
simple_x = list(x_values)
print(f"Simple list conversion: {simple_x}")
print(f"Simple list type: {type(simple_x)}")

# Test with Plotly
print(f"\n=== TESTING WITH PLOTLY ===")
import plotly.graph_objects as go

try:
    # Test with flattened (broken) data
    trace1 = go.Scatter(x=flattened_x, y=flatten(window_data.values[:, 1]), mode='lines')
    print(f"✅ Plotly accepted flattened data: {len(trace1.x)} points")
    print(f"Trace x sample: {trace1.x}")
except Exception as e:
    print(f"❌ Plotly rejected flattened data: {e}")

try:
    # Test with simple list (correct) data  
    trace2 = go.Scatter(x=simple_x, y=list(window_data.values[:, 1]), mode='lines')
    print(f"✅ Plotly accepted simple data: {len(trace2.x)} points")
    print(f"Trace x sample: {trace2.x}")
except Exception as e:
    print(f"❌ Plotly rejected simple data: {e}")

print(f"\n=== SOLUTION ===")
print("Replace flatten() with simple list() conversion for interpolated data")