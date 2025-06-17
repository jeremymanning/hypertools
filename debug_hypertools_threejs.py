#!/usr/bin/env python3
"""
Debug the specific HyperTools Three.js issue with detailed inspection
"""

import numpy as np
import pandas as pd
import sys
import os

# Add hypertools to path
sys.path.insert(0, '/Users/jmanning/hypertools')

import hypertools as hyp
from hypertools.core.threejs_backend import HyperToolsFigure

def debug_2d_scatter_issue():
    """Debug the 2D scatter points appearing on y=0 line"""
    print("🔍 DEBUGGING 2D SCATTER ISSUE")
    print("=" * 50)
    
    # Create simple 2D scatter data (same as problematic case)
    np.random.seed(123)
    data_2d = np.random.randn(5, 2) * 2
    print(f"Original data shape: {data_2d.shape}")
    print(f"Original data:\n{data_2d}")
    print(f"Y values range: {data_2d[:, 1].min():.2f} to {data_2d[:, 1].max():.2f}")
    
    # Create HyperTools figure
    print("\n📊 Creating HyperTools figure...")
    fig = hyp.plot(data_2d, 'ro', markersize=8, alpha=0.7)
    
    # Inspect the figure's internal data
    print("\n🔎 INSPECTING INTERNAL DATA:")
    print(f"Number of datasets: {fig.n_datasets}")
    print(f"Dimensionality: {fig.dimensionality}")
    
    for i, dataset in enumerate(fig.datasets):
        print(f"\nDataset {i}:")
        print(f"  Shape: {dataset.shape}")
        print(f"  Columns: {list(dataset.columns)}")
        print(f"  Data:\n{dataset}")
        print(f"  X range: {dataset['x'].min():.2f} to {dataset['x'].max():.2f}")
        print(f"  Y range: {dataset['y'].min():.2f} to {dataset['y'].max():.2f}")
    
    # Inspect Three.js position conversion
    print("\n🎯 TESTING POSITION CONVERSION:")
    positions = fig._data_to_positions(fig.datasets[0])
    print(f"Positions array shape: {positions.shape}")
    print(f"Positions array: {positions}")
    
    # Reshape to see individual points
    positions_3d = positions.reshape(-1, 3)
    print(f"Reshaped positions (N x 3):\n{positions_3d}")
    print(f"X positions: {positions_3d[:, 0]}")
    print(f"Y positions: {positions_3d[:, 1]}")
    print(f"Z positions: {positions_3d[:, 2]}")
    
    # Check camera setup
    print("\n📷 INSPECTING CAMERA SETUP:")
    print(f"Camera type: {type(fig.camera)}")
    if hasattr(fig.camera, 'left'):
        print(f"Orthographic bounds:")
        print(f"  Left: {fig.camera.left}")
        print(f"  Right: {fig.camera.right}")
        print(f"  Top: {fig.camera.top}")
        print(f"  Bottom: {fig.camera.bottom}")
    
    print(f"Camera position: {fig.camera.position}")
    
    # Test if the issue is in the renderer/display
    print("\n🖥️  TESTING RENDERER:")
    try:
        renderer = fig.show()
        print("✅ Renderer created successfully")
        print(f"Renderer type: {type(renderer)}")
        print(f"Renderer width: {renderer.width}")
        print(f"Renderer height: {renderer.height}")
        
        # Return for Jupyter testing
        return fig, renderer
        
    except Exception as e:
        print(f"❌ Renderer failed: {e}")
        import traceback
        traceback.print_exc()
        return fig, None

def test_camera_bounds_calculation():
    """Test the camera bounds calculation specifically"""
    print("\n📐 TESTING CAMERA BOUNDS CALCULATION")
    print("=" * 50)
    
    # Create data with known bounds
    test_data = np.array([
        [-2.0, -3.0],  # Min X, Min Y
        [4.0, 5.0],    # Max X, Max Y
        [1.0, 1.0]     # Middle point
    ])
    
    print(f"Test data:\n{test_data}")
    print(f"Expected X bounds: {test_data[:, 0].min()} to {test_data[:, 0].max()}")
    print(f"Expected Y bounds: {test_data[:, 1].min()} to {test_data[:, 1].max()}")
    
    fig = hyp.plot(test_data, 'bo', markersize=10)
    
    print(f"\nCalculated camera bounds:")
    print(f"  Left: {fig.camera.left}")
    print(f"  Right: {fig.camera.right}")
    print(f"  Bottom: {fig.camera.bottom}")
    print(f"  Top: {fig.camera.top}")
    
    # Check if bounds are reasonable
    x_range = test_data[:, 0].max() - test_data[:, 0].min()
    y_range = test_data[:, 1].max() - test_data[:, 1].min()
    padding = 0.1
    
    expected_left = test_data[:, 0].min() - x_range * padding
    expected_right = test_data[:, 0].max() + x_range * padding
    expected_bottom = test_data[:, 1].min() - y_range * padding
    expected_top = test_data[:, 1].max() + y_range * padding
    
    print(f"\nExpected bounds with padding:")
    print(f"  Left: {expected_left:.2f}")
    print(f"  Right: {expected_right:.2f}")
    print(f"  Bottom: {expected_bottom:.2f}")
    print(f"  Top: {expected_top:.2f}")
    
    return fig

if __name__ == "__main__":
    print("🚀 HYPERTOOLS THREE.JS DIAGNOSTIC")
    print("=" * 60)
    
    # Test 1: Debug the main issue
    fig1, renderer1 = debug_2d_scatter_issue()
    
    # Test 2: Test camera bounds
    fig2 = test_camera_bounds_calculation()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY:")
    print("- Check the Y positions in the position array")
    print("- Verify camera bounds calculation")
    print("- Test if the issue is in the widget display system")
    print("=" * 60)