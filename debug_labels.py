import numpy as np
import hypertools as hyp

# Create test data
np.random.seed(42)
data = np.random.randn(100, 3)
labels = ['Group A'] * 30 + ['Group B'] * 30 + ['Group C'] * 40

print(f"Data shape: {data.shape}")
print(f"Labels length: {len(labels)}")
print(f"Unique labels: {set(labels)}")

# Try to plot with labels
try:
    fig = hyp.plot(data, hue=labels)
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()