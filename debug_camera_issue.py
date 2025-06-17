#!/usr/bin/env python3
"""
Debug why the camera fix isn't working properly
"""

import numpy as np
import sys
sys.path.insert(0, '/Users/jmanning/hypertools')
import hypertools as hyp

def debug_camera_positioning():
    """Debug the camera positioning calculation"""
    print("🔍 DEBUGGING CAMERA POSITIONING")
    print("=" * 50)
    
    # Test with the exact data from the failing test
    test_data = np.array([
        [0, 3],    # Top point
        [0, 0],    # Center point  
        [0, -3],   # Bottom point
        [2, 1],    # Right-top
        [-2, -1]   # Left-bottom
    ])
    
    print(f"Test data:\n{test_data}")
    print(f"X range: {test_data[:, 0].min()} to {test_data[:, 0].max()}")
    print(f"Y range: {test_data[:, 1].min()} to {test_data[:, 1].max()}")
    
    # Step through the camera calculation manually
    x_min, x_max = test_data[:, 0].min(), test_data[:, 0].max()
    y_min, y_max = test_data[:, 1].min(), test_data[:, 1].max()
    
    print(f"\nData bounds:")
    print(f"  X: {x_min} to {x_max}")
    print(f"  Y: {y_min} to {y_max}")
    
    # Calculate center as our code does
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    z_center = 0
    
    print(f"\nCalculated centers:")
    print(f"  X center: {x_center}")
    print(f"  Y center: {y_center}")
    print(f"  Z center: {z_center}")
    
    print(f"\nExpected camera position: ({x_center}, {y_center}, 10)")
    
    # Create the actual figure and check what happens
    fig = hyp.plot(test_data, 'ro', markersize=15)
    
    print(f"\nActual camera position: {fig.camera.position}")
    print(f"Actual camera bounds:")
    print(f"  Left: {fig.camera.left}, Right: {fig.camera.right}")
    print(f"  Bottom: {fig.camera.bottom}, Top: {fig.camera.top}")
    
    # Check the data conversion
    positions = fig._data_to_positions(fig.datasets[0])
    positions_3d = positions.reshape(-1, 3)
    print(f"\n3D positions:\n{positions_3d}")
    
    return fig

def test_simple_case():
    """Test with an even simpler case"""
    print("\n🧪 TESTING SIMPLE CASE")
    print("=" * 30)
    
    # Very simple data
    simple_data = np.array([
        [0, 1],   # Top
        [0, -1]   # Bottom
    ])
    
    print(f"Simple data:\n{simple_data}")
    
    fig = hyp.plot(simple_data, 'bo', markersize=20)
    print(f"Camera position: {fig.camera.position}")
    print(f"Should be: (0, 0, 10)")
    
    return fig

if __name__ == "__main__":
    print("🚨 CAMERA POSITIONING DEBUG")
    print("=" * 60)
    
    fig1 = debug_camera_positioning()
    fig2 = test_simple_case()
    
    print("\n" + "=" * 60)
    print("📋 ANALYSIS:")
    print("- Check if camera position matches expected values")
    print("- Verify 3D positions have correct Y coordinates")  
    print("- Identify where the positioning goes wrong")
    print("=" * 60)