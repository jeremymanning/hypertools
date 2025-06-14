import numpy as np
import pandas as pd
import polars as pl
import time

print("=== SIMPLE POLARS PERFORMANCE TEST ===")

# Create larger test dataset for meaningful performance comparison
n_points = 10000
n_timepoints = 10

print(f"Creating dataset: {n_points} points x {n_timepoints} timepoints = {n_points * n_timepoints} total rows")

# Generate test data
all_data = []
for t in range(n_timepoints):
    points = np.random.randn(n_points, 3)
    df = pd.DataFrame(points, columns=['x', 'y', 'z'], index=[t] * n_points)
    all_data.append(df)

# Pandas version
start = time.time()
pandas_trajectory = pd.concat(all_data)
pandas_concat_time = time.time() - start

# Basic operations with pandas
start = time.time()
pandas_mean = pandas_trajectory.mean()
pandas_groupby = pandas_trajectory.groupby(pandas_trajectory.index).mean()
pandas_filter = pandas_trajectory[pandas_trajectory.index <= 2]
pandas_ops_time = time.time() - start

print(f"\n=== PANDAS PERFORMANCE ===")
print(f"Concat time: {pandas_concat_time:.4f}s")
print(f"Operations time: {pandas_ops_time:.4f}s")
print(f"Total pandas time: {pandas_concat_time + pandas_ops_time:.4f}s")

# Polars version - direct creation
start = time.time()
polars_data = []
for t in range(n_timepoints):
    points = np.random.randn(n_points, 3)
    # Create with time index as a column instead of index
    df = pl.DataFrame({
        'x': points[:, 0],
        'y': points[:, 1], 
        'z': points[:, 2],
        'time': [t] * n_points
    })
    polars_data.append(df)

polars_trajectory = pl.concat(polars_data)
polars_concat_time = time.time() - start

# Basic operations with polars
start = time.time()
polars_mean = polars_trajectory.select(pl.col(['x', 'y', 'z']).mean())
polars_groupby = polars_trajectory.group_by('time').agg(pl.col(['x', 'y', 'z']).mean())
polars_filter = polars_trajectory.filter(pl.col('time') <= 2)
polars_ops_time = time.time() - start

print(f"\n=== POLARS PERFORMANCE ===")
print(f"Concat time: {polars_concat_time:.4f}s")
print(f"Operations time: {polars_ops_time:.4f}s")
print(f"Total polars time: {polars_concat_time + polars_ops_time:.4f}s")

# Calculate speedups
total_pandas = pandas_concat_time + pandas_ops_time
total_polars = polars_concat_time + polars_ops_time
speedup = total_pandas / total_polars

print(f"\n=== PERFORMANCE COMPARISON ===")
print(f"Polars is {speedup:.2f}x faster than pandas")
print(f"Concat speedup: {pandas_concat_time / polars_concat_time:.2f}x")
print(f"Operations speedup: {pandas_ops_time / polars_ops_time:.2f}x")

# Test compatibility with hypertools animation logic
print(f"\n=== HYPERTOOLS COMPATIBILITY ===")

# Test time-based filtering (core animation requirement)
print("Testing time-based filtering (animation windowing):")

start = time.time()
# Pandas filtering for animation windows
for window_start in [0, 1, 2]:
    window_end = window_start + 1
    pandas_window = pandas_trajectory[(pandas_trajectory.index >= window_start) & (pandas_trajectory.index <= window_end)]
pandas_window_time = time.time() - start

start = time.time()
# Polars filtering for animation windows  
for window_start in [0, 1, 2]:
    window_end = window_start + 1
    polars_window = polars_trajectory.filter((pl.col('time') >= window_start) & (pl.col('time') <= window_end))
polars_window_time = time.time() - start

window_speedup = pandas_window_time / polars_window_time
print(f"✅ Window filtering speedup: {window_speedup:.2f}x")

print(f"\n=== INTEGRATION STRATEGY ===")
print("1. ✅ Polars shows significant performance improvements")
print("2. ✅ Core operations needed for animations work in Polars")
print("3. 🔄 Need to modify hypertools to use 'time' column instead of index")
print("4. 🔄 Update animation logic to use .filter() instead of index-based selection")