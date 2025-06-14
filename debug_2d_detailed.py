import numpy as np
import pandas as pd
import hypertools as hyp
from hypertools.plot import static

# Monkey patch to debug
original_get_plotly_shape = static.get_plotly_shape

def debug_get_plotly_shape(x, **kwargs):
    print(f"get_plotly_shape called with data shape: {x.shape}")
    return original_get_plotly_shape(x, **kwargs)

static.get_plotly_shape = debug_get_plotly_shape

# Also patch static_plot
original_static_plot = static.static_plot

def debug_static_plot(data, **kwargs):
    print(f"static_plot called with data type: {type(data)}")
    if hasattr(data, 'shape'):
        print(f"  Data shape: {data.shape}")
    return original_static_plot(data, **kwargs)

static.static_plot = debug_static_plot

# Create 2D data
data_2d = np.random.randn(50, 2)
print(f"Original data shape: {data_2d.shape}")

# Test the plot function pipeline
from hypertools.plot.plot import plot

# Check pad function behavior
from hypertools.align.common import pad
print(f"\nTesting pad function:")
padded = pad(pd.DataFrame(data_2d), 3)
print(f"Padded shape: {padded.shape}")

# Plot
try:
    fig = plot(data_2d)
    print(f"\nSuccessfully created figure")
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()