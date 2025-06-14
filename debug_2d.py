import numpy as np
import hypertools as hyp

# Create 2D data
data_2d = np.random.randn(50, 2)
print(f"Original data shape: {data_2d.shape}")

# Plot and check what happens
fig = hyp.plot(data_2d)
print(f"Figure type: {type(fig)}")