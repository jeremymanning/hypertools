#!/usr/bin/env python3
"""
Simple debugging script to check data positioning in Three.js backend
"""

import numpy as np
import sys
sys.path.insert(0, '/Users/jmanning/hypertools')
import hypertools as hyp

def debug_plot():
    """Debug basic plotting functionality"""
    print("🔍 DEBUGGING SIMPLE PLOT")
    print("=" * 40)
    
    # Simple test data
    test_data = np.array([
        [0, 2],    # Should be at Y=2
        [1, 1],    # Should be at Y=1  
        [2, 0],    # Should be at Y=0
        [3, -1],   # Should be at Y=-1
        [4, -2]    # Should be at Y=-2
    ])
    
    print("Test data (X, Y):")
    for i, (x, y) in enumerate(test_data):
        print(f"  Point {i+1}: ({x}, {y})")
    
    # Create HyperTools figure
    print("\n📊 Creating plot...")
    fig = hyp.plot(test_data, 'ro', markersize=12)
    
    # Debug the internal data processing
    print(f"\n🔧 Figure internals:")
    print(f"Number of datasets: {fig.n_datasets}")
    print(f"Dimensionality: {fig.dimensionality}")
    
    # Check the standardized data
    dataset = fig.datasets[0]
    print(f"\nStandardized data:")
    print(dataset)
    
    # Check the positions array that gets sent to Three.js
    positions = fig._data_to_positions(dataset)
    print(f"\nThree.js positions array (flattened):")
    # Reshape back to (n_points, 3) for readability
    positions_3d = positions.reshape(-1, 3)
    for i, (x, y, z) in enumerate(positions_3d):
        print(f"  Point {i+1}: ({x:.1f}, {y:.1f}, {z:.1f})")
    
    # Check camera setup
    print(f"\n📷 Camera:")
    print(f"Type: {type(fig.camera).__name__}")
    print(f"Position: {fig.camera.position}")
    print(f"FOV: {fig.camera.fov if hasattr(fig.camera, 'fov') else 'N/A'}")
    
    if fig.controls:
        print(f"Controls target: {fig.controls[0].target}")
    
    return fig

if __name__ == "__main__":
    fig = debug_plot()
    print("\n✅ Debug complete - check above output for issues")