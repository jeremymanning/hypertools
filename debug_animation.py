import numpy as np
import pandas as pd
import hypertools as hyp

# Create test data with time series
np.random.seed(42)
n_timepoints = 20
n_features = 3

# Create data that changes over time
t = np.linspace(0, 4*np.pi, n_timepoints)
data = []

for i in range(n_timepoints):
    # Create a spiral that evolves over time
    x = np.sin(t[i]) * np.linspace(0.1, 1, 50)
    y = np.cos(t[i]) * np.linspace(0.1, 1, 50)
    z = np.linspace(0, t[i]/4, 50)
    
    # Add some noise
    x += np.random.randn(50) * 0.1
    y += np.random.randn(50) * 0.1
    z += np.random.randn(50) * 0.1
    
    # Create DataFrame with time index
    df = pd.DataFrame({
        'x': x,
        'y': y, 
        'z': z
    }, index=[i] * 50)  # Use time as index
    
    data.append(df)

# Combine into single DataFrame
combined_data = pd.concat(data)
print(f"Combined data shape: {combined_data.shape}")
print(f"Index range: {combined_data.index.min()} to {combined_data.index.max()}")
print(f"Unique time points: {len(combined_data.index.unique())}")

# Test basic animation
print("\nTesting basic animation...")
try:
    fig = hyp.plot(combined_data, animate=True)
    print("✓ Basic animation successful")
    print(f"Figure type: {type(fig)}")
    
    # Check if it has animation frames
    if hasattr(fig, 'frames'):
        print(f"Number of frames: {len(fig.frames) if fig.frames else 0}")
    
except Exception as e:
    print(f"✗ Basic animation failed: {e}")
    import traceback
    traceback.print_exc()

# Test different animation styles
styles = ['window', 'precog']
for style in styles:
    print(f"\nTesting animation style: {style}")
    try:
        fig = hyp.plot(combined_data, animate=style)
        print(f"✓ Animation style '{style}' successful")
    except Exception as e:
        print(f"✗ Animation style '{style}' failed: {e}")
        import traceback
        traceback.print_exc()