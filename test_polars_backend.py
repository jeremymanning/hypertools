import numpy as np
import pandas as pd
import polars as pl
import datawrangler as dw
import time

print("=== TESTING POLARS BACKEND ===")

# Create test data
data = np.random.randn(1000, 3)
df_pandas = pd.DataFrame(data, columns=['x', 'y', 'z'])
df_polars = pl.DataFrame(data, schema=['x', 'y', 'z'])

print(f"Created test data: {data.shape}")
print(f"Pandas DataFrame: {type(df_pandas)}")
print(f"Polars DataFrame: {type(df_polars)}")

# Test datawrangler with different backends
print("\n=== DATAWRANGLER BACKEND TESTS ===")

# Test pandas backend (default)
print("\n1. Pandas backend (default):")
start = time.time()
try:
    wrapped_pandas = dw.wrangle(df_pandas)
    stacked_pandas = dw.stack(wrapped_pandas)
    pandas_time = time.time() - start
    print(f"✅ SUCCESS - Time: {pandas_time:.4f}s")
    print(f"   Wrapped type: {type(wrapped_pandas)}")
    print(f"   Stacked shape: {stacked_pandas.shape}")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test polars backend
print("\n2. Polars backend:")
start = time.time()
try:
    # Test if we can set backend
    wrapped_polars = dw.wrangle(df_polars, backend='polars')
    stacked_polars = dw.stack(wrapped_polars)
    polars_time = time.time() - start
    print(f"✅ SUCCESS - Time: {polars_time:.4f}s")
    print(f"   Wrapped type: {type(wrapped_polars)}")
    print(f"   Stacked shape: {stacked_polars.shape}")
    
    # Calculate speedup
    if 'pandas_time' in locals():
        speedup = pandas_time / polars_time
        print(f"   Speedup: {speedup:.2f}x faster than pandas")
        
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test with hypertools data format
print("\n=== HYPERTOOLS COMPATIBILITY TEST ===")

# Create multi-timepoint data like hypertools uses
trajectory_data = []
for t in range(4):
    points = np.random.randn(5, 3)
    df = pd.DataFrame(points, columns=['x', 'y', 'z'], index=[t] * 5)
    trajectory_data.append(df)

combined_trajectory = pd.concat(trajectory_data)
print(f"HyperTools trajectory shape: {combined_trajectory.shape}")
print(f"Unique timepoints: {combined_trajectory.index.unique()}")

# Test polars conversion
try:
    # Convert to polars
    polars_trajectory = pl.from_pandas(combined_trajectory)
    print(f"✅ Polars conversion successful: {polars_trajectory.shape}")
    
    # Test datawrangler with polars trajectory
    wrapped_polars_traj = dw.wrangle(polars_trajectory, backend='polars')
    print(f"✅ DataWrangler polars wrangle successful")
    
except Exception as e:
    print(f"❌ Polars trajectory test failed: {e}")

print("\n=== SUMMARY ===")
print("Next steps for Polars integration:")
print("1. Update hypertools data loading to use Polars")
print("2. Modify animation logic to work with Polars DataFrames") 
print("3. Benchmark performance improvements in real hypertools workflows")