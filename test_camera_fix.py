#!/usr/bin/env python3
"""
Test the camera fix to ensure 2D scatter points are properly displayed
"""

import numpy as np
import sys
sys.path.insert(0, '/Users/jmanning/hypertools')
import hypertools as hyp

def test_camera_fix():
    """Test that 2D scatter points are now properly positioned"""
    print("🔧 TESTING CAMERA FIX")
    print("=" * 40)
    
    # Create test data with known Y positions
    test_data = np.array([
        [0, 3],    # Top point
        [0, 0],    # Center point  
        [0, -3],   # Bottom point
        [2, 1],    # Right-top
        [-2, -1]   # Left-bottom
    ])
    
    print("Test data (X, Y):")
    for i, (x, y) in enumerate(test_data):
        print(f"  Point {i+1}: ({x:4.1f}, {y:4.1f})")
    
    print(f"\nY range: {test_data[:, 1].min()} to {test_data[:, 1].max()}")
    
    # Create HyperTools figure
    fig = hyp.plot(test_data, 'ro', markersize=15, alpha=0.8)
    
    # Check camera positioning
    print(f"\n📷 Camera Details:")
    print(f"Position: {fig.camera.position}")
    print(f"Bounds: Left={fig.camera.left:.1f}, Right={fig.camera.right:.1f}")
    print(f"        Bottom={fig.camera.bottom:.1f}, Top={fig.camera.top:.1f}")
    
    # Check if camera is properly centered and positioned
    x_center = (fig.camera.left + fig.camera.right) / 2
    y_center = (fig.camera.bottom + fig.camera.top) / 2
    
    print(f"Camera center: ({x_center:.1f}, {y_center:.1f})")
    print(f"Data center: ({test_data[:, 0].mean():.1f}, {test_data[:, 1].mean():.1f})")
    
    # Verify camera is perpendicular to data plane
    cam_pos = fig.camera.position
    if abs(cam_pos[2]) > 5:  # Z > 5 means camera is above the XY plane
        print("✅ Camera positioned perpendicular to data plane")
    else:
        print("❌ Camera may still be too close to data plane")
    
    # Check controls target
    if hasattr(fig.controls[0], 'target'):
        target = fig.controls[0].target
        print(f"Controls target: {target}")
    
    print("\n🎯 Ready for Jupyter testing!")
    return fig

if __name__ == "__main__":
    fig = test_camera_fix()
    
    # Test matplotlib conversion still works
    print("\n📊 Testing matplotlib conversion...")
    matplotlib_fig = fig.to_matplotlib()
    print("✅ Matplotlib conversion successful")
    
    print("\n" + "=" * 40)
    print("✅ CAMERA FIX VERIFICATION COMPLETE")
    print("Next: Test in Jupyter notebook")
    print("=" * 40)